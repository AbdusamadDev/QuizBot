import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

from conf import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

questions = [
    {
        "question": "What is the capital of France?",
        "options": ["Paris", "Berlin", "London"],
    },
    {
        "question": "Who wrote 'Romeo and Juliet'?",
        "options": ["William Shakespeare", "Jane Austen", "Charles Dickens"],
    },
    {
        "question": "What is the largest mammal in the world?",
        "options": ["Blue whale", "Elephant", "Giraffe"],
    },
    {
        "question": "What is the chemical symbol for water?",
        "options": ["H2O", "CO2", "O2"],
    },
]


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("Welcome to the Quiz Bot! Here's your first question:")
    await ask_question(message)


async def ask_question(message: types.Message):
    question = random.choice(questions)
    options = question["options"]
    markup = types.InlineKeyboardMarkup(row_width=1)
    for option in options:
        markup.add(types.InlineKeyboardButton(text=option, callback_data=option))
    await message.reply(question["question"], reply_markup=markup)


@dp.callback_query_handler(
    lambda c: c.data
    in [option for question in questions for option in question["options"]]
)
async def process_answer(callback_query: types.CallbackQuery):
    selected_option = callback_query.data
    for question in questions:
        if selected_option in question["options"]:
            if selected_option == question["options"][0]:
                await bot.answer_callback_query(callback_query.id, "Correct!")
            else:
                await bot.answer_callback_query(
                    callback_query.id,
                    "Incorrect! The correct answer is: " + question["options"][0],
                )
            await ask_question(callback_query.message)
            return


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
