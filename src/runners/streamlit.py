import asyncio
import streamlit as st
from src.scrapers.linkedin import scrape_jobs

def streamlit_run():
    st.title("AI Web Scraper")

    if st.button("Scrape Site", type="primary"):
        st.write("Scrapping websites")
        result = asyncio.run(scrape_jobs())
        print("Scraped Data:", result)

        if result is not None:
            st.session_state.scraped_data = result
            st.subheader("Job Details:")
            st.dataframe(result, use_container_width=True)
        else:
            st.error("Failed to scrape the website. Try again.")
