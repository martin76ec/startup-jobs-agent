from firecrawl import FirecrawlApp
from src.domain.job_offers.job_offers import job_summarize_description
from src.domain.scrappers.base import OfferScrapper
from src.providers.constants.env import FIRECRAWL_API_KEY
from src.providers.genai.genai import GeminiSingleton


class FirecrawlScrapper(OfferScrapper):
  def __init__(self, url: str):
    super().__init__(url)
    self.driver = None

  def page_content_get(self):
    app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)
    return app.scrape_url(
      url=self.url,
      params={
        "formats": ["markdown"],
      },
    )

  def scrap(self):
    content = self.page_content_get()
    gemini = GeminiSingleton.get_instance()
    reduced = gemini.generate_content(
      contents=f"show me all the data of the job offer, it doesnt matter if there is a show more button, just extact the data you are able to find: \n\n {content}"
    )
    summary = job_summarize_description(reduced.text)
    self.offer_data.role = summary.name
    self.offer_data.remote = summary.name
    self.offer_data.company_name = summary.startup
    self.offer_data.apply_url = summary.apply_url
    self.offer_data.location = summary.company_hq
    self.offer_data.details = summary.details

    return self.offer_data
