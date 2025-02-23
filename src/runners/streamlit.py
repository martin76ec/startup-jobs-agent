import streamlit as st
import tempfile
from src.infrastructure.selenium import ChromeDriverSingleton
from src.readers.pdf import summarize_content
from streamlit.runtime.uploaded_file_manager import UploadedFile
from src.scrapers.linkedin import LinkedInScrapper
from PIL import Image


def process_text_input(text):
    breakpoint()
    driver = ChromeDriverSingleton.get_instance()
    linkedin = LinkedInScrapper(text, driver)
    content = linkedin.scrap()
    st.write(f"Procesando: {text.upper()}")
    with st.expander("ver resumen"):
        st.markdown(content)


def process_pdf(file: UploadedFile):
    st.write(f"Processing PDF: {file.name}")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file.read())
        tmp_path = tmp.name
    content = summarize_content(tmp_path)
    with st.expander("ver resumen"):
        st.markdown(content)


def process_image(file: UploadedFile):
    st.write(f"Processing Image: {file.name}")

    try:
        image = Image.open(file)
    except Exception as e:
        st.error("Error abriendo la imagen " + e.__str__())
        return

    with tempfile.NamedTemporaryFile(delete=False, suffix=".webp") as tmp:
        image.save(tmp, format="WEBP")
        tmp_path = tmp.name

    content = summarize_content(tmp_path)

    with st.expander("Ver resumen"):
        st.markdown(content)


def run_app():
    st.title("Startuper Tool")
    input_type = st.sidebar.selectbox(
        "Escoje la fuente de la oferta", ("URL", "PDF", "Imagen")
    )

    if input_type == "URL":
        user_text = st.text_area("Enter your text below:")
        if st.button("Procesar"):
            process_text_input(user_text)

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
