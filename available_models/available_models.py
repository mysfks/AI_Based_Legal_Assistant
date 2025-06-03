"""
    Available Models for Google Gemini API
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file.")

genai.configure(api_key=GOOGLE_API_KEY)

models = genai.list_models()

with open("models.txt", "w", encoding="utf-8") as f:
    for model in models:
        f.write(f"{model.name}\n")
        print(model.name)
