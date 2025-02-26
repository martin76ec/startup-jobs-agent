from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class OfferData:
    role: Optional[str] = field(default=None)
    remote: Optional[str] = field(default=None)
    company_name: Optional[str] = field(default="unknown")
    vertical: str = field(default="unknown")
    apply_url: Optional[str] = field(default=None)
    location: Optional[str] = field(default=None)
    details: Optional[str] = field(default="")
    date_scraped: str = field(
        default=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    )

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}


class OfferScrapper(ABC):
    def __init__(self, url: str):
        self.url = url
        self.offer_data = OfferData()

    @abstractmethod
    def scrap(self) -> OfferData:
        """Main method to orchestrate the scraping process."""
        pass
