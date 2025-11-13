from langchain_goolge_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

gemini_llm = ChatGoogleGenerativeAI(model="gpt-4o", temperature=0)

