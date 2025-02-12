import streamlit as st # type: ignore
from scrape import scrape_website

st.title("AI Web Scraper")
url = st.text_input("Enter a websiete URL")

if st.button("Scrape Site"):
    st.write("Scrapping the website")
    result = scrape_website(url)
    # print(result)

   # st.session_state.dom_content =
