from dataclasses import dataclass
from typing import Optional

from src.providers.generic_scraper_provider import GenericScraperProvider

@dataclass
class JobOffer:
    title: str
    description: str
    company: Optional[str] = None
    location: Optional[str] = None
    salary: Optional[str] = None
    requirements: Optional[str] = None
    benefits: Optional[str] = None
    url: Optional[str] = None
    source: str = "generic"

class GenericWebScraper:
    def __init__(self, url: str):
        self.url = url
        self.provider = GenericScraperProvider()
    
    def scrap(self) -> JobOffer:
        content = self.provider.scrape(self.url)
        
        if content.status == 'error':
            raise Exception(f"Failed to scrape URL: {content.error}")
        
        # Extract job details from the content
        title = content.metadata.title or "Untitled Position"
        description = content.main_content
        
        # Try to identify company and location from metadata or content
        company = None
        location = None
        
        # Look for common patterns in the content
        text_lines = description.split('\n')
        for line in text_lines[:10]:  # Check first 10 lines for company/location
            line = line.lower()
            if any(word in line for word in ['company:', 'empresa:', 'organización:']):
                company = line.split(':', 1)[1].strip().title()
            elif any(word in line for word in ['location:', 'ubicación:', 'lugar:']):
                location = line.split(':', 1)[1].strip().title()
        
        return JobOffer(
            title=title,
            description=description,
            company=company,
            location=location,
            url=self.url
        ) 