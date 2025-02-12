from src.domain.jobs import jobs_get
import asyncio


data = asyncio.run(jobs_get())
print(data)
