from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from config import GOOGLE_API_KEY, GROQ_API_KEY

# Agent A: Gemini 2.0 Flash
gemini = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    google_api_key=GOOGLE_API_KEY
)

# Agent B: Groq LLaMA 3.1 8B Instant
llama = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model="llama-3.1-8b-instant",
    temperature=0.3,
)
