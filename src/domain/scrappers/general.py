from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from src.domain.scrappers.base import OfferScrapper


class GeneralScrapper(OfferScrapper):
  def __init__(self, url: str, driver: WebDriver):
    super().__init__(url)
    self.driver = driver

  def get_full_dom_after_load(self, timeout: int = 20) -> BeautifulSoup:
    WebDriverWait(self.driver, timeout).until(lambda d: d.execute_script("return document.readyState") == "complete")
    page_source = self.driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    return soup

  def extract_text_from_dom(self, soup: BeautifulSoup) -> str:
    paragraphs = soup.find_all(["p", "li"])
    return "\n".join([el.get_text(strip=True) for el in paragraphs if el.get_text(strip=True)])

  def get_page_text_from_dom(self) -> str:
    soup = self.get_full_dom_after_load()
    return self.extract_text_from_dom(soup)

  def scrap(self):
    content = self.get_page_text_from_dom()
    return content
