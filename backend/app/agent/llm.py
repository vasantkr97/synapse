from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

gemini_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=api_key, temperature=0)

