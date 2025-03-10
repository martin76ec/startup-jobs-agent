from langchain_groq import ChatGroq

from src.providers.constants.env import GROQ_KEY

groq_chat = ChatGroq(temperature=0, api_key=GROQ_KEY, model="mixtral-8x7b-32768")
