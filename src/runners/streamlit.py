import asyncio
import streamlit as st
from scrapers.linkedin import scrape_jobs, scrape_website

st.title("AI Web Scraper")
url = st.text_input("Enter a websiete URL")

if st.button("Scrape Site"):
    st.write("Scrapping the website")
    result = asyncio.run(scrape_jobs())
    print("Scraped Data:", result)

    if result is not None:
        st.session_state.scraped_data = (
            result  # Guardar en session_state para persistencia
        )

        # Mostrar la información en una tabla
        st.subheader("Job Details:")
        st.dataframe(
            result, use_container_width=True
        )  # ajusta la tabla al ancho del contenedor
    else:
        st.error("Failed to scrape the website. Try again.")
