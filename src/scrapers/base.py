from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
from selenium.webdriver.chrome.webdriver import WebDriver


@dataclass
class OfferData:
    title: Optional[str] = field(default=None)
    position: Optional[str] = field(default=None)
    type: Optional[str] = field(default=None)
    hours: Optional[str] = field(default=None)
    seniority: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)


class OfferScrapper(ABC):
    def __init__(self, url: str, driver: WebDriver):
        self.url = url
        self.driver = driver
        self.offer_data = OfferData()

    @abstractmethod
    def scrap(self) -> OfferData:
        """Main method to orchestrate the scraping process."""
        pass
