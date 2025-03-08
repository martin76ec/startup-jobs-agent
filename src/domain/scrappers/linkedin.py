import time
from dataclasses import dataclass

from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.domain.job_offers.job_offers import job_summarize_description
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


class LinkedInScrapper(OfferScrapper):
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
  def title_get(self):
    return self.driver.find_element(By.XPATH, self.xpaths.title).text

  @error_handler_print()
  def company_name_get(self):
    return self.driver.find_element(By.XPATH, self.xpaths.company_name).text

  @error_handler_print()
  def position_get(self):
    return self.driver.find_element(By.XPATH, self.xpaths.position).text

  @error_handler_print()
  def remote_get(self):
    return self.driver.find_element(By.XPATH, self.xpaths.remote).text

  @error_handler_print()
  def location_get(self):
    return self.driver.find_element(By.XPATH, self.xpaths.location).text

  @error_handler_print()
  def description_get(self):
    wait = WebDriverWait(self.driver, 10)
    description_element = wait.until(EC.presence_of_element_located((By.ID, self.xpaths.description)))

    description = description_element.get_attribute("innerHTML")
    if description is None:
      return None

    soup = BeautifulSoup(description, "html.parser")
    paragraphs = soup.find_all(["p", "li"])
    return "\n".join([el.get_text(strip=True) for el in paragraphs if el.get_text(strip=True)])

  def scrap(self):
    self.login()
    self.offer_data.role = self.title_get()
    self.offer_data.remote = self.remote_get()
    self.offer_data.company_name = self.company_name_get()
    self.offer_data.apply_url = self.url
    self.offer_data.location = self.location_get()
    description = self.description_get()

    if description is None:
      raise (Exception("description not found."))

    summary = job_summarize_description(description)

    if self.offer_data.role is None:
      self.offer_data.role = summary.name
    if self.offer_data.company_name is None:
      self.offer_data.company_name = summary.startup
    if self.offer_data.location is None:
      self.offer_data.location = summary.company_hq

    self.offer_data.vertical = summary.vertical
    self.offer_data.details = summary.details

    return self.offer_data
