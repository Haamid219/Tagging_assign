import os
from dotenv import load_dotenv

# 1. Load the .env file
load_dotenv()

class Settings:
    def __init__(self):
        # 2. Use a fallback empty string to prevent crashes, 
        # but print a warning if the key is missing.
        self.OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
        self.BASE_URL = "https://openrouter.ai/api/v1"
        self.MODEL_NAME = "nvidia/nemotron-3-super-120b-a12b:free"
        self.TAGS_FILE = "tags_assign.xlsx"

        if not self.OPENROUTER_KEY:
            print("⚠️ WARNING: OPENROUTER_API_KEY not found in .env file!")

# Initialize the instance
settings = Settings()