from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from time import strftime
from typing import Optional
from google.auth import default
from selenium.webdriver.chrome.webdriver import WebDriver


@dataclass
class OfferData:
    role: Optional[str] = field(default=None)
    remote: Optional[bool] = field(default=None)
    company_name: Optional[str] = field(default=None)
    vertical: Optional[str] = field(default=None)
    apply_url: Optional[str] = field(default=None)
    location: Optional[str] = field(default=None)
    details: Optional[str] = field(default=None)
    date_scraped: str = field(default=strftime("%m/%d/%Y:%H:%M:%S"))


class OfferScrapper(ABC):
    def __init__(self, url: str, driver: WebDriver):
        self.url = url
        self.driver = driver
        self.offer_data = OfferData()

    @abstractmethod
    def scrap(self) -> OfferData:
        """Main method to orchestrate the scraping process."""
        pass
