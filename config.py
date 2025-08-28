import os
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# print("FINNHUB_API_KEY:", FINNHUB_API_KEY)