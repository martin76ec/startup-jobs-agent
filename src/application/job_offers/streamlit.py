import re
import tempfile
from urllib.parse import parse_qs, urlparse

from src.domain.scrappers.linkedin_job import LinkedInJobScrapper
import streamlit as st
from PIL import Image
from selenium.webdriver.chrome.webdriver import WebDriver
from streamlit.runtime.uploaded_file_manager import UploadedFile

from src.domain.scrappers.general import GeneralScrapper
from src.domain.scrappers.linkedin import LinkedInScrapper
from src.domain.scrappers.pdf import PdfScrapper
from src.domain.scrappers.plain_text import PlainTextScrapper
from src.infrastructure.positions_raw import PositionsDS
from src.providers.selenium.selenium import ChromeDriverSingleton
from src.providers.utils.job_offers import offer_to_markdown


def process_text(text: str):
  with st.spinner("Processing..."):
    offer = PlainTextScrapper(text).scrap()
    PositionsDS.position_create(offer)

  with st.expander("ver resumen"):
    st.markdown(offer_to_markdown(offer))


def _extract_linkedin_job_id(url: str) -> str | None:
  parsed_url = urlparse(url)
  match = re.search(r"/jobs/view/(\d+)", parsed_url.path)
  if match:
    return match.group(1)

  match = re.search(r"/jobs/(\d+)", parsed_url.path)
  if match:
    return match.group(1)

  if "/jobs/collections/recommended/" in parsed_url.path:
    query_params = parse_qs(parsed_url.query)
    current_job_id = query_params.get("currentJobId", [None])[0]
    if current_job_id:
      return current_job_id

  if "/jobs/search/results/" in parsed_url.path:
    query_params = parse_qs(parsed_url.query)
    current_job_id = query_params.get("currentJobId", [None])[0]
    if current_job_id:
      return current_job_id

  if "/jobs/view/" in parsed_url.path:
    query_params = parse_qs(parsed_url.query)
    current_job_id = query_params.get("currentJobId", [None])[0]
    if current_job_id:
      return current_job_id

  return url


def _process_linkedin_url(url: str) -> str:
  job_id = _extract_linkedin_job_id(url)
  if job_id:
    return f"https://www.linkedin.com/jobs/view/{job_id}"
  else:
    st.error("Could not extract job ID from LinkedIn URL.")
    return url


# def process_url(url):
#   with st.spinner(f"Processing {url}"):
#     driver = ChromeDriverSingleton.get_instance()
#     linkedin = LinkedInScrapper(url, driver)
#     offer = linkedin.scrap()
#     PositionsDS.position_create(offer)
#
#   with st.expander("ver resumen"):
#     st.markdown(offer_to_markdown(offer))


def process_url(url: str):
  with st.spinner(f"Processing {url}"):
    driver = ChromeDriverSingleton.get_instance()

    parsed_url = urlparse(url)
    if "linkedin.com" in parsed_url.netloc:
      linkedin_url = _process_linkedin_url(url)
      scrapper = LinkedInJobScrapper(linkedin_url, driver)
    else:
      scrapper = GeneralScrapper(url, driver)

    try:
      offer = scrapper.scrap()
      PositionsDS.position_create(offer)

      with st.expander("ver resumen"):
        st.markdown(offer_to_markdown(offer))

    except Exception as e:
      st.error(f"An error occurred while processing the URL: {e}")
      st.error(f"url: {url}")


def process_pdf(file: UploadedFile):
  with st.spinner(f"Processing {file.name}"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
      tmp.write(file.read())
      tmp_path = tmp.name

    pdf = PdfScrapper(tmp_path)
    offer = pdf.scrap()
    PositionsDS.position_create(offer)

  with st.expander("ver resumen"):
    st.markdown(offer_to_markdown(offer))


def process_image(file: UploadedFile):
  with st.spinner(f"Processing {file.name}"):
    image = Image.open(file)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webp") as tmp:
      image.save(tmp, format="WEBP")
      tmp_path = tmp.name
    pdf = PdfScrapper(tmp_path)
    offer = pdf.scrap()
    PositionsDS.position_create(offer)

  with st.expander("Ver resumen"):
    st.markdown(offer_to_markdown(offer))


def run_app():
  st.title("Startuper Tool")
  input_type = st.sidebar.selectbox("Escoje la fuente de la oferta", ("URL", "PDF", "Imagen", "Texto"))

  if input_type == "Texto":
    user_text = st.text_area("Ingresa la oferta:")
    if st.button("Procesar"):
      process_text(user_text)

  if input_type == "URL":
    user_text = st.text_area("Ingresa la url de la oferta:")
    if st.button("Procesar"):
      process_url(user_text)

  elif input_type == "PDF":
    uploaded_pdf = st.file_uploader("Subir un pdf", type=["pdf"])
    if uploaded_pdf is not None:
      process_pdf(uploaded_pdf)

  elif input_type == "Imagen":
    uploaded_image = st.file_uploader("Subir una imagen", type=["png", "jpg", "jpeg"])
    if uploaded_image is not None:
      process_image(uploaded_image)
