from time import strftime
from typing import Any, Dict, Literal, Optional, cast
from typing_extensions import Annotated

from pydantic import BaseModel, Field
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
    name: Optional[str]
    remote: Optional[str]
    startup: Optional[str]
    status: Optional[str]
    vertical: Optional[str]


class JobOfferStruct(BaseModel):
    company_hq: str = Field(
        default="",
        description="the city and country of the offer in format: City, Country",
    )
    details: str = Field(
        default="", description="the details in markdown about the job"
    )
    name: str = Field(default="", description="the role of the position")
    remote: str = Field(
        default="", description="the type of job, remote, hybrid or presential"
    )
    startup: str = Field(
        default="", description="the name of the company that makes the offer"
    )
    vertical: str = Field(
        default="",
        description="The area of work (e.g Data, Engineering, Marketing[str,)",
    )


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
    system = "You are an expert human resources specialist, you are native in english and spanish, and you translate summarize and translate to spanish the job offer"
    human = "{text}"
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
    model = groq_chat.with_structured_output(JobOfferStruct)
    chain = prompt | model
    response = chain.invoke(
        {
            "text": f"""
    summarize #JOBOFFER
    {description}
    """
        }
    )

    return response


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
