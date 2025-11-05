import os
from dotenv import load_dotenv

load_dotenv()

class Settings():
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    MODEL_NAME = "openai/gpt-oss-120b"
    TEMPERATURE = 0.8
    MAX_RETRIES = 5

settings = Settings()  