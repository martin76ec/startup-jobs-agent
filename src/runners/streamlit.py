import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
import tempfile

from src.readers.pdf import summarize_content


def process_text_input(text):
    st.write(f"Processed Text: {text.upper()}")


def process_pdf(file: UploadedFile):
    st.write(f"Processing PDF: {file.name}")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file.read())
        tmp_path = tmp.name
    content = summarize_content(tmp_path)
    with st.expander("ver resumen"):
        st.markdown(content)


def process_image(uploaded_file: UploadedFile):
    st.image(uploaded_file, caption="Uploaded Image")
    st.write("Image processed successfully!")


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
