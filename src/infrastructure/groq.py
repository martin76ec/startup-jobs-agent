from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from src.constants.env import GROQ_KEY

groq_chat = ChatGroq(
    temperature=0, groq_api_key=GROQ_KEY, model_name="mixtral-8x7b-32768"
)
