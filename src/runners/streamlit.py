import streamlit as st
from src.scrapers.linkedin import scrape_website

st.title("AI Web Scraper")
url = st.text_input("Enter a websiete URL")

if st.button("Scrape Site"):
    st.write("Scrapping the website")
    result = scrape_website(url)
    print(result)
