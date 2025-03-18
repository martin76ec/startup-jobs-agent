from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
import os


class ChromeDriverSingleton:
  _instance = None

  @classmethod
  def get_driver(cls, options):
    driver = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
    val = webdriver.Chrome(
      service=Service(driver),
      options=options,
    )

    return val

  @classmethod
  def get_instance(cls):
    if cls._instance is None:
      options = Options()
      options.add_argument("--headless=new")
      options.add_argument("--no-sandbox")
      options.add_argument("--disable-dev-shm-usage")
      options.add_argument("--enable-logging")
      options.add_argument("--v=1")
      options.add_argument("--remote-debugging-pipe")
      options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
      )
      cls._instance = cls.get_driver(options)
    return cls._instance
