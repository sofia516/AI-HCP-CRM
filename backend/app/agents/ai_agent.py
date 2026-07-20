from langchain_groq import ChatGroq
from app.core.config import settings

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=settings.GROQ_API_KEY,
    temperature=0.2,
)