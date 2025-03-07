from typing import cast
from google import generativeai
from langchain_core import messages
from src.domain.job_offers.job_offers import (
    JobOffer,
    JobOfferStruct,
    job_summarize_description,
)
from src.providers.genai.genai import GeminiSingleton
from src.domain.scrappers.base import OfferScrapper
from langchain_core.prompts import ChatPromptTemplate
from src.providers.groq.groq import groq_chat


class PlainTextScrapper(OfferScrapper):
    offer: str

    def __init__(self, offer: str):
        super().__init__("")
        self.offer = offer

    def summarize_content(self, description: str):
        system: str = "You are an expert human resources specialist, you are native in english and spanish, and you translate summarize and translate to spanish the job offer. Your output should be just the spanish offer in markdown and anything else. If there is an apply url include it in the summary. Never try to introduce an application URL if there is not such thing, just don't add the url if it is not provided"
        human = "{text}"
        prompt = ChatPromptTemplate.from_messages(
            [("system", system), ("human", human)]
        )

        chain = prompt | groq_chat
        response = chain.invoke(
            {
                "text": f"""
        summarize #JOBOFFER
        {description}
        """
            }
        )

        return response.text()

    def scrap(self):
        content = self.summarize_content(self.offer)
        breakpoint()
        summary = job_summarize_description(content)
        self.offer_data.role = summary.name
        self.offer_data.remote = summary.remote
        self.offer_data.company_name = summary.startup
        self.offer_data.apply_url = summary.apply_url
        self.offer_data.location = summary.company_hq
        self.offer_data.vertical = summary.vertical
        self.offer_data.details = summary.details

        return self.offer_data
