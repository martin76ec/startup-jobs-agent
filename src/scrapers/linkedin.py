import selenium.webdriver as webdriver  # type: ignore
from selenium.webdriver.chrome.service import Service  # type: ignore
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from constants.env import LINKEDIN_EMAIL, LINKEDIN_PASSWORD
import time


def scrape_website(website):
    chrome_driver_path = "/usr/bin/chromedriver"
    chrome_binary_path = "/usr/bin/chromium-browser"
    options = Options()
    options.binary_location = chrome_binary_path
    options.add_argument("--no-sandbox")  # quita el aislamiento de procesos
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(website)
        print("Page loaded...")

        button = driver.find_element(
            By.XPATH,
            '//*[@id="base-contextual-sign-in-modal"]/div/section/div/div/div/div[2]/button',
        )
        button.click()
        time.sleep(5)
        user = driver.find_element(
            By.XPATH, '//*[@id="base-sign-in-modal_session_key"]'
        )
        user.send_keys(LINKEDIN_EMAIL)

        pwd = driver.find_element(
            By.XPATH, '//*[@id="base-sign-in-modal_session_password"]'
        )
        pwd.send_keys(LINKEDIN_PASSWORD)
        time.sleep(2)

        sbm = driver.find_element(
            By.XPATH,
            '//*[@id="base-sign-in-modal"]/div/section/div/div/form/div[2]/button',
        )
        sbm.click()
        time.sleep(5)

        # encontrar el tpitulo H1
        print("Reading position...")
        title = driver.find_element(
            By.XPATH,
            "/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[2]/div/h1",
        )
        print(title.text)

        # encontrar el Tipo (Remoto, hibrido o presencial)
        print("Reading type...")
        type = driver.find_element(
            By.XPATH,
            "/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[4]/ul/li[1]/span/span[1]/span/span[1]",
        )
        print(type.text)

        # encontrar Horas Laborales (Parcial , jornada completa)
        print("Reading working hours...")
        whours = driver.find_element(
            By.XPATH,
            "/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[4]/ul/li[1]/span/span[2]/span/span[1]",
        )
        print(whours.text)

        # encontrar el seniority (director, intermedio, etc)
        print("Reading level of seniority...")
        level = driver.find_element(
            By.XPATH,
            "/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[4]/ul/li[1]/span/span[3]",
        )
        print(level.text)

        # encontrar la descripcion
        print("Reading description...")
        desc = driver.find_element(By.XPATH, '//*[@id="job-details"]/div/p')
        print(desc.text)

        time.sleep(10)
    except Exception as e:
        print(e)
    finally:
        driver.quit()
