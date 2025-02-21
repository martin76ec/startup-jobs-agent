from src.domain.jobs import jobs_get_by_status
from src.runners.streamlit import streamlit_run
from src.scrapers.linkedin import scrape_jobs
import asyncio

# jobs = asyncio.run(scrape_jobs())

# print(jobs)
streamlit_run()
