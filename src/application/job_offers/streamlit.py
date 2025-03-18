import re
import tempfile
from typing import Any, cast
from urllib.parse import parse_qs, urlparse

import streamlit as st
from PIL import Image
from streamlit.runtime.uploaded_file_manager import UploadedFile

from src.domain.scrappers.firecrawl import FirecrawlScrapper
from src.domain.scrappers.general import GeneralScrapper
from src.domain.scrappers.linkedin import LinkedInScrapper
from src.domain.scrappers.pdf import PdfScrapper
from src.domain.scrappers.plain_text import PlainTextScrapper
from src.infrastructure.positions_raw import PositionsDS
from src.providers.selenium.selenium import ChromeDriverSingleton
from src.providers.utils.job_offers import offer_to_markdown


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


def process_text(text: str):
  offer = PlainTextScrapper(text).scrap()
  PositionsDS.position_create(offer)
  return offer


def process_url(url: str):
  driver = ChromeDriverSingleton.get_instance()
  parsed_url = urlparse(url)

  if "linkedin.com" in parsed_url.netloc:
    linkedin_url = _process_linkedin_url(url)
    scrapper = LinkedInScrapper(linkedin_url, driver)
  else:
    scrapper = FirecrawlScrapper(url)

  offer = scrapper.scrap()
  PositionsDS.position_create(offer)
  return offer


def process_pdf(file: UploadedFile):
  with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
    tmp.write(file.read())
    tmp_path = tmp.name

  pdf = PdfScrapper(tmp_path)
  offer = pdf.scrap()
  PositionsDS.position_create(offer)
  return offer


def process_image(file: UploadedFile):
  image = Image.open(file)
  with tempfile.NamedTemporaryFile(delete=False, suffix=".webp") as tmp:
    image.save(tmp, format="WEBP")
    tmp_path = tmp.name
  pdf = PdfScrapper(tmp_path)
  offer = pdf.scrap()
  PositionsDS.position_create(offer)
  return offer


def run_app():
  st.title("Startuper Tool")
  processing = st.session_state.get("processing", False)
  input_type = st.sidebar.selectbox("Escoje la fuente de la oferta", ("URL", "PDF", "Imagen", "Texto"))
  target: Any = st.session_state.get("target", None)
  file: Any = st.session_state.get("file", None)
  response = st.session_state.get("response", None)

  labels = {
    "URL": "Ingresa la url de la oferta:",
    "PDF": "Subir un pdf:",
    "Imagen": "Subir una imagen:",
    "Texto": "Ingrese la oferta:",
  }

  user_text = None
  user_file = None

  if input_type == "PDF":
    user_file = st.file_uploader("Subir un pdf", type=["pdf"])
  elif input_type == "Imagen":
    user_file = st.file_uploader("Subir una imagen", type=["png", "jpeg", "jpg"], disabled=processing)
  else:
    user_text = st.text_area(labels[input_type], disabled=processing)

  if st.button("Procesar", disabled=processing):
    st.session_state.processing = True
    st.session_state.response = None
    st.rerun()

  if response is not None:
    with st.expander("ver resumen"):
      st.markdown(offer_to_markdown(response))

  if processing:
    res = None
    with st.spinner("Procesando..."):
      try:
        if input_type == "URL":
          res = process_url(target)
        elif input_type == "PDF":
          res = process_pdf(file)
        elif input_type == "Imagen":
          res = process_image(file)
        else:
          res = process_text(target)
      except Exception as e:
        print(e)
        st.error(
          "Tenemos un error interno, lo estamos solucionando, pero podrías probar con las opciones de PDF, imagen y Texto, agrademos mucho tu comprensión"
        )

      st.session_state.processing = False
      st.session_state.response = res
      st.rerun()

  if not processing:
    st.session_state.handler = input_type
    st.session_state.target = user_text
    st.session_state.file = user_file
