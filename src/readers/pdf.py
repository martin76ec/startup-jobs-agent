from google import generativeai
from src.infrastructure.genai import GeminiSingleton

def summarize_content(file: str):
    sample_file = generativeai.upload_file(path=file, display_name="job_offer")
    gemini = GeminiSingleton.get_instance()
    response = gemini.generate_content(
        [
            sample_file,
            "You are an expert human resources specialist, you are native in english and spanish, and you translate summarize and translate to spanish the job offer. Your output should be just the spanish offer in markdown and anything else",
        ]
    )

    return response.text
