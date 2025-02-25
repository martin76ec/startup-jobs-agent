from typing import TypedDict, cast
from src.constants.env import DB_ID
from src.domain.jobs import JobOffer
from src.infrastructure.notion import notion
from src.scrapers.base import OfferData


class Status(TypedDict):
    name: str
    color: str


class PositionsDS:
    @staticmethod
    def status_get_all(database: dict):
        return cast(list, database["properties"]["Status"]["status"]["options"])

    @staticmethod
    def status_find(status_options: list, status: str):
        return next((opt for opt in status_options if opt["name"] == status), None)

    @staticmethod
    def status_list_add(status: Status):
        database = cast(dict, notion.databases.retrieve(database_id=DB_ID))
        options = PositionsDS.status_get_all(database)
        data = options + [status]

        notion.databases.update(
            database_id=DB_ID,
            properties={"Status": {"status": {"options": data}}},
        )

        database = cast(dict, notion.databases.retrieve(database_id=DB_ID))
        id = next(
            opt["id"]
            for opt in PositionsDS.status_get_all(database)
            if opt["name"] == status["name"]
        )

        return id

    @staticmethod
    def status_id_get_or_create(status: Status):
        database = cast(dict, notion.databases.retrieve(database_id=DB_ID))
        status_options = PositionsDS.status_get_all(database)
        existing_status = PositionsDS.status_find(status_options, status["name"])

        return (
            existing_status["id"]
            if existing_status
            else PositionsDS.status_list_add(status)
        )

    @staticmethod
    def position_create(offer: OfferData):
        # status: Status = {"name": "Scraped", "color": ""}
        # status_id = PositionsDS.status_id_get_or_create(status)
        status_id = "123123213"

        # data = {
        #     "Role": {
        #         "text": { "content": "test" } },
        #     "Location": "test",
        #     "Summary": "test",
        #     "Vertical": "test",
        #     "Apply URL": "test",
        #     "Location": "test",
        #     "Summary": "test",
        #     "Status": {"id": status_id},
        # }
        #
        data = {
            "parent": {
                "database_id": "your_database_id"
            },  # Replace with your actual database ID
            "properties": {
                "Role": {"title": [{"text": {"content": "test"}}]},
                "Location": {"rich_text": [{"text": {"content": "test"}}]},
                "Summary": {"rich_text": [{"text": {"content": "test"}}]},
                "Vertical": {"rich_text": [{"text": {"content": "test"}}]},
                "Apply URL": {"url": "test"},
                "Status": {
                    "status": {
                        "id": status_id
                    }  # Ensure `status_id` is a valid Notion status ID
                },
            },
        }
        breakpoint()

        notion.pages.create(parent={"database_id": DB_ID}, properties=data)
