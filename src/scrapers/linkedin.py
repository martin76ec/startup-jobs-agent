from dataclasses import dataclass
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from src.constants.env import LINKEDIN_EMAIL, LINKEDIN_PASSWORD
from src.constants.utils import error_handler_print
from src.domain.jobs import job_summarize_description
from src.scrapers.base import OfferScrapper
import time


@dataclass
class LinkedInXPaths:
    login_button: str
    email_input: str
    pass_input: str
    auth_button: str
    offer_title: str
    offer_position: str
    offer_type: str
    offer_hours: str
    offer_seniority: str
    offer_description: str


class LinkedInScrapper(OfferScrapper):
    xpaths = LinkedInXPaths(
        login_button='//*[@id="base-contextual-sign-in-modal"]/div/section/div/div/div/div[2]/button',
        email_input='//*[@id="base-sign-in-modal_session_key"]',
        pass_input='//*[@id="base-sign-in-modal_session_password"]',
        auth_button='//*[@id="base-sign-in-modal"]/div/section/div/div/form/div[2]/button',
        offer_title="/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[2]/div/h1",
        offer_position="/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[4]/ul/li[1]/span/span[1]/span/span[2]",
        offer_type="/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[4]/ul/li[1]/span/span[1]/span/span[1]",
        offer_hours="/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[4]/ul/li[1]/span/span[2]/span/span[1]",
        offer_seniority="/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[4]/ul/li[1]/span/span[3]",
        offer_description="job-details",
    )

    def login(self):
        self.driver.get(self.url)
        self.driver.find_element(By.XPATH, self.xpaths.login_button).click()
        time.sleep(5)

        self.driver.find_element(By.XPATH, self.xpaths.email_input).send_keys(
            LINKEDIN_EMAIL
        )
        self.driver.find_element(By.XPATH, self.xpaths.pass_input).send_keys(
            LINKEDIN_PASSWORD
        )
        time.sleep(2)

        self.driver.find_element(By.XPATH, self.xpaths.auth_button).click()
        time.sleep(3)

    @error_handler_print()
    def title_get(self):
        return self.driver.find_element(By.XPATH, self.xpaths.offer_title).text

    @error_handler_print()
    def position_get(self):
        return self.driver.find_element(By.XPATH, self.xpaths.offer_position).text

    @error_handler_print()
    def type_get(self):
        return self.driver.find_element(By.XPATH, self.xpaths.offer_type).text

    @error_handler_print()
    def hours_get(self):
        return self.driver.find_element(By.XPATH, self.xpaths.offer_hours).text

    @error_handler_print()
    def seniority_get(self):
        return self.driver.find_element(By.XPATH, self.xpaths.offer_seniority).text

    @error_handler_print()
    def description_get(self):
        wait = WebDriverWait(self.driver, 10)
        description_element = wait.until(
            EC.presence_of_element_located((By.ID, self.xpaths.offer_description))
        )

        description = description_element.get_attribute("innerHTML")
        if description is None:
            return None

        soup = BeautifulSoup(description, "html.parser")
        paragraphs = soup.find_all(["p", "li"])
        return "\n".join(
            [el.get_text(strip=True) for el in paragraphs if el.get_text(strip=True)]
        )

    def scrap(self):
        self.login()
        self.offer_data.title = self.title_get()
        self.offer_data.position = self.position_get()
        self.offer_data.type = self.type_get()
        self.offer_data.hours = self.hours_get()
        self.offer_data.seniority = self.seniority_get()
        description = self.description_get()

        if description != None:
            self.offer_data.description = job_summarize_description(description)

        return self.offer_data
