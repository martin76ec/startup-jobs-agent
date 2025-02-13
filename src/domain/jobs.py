from typing import Any, Dict, Literal, Optional, cast
from src.constants.env import DB_ID
from src.infrastructure.notion import notion
from dataclasses import dataclass
from src.infrastructure.groq import groq_chat
from langchain_core.prompts import ChatPromptTemplate


@dataclass
class JobOffer:
    apply_url: Optional[str]
    company_hq: Optional[str]
    date_scrapped: Optional[str]
    details: Optional[str]
    id: Optional[int]
    name: Optional[str]
    remote: Optional[str]
    startup: Optional[str]
    status: Optional[str]
    vertical: Optional[str]


def job_raw_to_obj(raw_job: Dict[str, Any]) -> JobOffer:
    return JobOffer(
        apply_url=raw_job.get("properties", {}).get("Apply URL", {}).get("url"),
        company_hq=raw_job.get("properties", {})
        .get("Company HQ", {})
        .get("rich_text", [{}])[0]
        .get("plain_text"),
        date_scrapped=raw_job.get("properties", {})
        .get("Date Scrapped", {})
        .get("created_time"),
        details=raw_job.get("properties", {})
        .get("Details", {})
        .get("rich_text", [{}])[0]
        .get("plain_text"),
        id=raw_job.get("properties", {})
        .get("ID", {})
        .get("unique_id", {})
        .get("number"),
        name=raw_job.get("properties", {})
        .get("Name", {})
        .get("title", [{}])[0]
        .get("plain_text"),
        remote=raw_job.get("properties", {})
        .get("Remote", {})
        .get("select", {})
        .get("name"),
        startup=raw_job.get("properties", {})
        .get("Startup", {})
        .get("rich_text", [{}])[0]
        .get("plain_text"),
        status=raw_job.get("properties", {})
        .get("Status", {})
        .get("status", {})
        .get("name"),
        vertical=raw_job.get("properties", {})
        .get("Vertical", {})
        .get("select", {})
        .get("name"),
    )


def job_summarize_description(description: str):
    system = "You are an expert human resources specialist"
    human = "{text}"
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
    chain = prompt | groq_chat
    response = chain.invoke(
        {
            "text": f"""
    summarize #JOBOFFER
    {description}
    """
        }
    )

    return response.content


async def jobs_get_by_status(status: Literal["In Review", "Aproved"]):
    query = cast(
        dict,
        notion.databases.query(
            **{
                "database_id": DB_ID,
                "filter": {
                    "and": [
                        {
                            "property": "Status",
                            "status": {
                                "equals": status,
                            },
                        },
                        {
                            "property": "Apply URL",
                            "url": {
                                "is_not_empty": True,
                            },
                        },
                    ]
                },
            }
        ),
    )

    results = query["results"]
    jobs = [job_raw_to_obj(r) for r in results]
    return jobs
