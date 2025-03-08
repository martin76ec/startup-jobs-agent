from google import generativeai

from src.domain.job_offers.job_offers import job_summarize_description
from src.domain.scrappers.base import OfferScrapper
from src.providers.genai.genai import GeminiSingleton


class PdfScrapper(OfferScrapper):
  def summarize_content(self, file: str):
    sample_file = generativeai.upload_file(path=file, display_name="job_offer")
    gemini = GeminiSingleton.get_instance()
    response = gemini.generate_content([
      sample_file,
      "You are an expert human resources specialist, you are native in english and spanish, and you translate summarize and translate to spanish the job offer. Your output should be just the spanish offer in markdown and anything else. If there is an apply url include it in the summary",
    ])

    return response.text

  def scrap(self):
    content = self.summarize_content(self.url)
    summary = job_summarize_description(content)
    self.offer_data.role = summary.name
    self.offer_data.remote = summary.remote
    self.offer_data.company_name = summary.startup
    self.offer_data.apply_url = summary.apply_url
    self.offer_data.location = summary.company_hq
    self.offer_data.vertical = summary.vertical
    self.offer_data.details = summary.details

    return self.offer_data
