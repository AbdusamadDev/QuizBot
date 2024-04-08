import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from client import create_exam, submit_exam
from conf import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


class ExamStates(StatesGroup):
    FULLNAME = State()
    GROUP = State()
    READY = State()
    EXAM = State()


# Function to create exam and fetch questions
async def create_exam_and_fetch_questions(fullname, group, state):
    exam_data = create_exam(fullname, group)
    exam_questions = exam_data.get("questions", [])
    exam_uuid = exam_data.get("uuid", "")
    return exam_questions, exam_uuid


@dp.message_handler(commands=["start"], state="*")
async def start(message: types.Message, state: FSMContext):
    await message.answer("Welcome to the Quiz Bot! Please provide your fullname:")
    await ExamStates.FULLNAME.set()


@dp.message_handler(state=ExamStates.FULLNAME)
async def process_fullname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["fullname"] = message.text
    await message.answer("Great! Now, please provide your group:")
    await ExamStates.GROUP.set()


@dp.message_handler(state=ExamStates.GROUP)
async def process_group(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["group"] = message.text
    exam_questions, exam_uuid = await create_exam_and_fetch_questions(
        data["fullname"], data["group"], state
    )
    async with state.proxy() as data:
        data["exam_questions"] = exam_questions
        data["asked_questions"] = []
        data["exam_uuid"] = exam_uuid
    await message.answer(
        f"Exam created! Exam UUID: {exam_uuid}. Are you ready to start the test? (yes/no)"
    )
    await ExamStates.READY.set()


@dp.message_handler(state=ExamStates.READY)
async def process_ready(message: types.Message, state: FSMContext):
    if message.text.lower() == "yes":
        await message.answer("Great! Let's begin.")
        await ExamStates.EXAM.set()
        await ask_question(message, state)
    else:
        await message.answer("Okay, whenever you're ready, just type 'yes'.")


async def ask_question(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        exam_questions = data["exam_questions"]
        asked_questions = data["asked_questions"]
        if len(asked_questions) == len(exam_questions):
            # All questions asked, send results
            answers = data.get("answers", [])
            await send_results(message, answers, data["exam_uuid"])
            return

        remaining_questions = [
            q for q in exam_questions if q["id"] not in asked_questions
        ]
        question_data = random.choice(remaining_questions)
        data["current_question"] = question_data["id"]
        asked_questions.append(question_data["id"])
        data["asked_questions"] = asked_questions

    question = question_data["title"]
    options = [
        question_data["option_1"],
        question_data["option_2"],
        question_data["option_3"],
        question_data["option_4"],
    ]

    markup = types.InlineKeyboardMarkup(row_width=1)
    for idx, option in enumerate(options, start=1):
        callback_data = (
            f"{question_data['id']}_{idx}"  # Format: question_id_option_index
        )
        markup.add(types.InlineKeyboardButton(text=option, callback_data=callback_data))

    await message.answer(question, reply_markup=markup)


@dp.callback_query_handler(state=ExamStates.EXAM)
async def process_answer(callback_query: types.CallbackQuery, state: FSMContext):
    selected_option_data = callback_query.data.split("_")
    question_id = int(selected_option_data[0])
    selected_option_index = int(selected_option_data[1]) - 1

    async with state.proxy() as data:
        answers = data.get("answers", [])
        answers.append({"qid": question_id, "ans": selected_option_index + 1})
        data["answers"] = answers

        # Delete the previous question
        await bot.delete_message(
            callback_query.message.chat.id, callback_query.message.message_id
        )
    await ask_question(callback_query.message, state)


async def send_results(message: types.Message, answers, exam_uuid):
    result_message = f"Here is an Exam UUID: {exam_uuid}:\n\n"
    await message.answer("🔄 Please wait for your exam result a while!")
    response = submit_exam(answers=answers, exam_uuid=exam_uuid)
    logging.info(f"Answers: {answers}\n\n\n")
    print(response)
    result_message += f"this is your result: {response.get('score')}"
    await message.answer(result_message)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
