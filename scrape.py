import os
import pandas as pd # type: ignore
import selenium.webdriver as webdriver # type: ignore
import time
from dotenv import load_dotenv # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

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
        try:
            driver.get(website)
            print("Loading page...")
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
            time.sleep(3)
            print("Login successful!")

        except:
            print("Could not login...")

        job_data = {}

        try:
            # encontrar el titulo H1
            print("Reading position...")
            title = driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[2]/div/h1').text
            job_data['title'] = title
        except:
            job_data['title'] = "null"

        try:
            # encontrar el Tipo (Remoto, hibrido o presencial)
            print("Reading type...")
            type = driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[4]/ul/li[1]/span/span[1]/span/span[1]').text
            job_data['type'] = type
        except:
            job_data['type'] = "null"

        try:
            # encontrar Horas Laborales (Parcial , jornada completa)
            print("Reading working hours...")
            hours = driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[4]/ul/li[1]/span/span[2]/span/span[1]').text
            job_data['hours'] = hours
        except:
            job_data['hours'] = "null"

        try:
            # encontrar el seniority (director, intermedio, etc)
            print("Reading level of seniority...")
            seniority = driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[4]/ul/li[1]/span/span[3]').text
            job_data['seniority'] = seniority
        except:
            job_data['seniority'] = "null"

        try:
            # encontrar la descripcion
            print("Reading description...")
            description = driver.find_element(By.XPATH, '//*[@id="job-details"]/div/p').text
            job_data['description'] = description
        except:
            job_data['description'] = "null"

        time.sleep(10)
        return job_data
        driver.quit()

        # Convertir a DataFrame
        df = pd.DataFrame([job_data])
        return df

    except Exception as e:
        print("❌ Error en el scraping:", str(e))
        return None

    finally:
        driver.quit()  # Cierra el navegador


# Ejecutar automáticamente si el script se corre directamente
'''
if __name__ == "__main__":
    URL_HARDCODEADA = "https://www.linkedin.com/jobs/search/?currentJobId=4131896161&distance=25&geoId=102927786&keywords=product%20manager&origin=JOBS_HOME_KEYWORD_HISTORY&refresh=true"
    resultado = scrape_website(URL_HARDCODEADA)

    if resultado:
        print("Scraping exitoso")
    else:
        print("Hubo un error en el scraping")
'''
