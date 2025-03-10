from dataclasses import dataclass
import time

from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.domain.job_offers.job_offers import job_summarize_description, job_parse
from src.domain.scrappers.base import OfferScrapper
from src.providers.constants.env import LINKEDIN_EMAIL, LINKEDIN_PASSWORD
from src.providers.constants.utils import error_handler_print


@dataclass
class LinkedInXPaths:
  login_button: str
  email_input: str
  pass_input: str
  auth_button: str
  company_name: str
  title: str
  position: str
  remote: str
  location: str
  description: str


class LinkedInJobScrapper(OfferScrapper):
  xpaths = LinkedInXPaths(
    login_button='//*[@id="base-contextual-sign-in-modal"]/div/section/div/div/div/div[2]/button',
    email_input='//*[@id="base-sign-in-modal_session_key"]',
    pass_input='//*[@id="base-sign-in-modal_session_password"]',
    auth_button='//*[@id="base-sign-in-modal"]/div/section/div/div/form/div[2]/button',
    company_name="/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div/div[1]/div/div[1]/div/div[1]/div[1]/div/a",
    title="/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[2]/div/h1",
    position="/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[4]/ul/li[1]/span/span[1]/span/span[2]",
    remote="/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div/div[1]/div/div[1]/div/div[4]/ul/li[1]/span/span[1]/span/span[1]",
    location="/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div/div[1]/div/div[1]/div/div[3]/div/span[1]",
    description="job-details",
  )

  def __init__(self, url: str, driver: WebDriver):
    super().__init__(url)
    self.driver = driver

  @error_handler_print()
  def login(self):
    self.driver.get(self.url)
    self.driver.find_element(By.XPATH, self.xpaths.login_button).click()
    time.sleep(5)

    self.driver.find_element(By.XPATH, self.xpaths.email_input).send_keys(LINKEDIN_EMAIL)
    self.driver.find_element(By.XPATH, self.xpaths.pass_input).send_keys(LINKEDIN_PASSWORD)
    time.sleep(2)

    self.driver.find_element(By.XPATH, self.xpaths.auth_button).click()
    time.sleep(3)

  @error_handler_print()
  def details_get(self):
    wait = WebDriverWait(self.driver, 10)
    description_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jobs-search__job-details--wrapper")))
    description = description_element.get_attribute("innerHTML")
    if description is None:
      return None
    soup = BeautifulSoup(description, "html.parser")
    paragraphs = soup.find_all(["p", "li"])
    return "\n".join([el.get_text(strip=True) for el in paragraphs if el.get_text(strip=True)])

  @error_handler_print()
  def description_get(self):
    wait = WebDriverWait(self.driver, 10)
    description_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jobs-description__container")))
    description = description_element.get_attribute("innerHTML")
    if description is None:
      return None
    soup = BeautifulSoup(description, "html.parser")
    paragraphs = soup.find_all(["p", "li"])
    return "\n".join([el.get_text(strip=True) for el in paragraphs if el.get_text(strip=True)])

  def scrap(self):
    self.login()
    details = self.details_get()
    description = self.description_get()
    offer = f"""
    ## Details
    {details}

    ## Description
    {description}
    """
    offer_data = job_summarize_description(offer)
    breakpoint()
    return self.offer_data
