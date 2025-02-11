import os
from dotenv import load_dotenv # type: ignore
import selenium.webdriver as webdriver # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# url -> https://www.linkedin.com/jobs/search/?currentJobId=4131896161&distance=25&geoId=102927786&keywords=product%20manager&origin=JOBS_HOME_KEYWORD_HISTORY&refresh=true

load_dotenv()
LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

def scrape_website(website):
    print("lauching chrome browser...")

    chrome_driver_path = "/usr/local/bin/chromedriver/chromedriver"
    chrome_binary_path = "/usr/local/bin/google-chrome/chrome"

    options = Options()
    options.binary_location = chrome_binary_path
    # options = webdriver.ChromeOptions()

    # Evitar problemas de sesión y permisos
    options.add_argument("--no-sandbox") # quita el aislamiento de procesos
    # options.add_argument("--disable-dev-shm-usage") # usar disco en vez de memoria compartida de Chrome
    # options.add_argument("--disable-gpu")  # Opcional, útil si hay errores gráficos
    # options.add_argument("--headless")  # Opcional, si no necesitas interfaz gráfica, no abre navegador nuevo

    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(website)
        print("Page loaded...")
        html = driver.page_source

        # nuevo codigo para logueo
        button = driver.find_element(By.XPATH, '//*[@id="base-contextual-sign-in-modal"]/div/section/div/div/div/div[2]/button')
        button.click()
        time.sleep(5)
        user = driver.find_element(By.XPATH, '//*[@id="base-sign-in-modal_session_key"]')
        user.send_keys(LINKEDIN_EMAIL)

        pwd = driver.find_element(By.XPATH, '//*[@id="base-sign-in-modal_session_password"]')
        pwd.send_keys(LINKEDIN_PASSWORD)
        time.sleep(2)

        sbm = driver.find_element(By.XPATH,'//*[@id="base-sign-in-modal"]/div/section/div/div/form/div[2]/button')
        sbm.click()

        time.sleep(30)
        return html

    except:
        print("Something went wrong!")
    # finally:
    #     driver.quit()
