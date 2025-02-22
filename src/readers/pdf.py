from google import generativeai
from streamlit.runtime.uploaded_file_manager import UploadedFile
from src.constants.env import GOOGLE_API_KEY

generativeai.configure(api_key=GOOGLE_API_KEY)
model = generativeai.GenerativeModel("gemini-1.5-flash")


def summarize_content(file: str):
    sample_file = generativeai.upload_file(path=file, display_name="job_offer")
    response = model.generate_content(
        [
            sample_file,
            "You are an expert human resources specialist, you are native in english and spanish, and you translate summarize and translate to spanish the job offer. Your output should be just the spanish offer in markdown and anything else",
        ]
    )

    return response.text
