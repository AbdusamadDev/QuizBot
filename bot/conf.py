from dotenv import load_dotenv
import os


load_dotenv()
TOKEN = os.environ.get("TOKEN")
TEST_URL = "http://localhost:8000"
BASE_URL = "https://osonquizapi.pythonanywhere.com"
