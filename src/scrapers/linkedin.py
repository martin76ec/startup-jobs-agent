import selenium.webdriver as webdriver  # type: ignore
from selenium.webdriver.chrome.service import Service  # type: ignore
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.constants.env import CHROME_BINARY_PATH, CHROME_DRIVER_PATH, LINKEDIN_EMAIL, LINKEDIN_PASSWORD
import time

from src.domain.jobs import job_summarize_description, jobs_get_by_status
from src.scrapers.link import LinkedInScrapper

async def scrape_jobs():
    jobs = await jobs_get_by_status("In Review")
    return [scrape_website(job.apply_url) for job in jobs]


def scrape_website(website):
    chrome_driver_path = CHROME_DRIVER_PATH
    chrome_binary_path = CHROME_BINARY_PATH

    options = Options()
    options.binary_location = chrome_binary_path
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")

    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
    scraper = LinkedInScrapper(url=website, driver=driver)
    offer_data = scraper.scrap()

    if offer_data.description != None:
        offer_data.description = job_summarize_description(offer_data.description)

    return offer_data
