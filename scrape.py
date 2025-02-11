import selenium.webdriver as webdriver # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
from selenium.webdriver.chrome.options import Options
import time

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
        time.sleep(10)

        return html
    finally:
        driver.quit()
