from src.domain.scrappers.plain_text import PlainTextScrapper
from src.infrastructure.positions_raw import PositionsDS
from src.providers.selenium.selenium import ChromeDriverSingleton
from src.providers.utils.job_offers import offer_to_markdown
from streamlit.runtime.uploaded_file_manager import UploadedFile
from src.domain.scrappers.linkedin import LinkedInScrapper
from src.domain.scrappers.pdf import PdfScrapper
from PIL import Image
import streamlit as st
import tempfile


def process_text(text: str):
    with st.spinner(f"Processing..."):
        offer = PlainTextScrapper(text).scrap()
        # PositionsDS.position_create(offer)

    with st.expander("ver resumen"):
        st.markdown(offer_to_markdown(offer))


def process_url(url):
    with st.spinner(f"Processing {url}"):
        driver = ChromeDriverSingleton.get_instance()
        linkedin = LinkedInScrapper(url, driver)
        offer = linkedin.scrap()
        PositionsDS.position_create(offer)

    with st.expander("ver resumen"):
        st.markdown(offer_to_markdown(offer))


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
    input_type = st.sidebar.selectbox(
        "Escoje la fuente de la oferta", ("URL", "PDF", "Imagen", "Texto")
    )

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
        uploaded_image = st.file_uploader(
            "Subir una imagen", type=["png", "jpg", "jpeg"]
        )
        if uploaded_image is not None:
            process_image(uploaded_image)
