from google import generativeai
from src.providers.constants.env import GOOGLE_API_KEY

generativeai.configure(api_key=GOOGLE_API_KEY)


class GeminiSingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = generativeai.GenerativeModel("gemini-1.5-flash")
        return cls._instance
