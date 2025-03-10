from dataclasses import dataclass
from typing import List, Optional
from bs4 import BeautifulSoup
from src.infrastructure.http_fetcher import fetch, content_clean

@dataclass
class ScrapedMetadata:
    title: Optional[str] = None
    description: Optional[str] = None
    keywords: Optional[str] = None
    author: Optional[str] = None

@dataclass
class ScrapedContent:
    url: str
    metadata: ScrapedMetadata
    main_content: str
    structured_data: List[str]
    status: str
    error: Optional[str] = None

class GenericScraperProvider:
    @staticmethod
    def extract_metadata(soup: BeautifulSoup) -> ScrapedMetadata:
        metadata = ScrapedMetadata()
        
        title_tag = soup.find('title')
        if title_tag:
            metadata.title = title_tag.string.strip()
        
        meta_tags = soup.find_all('meta')
        for tag in meta_tags:
            if tag.get('name') and tag.get('content'):
                name = tag.get('name').lower()
                if hasattr(metadata, name):
                    setattr(metadata, name, tag.get('content'))
            elif tag.get('property') == 'og:description' and tag.get('content'):
                metadata.description = tag.get('content')
        
        return metadata

    @staticmethod
    def extract_main_content(soup: BeautifulSoup) -> str:
        main_content = ''
        
        content_identifiers = [
            {'tag': 'article'},
            {'tag': 'div', 'class_': 'content'},
            {'tag': 'div', 'class_': 'main-content'},
            {'tag': 'div', 'id': 'content'},
            {'tag': 'div', 'id': 'main-content'},
            {'tag': 'div', 'class_': 'post-content'},
        ]
        
        for identifier in content_identifiers:
            tag_name = identifier['tag']
            if 'class_' in identifier:
                elements = soup.find_all(tag_name, class_=identifier['class_'])
            elif 'id' in identifier:
                elements = soup.find_all(tag_name, id=identifier['id'])
            else:
                elements = soup.find_all(tag_name)
                
            for element in elements:
                content = content_clean(element)
                if content:
                    main_content += content + '\n'
        
        if not main_content.strip():
            paragraphs = soup.find_all('p')
            main_content = '\n'.join(p.get_text().strip() for p in paragraphs if p.get_text().strip())
        
        return main_content.strip()

    @staticmethod
    def scrape(url: str) -> ScrapedContent:
        try:
            response = fetch(url)
            soup = BeautifulSoup(response.content, "html.parser")
            
            metadata = GenericScraperProvider.extract_metadata(soup)
            main_content = GenericScraperProvider.extract_main_content(soup)
            
            structured_data = []
            for script in soup.find_all('script', type='application/ld+json'):
                if script.string:
                    structured_data.append(script.string)
            
            return ScrapedContent(
                url=url,
                metadata=metadata,
                main_content=main_content,
                structured_data=structured_data,
                status='success'
            )
            
        except Exception as e:
            return ScrapedContent(
                url=url,
                metadata=ScrapedMetadata(),
                main_content='',
                structured_data=[],
                status='error',
                error=str(e)
            ) 