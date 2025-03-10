from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType


class ChromeDriverSingleton:
  _instance = None

  @classmethod
  def get_driver(cls, options):
    return webdriver.Chrome(
      service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
      options=options,
    )

  @classmethod
  def get_instance(cls):
    if cls._instance is None:
      options = Options()
      options.add_argument("--no-sandbox")
      options.add_argument("--headless")
      cls._instance = cls.get_driver(options)
    return cls._instance
