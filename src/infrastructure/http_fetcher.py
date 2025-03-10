import requests
import re
import csv
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

ua = UserAgent()


def fetch(url: str):
  headers = {
    "User-Agent": ua.random,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.google.com/",  # example of a referer.
    "DNT": "1",
    "Connection": "keep-alive",
  }
  return requests.get(url, headers=headers)


def content_clean(content):
  if content:
    # Remove script and style elements
    for script_or_style in content(["script", "style"]):
      script_or_style.decompose()

    # Get text and handle whitespace
    text = content.get_text(separator="\n", strip=True)  # add newlines between elements.
    return text
  return None


def extract_scripts(soup):
  if not isinstance(soup, BeautifulSoup):
    return []

  script_tags = soup.find_all("script")
  script_contents = []

  for script in script_tags:
    if script.string:  # Check if the script tag has content
      script_contents.append(script.string)

  return script_contents


def extract_article_body_value(substring):
  try:
    match = re.search(r'\{.*?"articleBody":.*?"\}', substring)
    if match:
      return match.group()
    else:
      return None
  except Exception:
    return None


def main(url: str):
  doc = fetch(url)
  content = BeautifulSoup(doc.content, "html.parser")
  scripts = extract_scripts(content)
  articles = [extract_article_body_value(script) for script in scripts]
  clean = [article for article in articles if article is not None]
  breakpoint()

  return clean[0] if len(clean) > 0 else None


def save_to_csv(data, filename="output.csv"):
  try:
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
      writer = csv.writer(csvfile)
      for item in data:
        writer.writerow([item])  # Write each string as a single-cell row
    print(f"Data saved to {filename}")
  except Exception as e:
    print(f"Error saving to CSV: {e}")


def extract_metadata(soup):
    """Extract metadata from the webpage"""
    metadata = {
        'title': None,
        'description': None,
        'keywords': None,
        'author': None
    }
    
    # Get title
    title_tag = soup.find('title')
    if title_tag:
        metadata['title'] = title_tag.string.strip()
    
    # Get meta tags
    meta_tags = soup.find_all('meta')
    for tag in meta_tags:
        if tag.get('name') and tag.get('content'):
            name = tag.get('name').lower()
            if name in metadata:
                metadata[name] = tag.get('content')
        elif tag.get('property') == 'og:description' and tag.get('content'):
            metadata['description'] = tag.get('content')
    
    return metadata

def extract_main_content(soup):
    """Extract main content from common content containers"""
    main_content = ''
    
    # Common content container IDs and classes
    content_identifiers = [
        {'tag': 'article'},
        {'tag': 'div', 'class_': 'content'},
        {'tag': 'div', 'class_': 'main-content'},
        {'tag': 'div', 'id': 'content'},
        {'tag': 'div', 'id': 'main-content'},
        {'tag': 'div', 'class_': 'post-content'},
    ]
    
    # Try to find content in common containers
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
    
    # If no content found in common containers, try getting all paragraphs
    if not main_content.strip():
        paragraphs = soup.find_all('p')
        main_content = '\n'.join(p.get_text().strip() for p in paragraphs if p.get_text().strip())
    
    return main_content.strip()

def generic_scraper(url: str):
    """
    A generic scraper that can handle any webpage and extract useful information
    Returns a dictionary containing metadata and content
    """
    try:
        response = fetch(url)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Extract metadata
        metadata = extract_metadata(soup)
        
        # Extract main content
        main_content = extract_main_content(soup)
        
        # Extract any structured data (JSON-LD)
        structured_data = []
        for script in soup.find_all('script', type='application/ld+json'):
            if script.string:
                structured_data.append(script.string)
        
        return {
            'url': url,
            'metadata': metadata,
            'main_content': main_content,
            'structured_data': structured_data,
            'status': 'success'
        }
        
    except Exception as e:
        return {
            'url': url,
            'status': 'error',
            'error': str(e)
        }

urls = [
  # "https://www.linkedin.com/posts/rodrigoromero86_hiring-seniorengineer-laravel-activity-7303840097920077825-7L9h?utm_source=share&utm_medium=member_android&rcm=ACoAAEfXK-QBU9l_2kY26rPpqEpHehiuNrmSzZE",
  # "https://www.linkedin.com/jobs/4180807059/view",
  # "https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4176296656",
  # "https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4063319063",
  # "https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4105269389",
  # "https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4174925335",
  "https://www.infojobs.net/ribeira/asesor-digitalizacion/of-i0122b2915c4361aeb3af83c21b0a86?applicationOrigin=search-new&page=1&sortBy=PUBLICATION_DATE"
]

# Example usage:
if __name__ == "__main__":
    # Example URLs list
    # articles = [main(url) for url in urls]  # Original article scraper
    # scraped_data = [generic_scraper(url) for url in urls]  # Generic scraper
    # clean = [article for article in articles if article is not None]
    # save_to_csv(clean)
