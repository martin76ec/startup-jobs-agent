import streamlit as st
import tempfile
from src.constants.env import DB_ID
from src.infrastructure.notion import notion
from src.infrastructure.positions_raw import PositionsDS
from src.infrastructure.selenium import ChromeDriverSingleton
from src.readers.pdf import summarize_content
from streamlit.runtime.uploaded_file_manager import UploadedFile
from src.scrapers.linkedin import LinkedInScrapper
from PIL import Image


def process_text_input(url):
    with st.spinner(f"Processing {url}"):
        # driver = ChromeDriverSingleton.get_instance()
        # linkedin = LinkedInScrapper(url, driver)
        # summary = linkedin.scrap()
        summary = {}

        status_id = None

        data = {
            "Role": "test",
            "Location": "test",
            "Summary": "test",
            "Vertical": "test",
            "Apply URL": "test",
            "Location": "test",
            "Summary": "test",
            "Status": {"id": status_id},
        }
        # breakpoint()

        PositionsDS.position_create(summary)
        notion.pages.create(parent={"database_id": DB_ID}, properties=data)

        # with st.expander("ver resumen"):
        #     # st.markdown(summary)
        #
        # if st.button("guardar"):
        #     st.write("sadfasdf")
        #     print("#######################################################################")


def process_pdf(file: UploadedFile):
    with st.spinner(f"Processing {file.name}"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name
        content = summarize_content(tmp_path)

    with st.expander("ver resumen"):
        st.markdown(content)


def process_image(file: UploadedFile):
    with st.spinner(f"Processing {file.name}"):
        image = Image.open(file)
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
