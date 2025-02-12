from src.domain.jobs import jobs_get_by_status
import asyncio


data = asyncio.run(jobs_get_by_status("In Review"))
print(data)
