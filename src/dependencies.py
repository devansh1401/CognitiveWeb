import os
from dotenv import load_dotenv
import google.generativeai as genai

def load_dotenv():
    load_dotenv()

def configure_genai():
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))