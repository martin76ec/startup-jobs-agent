from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from src.constants.env import CHROME_BINARY_PATH, CHROME_DRIVER_PATH

class ChromeDriverSingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            options = Options()
            options.binary_location = CHROME_BINARY_PATH
            options.add_argument("--no-sandbox")
            options.add_argument("--headless")
            cls._instance = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=options)
        return cls._instance
