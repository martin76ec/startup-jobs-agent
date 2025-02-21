import selenium.webdriver as webdriver  # type: ignore
from selenium.webdriver.chrome.service import Service  # type: ignore
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.constants.env import CHROME_BINARY_PATH, CHROME_DRIVER_PATH, LINKEDIN_EMAIL, LINKEDIN_PASSWORD
import time

from src.domain.jobs import job_summarize_description, jobs_get_by_status

async def scrape_jobs():
    jobs = await jobs_get_by_status("In Review")
    return [scrape_website(job.apply_url) for job in jobs]

def scrape_website(website):
    chrome_driver_path = CHROME_DRIVER_PATH
    chrome_binary_path = CHROME_BINARY_PATH

    options = Options()
    options.binary_location = chrome_binary_path
    options.add_argument("--no-sandbox")
    # options.add_argument("--headless")

    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        try:
            driver.get(website)
            wait = WebDriverWait(driver, 10)
            print("Loading page...")

            # nuevo codigo para logueo
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
            time.sleep(3)
            print("Login successful!")

        except:
            print("Could not login...")

        job_data = {}

        try:
            # encontrar el titulo H1
            print("Reading position...")
            title = driver.find_element(
                By.XPATH,
                "/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[2]/div/h1",
            ).text
            job_data["title"] = title
        except:
            job_data["title"] = "null"

        try:
            # encontrar el Tipo (Remoto, hibrido o presencial)
            print("Reading type...")
            type = driver.find_element(
                By.XPATH,
                "/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[4]/ul/li[1]/span/span[1]/span/span[1]",
            ).text
            job_data["type"] = type
        except:
            job_data["type"] = "null"

        try:
            # encontrar Horas Laborales (Parcial , jornada completa)
            print("Reading working hours...")
            hours = driver.find_element(
                By.XPATH,
                "/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[4]/ul/li[1]/span/span[2]/span/span[1]",
            ).text
            job_data["hours"] = hours
        except:
            job_data["hours"] = "null"

        try:
            # encontrar el seniority (director, intermedio, etc)
            print("Reading level of seniority...")
            seniority = driver.find_element(
                By.XPATH,
                "/html/body/div[6]/div[3]/div[2]/div/div/main/div[2]/div[1]/div/div[1]/div/div/div/div[4]/ul/li[1]/span/span[3]",
            ).text
            job_data["seniority"] = seniority
        except:
            job_data["seniority"] = "null"

        """ try:
            # encontrar la descripcion
            print("Reading description...")
            # description = driver.find_element(By.ID, "job-details").text
            job_description_element = driver.find_element(By.TAG_NAME, 'html').text
            print(job_description_element)
            print("----------")

            paragraphs = job_description_element.find_elements(By.TAG_NAME, "p")
            description = "\n".join([p.text for p in paragraphs if p.text.strip()])

            job_data["description"] = description
            print(description)
            print("----------")
            desc = job_summarize_description(description)
            job_data["description"] = desc

        except Exception as e:
            print(e)
            job_data["description"] = "null" """

        try:
            # encontrar la descripcion
            print("Reading description...")
            breakpoint()
            # Esperar hasta que la descripción del trabajo esté presente
            job_description_element = wait.until(
                EC.presence_of_element_located((By.ID, "job-details"))
            )
            # Buscar el botón padre que contiene al span con clase "see-more"
            try:
                see_more_button = wait.until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "text-expand-collapse-button"))
                )
                if see_more_button.is_displayed():
                    see_more_button.click()
                    time.sleep(2)  # Esperar a que se expanda el contenido
            except Exception as e:
                print("No se encontró el botón 'Ver más' o no se pudo hacer clic.")

            # Buscar el elemento que contiene la descripción del trabajo
            job_description_element = driver.find_element(By.ID, "job-details")
            paragraphs = job_description_element.find_elements(By.TAG_NAME, "p")

            job_description = "\n".join([p.text for p in paragraphs if p.text.strip()])

            return job_description
        except Exception as e:
            print(f"Error al obtener la descripción: {e}")
            return None

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
        print("casi terminamosss")
        # driver.quit()  # Cierra el navegador
