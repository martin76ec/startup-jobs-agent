from src.constants.env import DB_ID
from src.infrastructure.notion import notion


async def jobs_get():
    job_list = notion.databases.query(
        **{
            "database_id": DB_ID,
            "filter": {
                "property": "Status",
                "rich_text": {
                    "equals": "In Review",
                },
            },
        }
    )

    return job_list
