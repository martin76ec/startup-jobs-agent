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
        time.sleep(5)

        # encontrar el tpitulo H1
        print("Reading position...")
        title = driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[2]/div/h1')
        print(title.text)

        # encontrar el Tipo (Remoto, hibrido o presencial)
        print("Reading type...")
        type = driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[4]/ul/li[1]/span/span[1]/span/span[1]')
        print(type.text)

        # encontrar Horas Laborales (Parcial , jornada completa)
        print("Reading working hours...")
        whours = driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[4]/ul/li[1]/span/span[2]/span/span[1]')
        print(whours.text)

        # encontrar el seniority (director, intermedio, etc)
        print("Reading level of seniority...")
        level = driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[4]/ul/li[1]/span/span[3]')
        print(level.text)

        # encontrar la descripcion
        print("Reading description...")
        desc = driver.find_element(By.XPATH, '//*[@id="job-details"]/div/p')
        print(desc.text)

        time.sleep(10)
        ### Encontrar el <ul>
        # ul_element = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div/ul')
        # print(ul_element.text)

        '''
        # Encontrar todos los <li> dentro del <ul>
        li_elements = ul_element.find_elements(By.TAG_NAME, "li")

        # Iterar sobre cada <li>
        for li in li_elements:
            try:
                # Buscar el <a> siguiendo la estructura especificada
                a_element = li.find_element(By.XPATH, "./div[4]/div[2]/div[1]/a")

                # Extraer y mostrar el texto del <a>
                link_text = a_element.text

                print(f"Texto del enlace: {link_text}")

            except Exception as e:
                print("No se encontró el enlace en este <li>")

        time.sleep(30)
        # return html
        '''
    except:
        print("Something went wrong!")
    # finally:
    #     driver.quit()


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
