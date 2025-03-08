from typing import TypedDict, cast

from src.domain.scrappers.base import OfferData
from src.providers.constants.env import DB_ID
from src.providers.notion.notion import notion


class Status(TypedDict):
  name: str
  color: str


class PositionsDS:
  @staticmethod
  def status_get_all(database: dict):
    return cast(list, database["properties"]["Status"]["status"]["options"])

  @staticmethod
  def vertical_get_all(database: dict):
    return cast(list, database["properties"]["Vertical"]["select"]["options"])

  @staticmethod
  def remote_get_all(database: dict):
    return cast(list, database["properties"]["Remote"]["select"]["options"])

  @staticmethod
  def status_find(status_options: list, status: str):
    return next((opt for opt in status_options if opt["name"] == status), None)

  @staticmethod
  def vertical_find(options: list, vertical: str):
    return next((opt for opt in options if opt["name"] == vertical), None)

  @staticmethod
  def remote_find(options: list, remote: str):
    return next((opt for opt in options if opt["name"] == remote), None)

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
    id = next(opt["id"] for opt in PositionsDS.status_get_all(database) if opt["name"] == status["name"])

    return id

  @staticmethod
  def vertical_list_add(vertical: dict[str, str]):
    database = cast(dict, notion.databases.retrieve(database_id=DB_ID))
    options = PositionsDS.vertical_get_all(database)
    data = options + [vertical]

    notion.databases.update(
      database_id=DB_ID,
      properties={"Vertical": {"select": {"options": data}}},
    )

    database = cast(dict, notion.databases.retrieve(database_id=DB_ID))
    id = next(opt["id"] for opt in PositionsDS.vertical_get_all(database) if opt["name"] == vertical["name"])

    return id

  @staticmethod
  def status_id_get_or_create(status: str):
    database = cast(dict, notion.databases.retrieve(database_id=DB_ID))
    status_options = PositionsDS.status_get_all(database)
    existing_status = PositionsDS.status_find(status_options, status)

    return existing_status["id"] if existing_status else PositionsDS.status_list_add({"name": status, "color": "default"})

  @staticmethod
  def vertical_get_or_create(vertical: str):
    database = cast(dict, notion.databases.retrieve(database_id=DB_ID))
    options = PositionsDS.vertical_get_all(database)
    vertical_found = PositionsDS.vertical_find(options, vertical)

    return vertical_found["id"] if vertical_found else PositionsDS.vertical_list_add({"name": vertical, "color": "default"})

  @staticmethod
  def remote_get(remote: str):
    database = cast(dict, notion.databases.retrieve(database_id=DB_ID))
    options = PositionsDS.remote_get_all(database)
    remote_found = PositionsDS.remote_find(options, remote)
    if remote_found == None:
      return cast(dict, PositionsDS.remote_find(options, "Hybrid"))["id"]
    return remote_found["id"]

  @staticmethod
  def offer_to_notion(offer: OfferData):
    status_id = PositionsDS.status_id_get_or_create("Scraped")
    vertical_id = PositionsDS.vertical_get_or_create(offer.vertical)
    remote_id = PositionsDS.remote_get(offer.remote)

    return {
      "Status": {
        "status": {
          "id": status_id,
        },
      },
      "Remote": {
        "select": {
          "id": remote_id,
        },
      },
      "Startup": {
        "rich_text": [
          {
            "text": {"content": offer.company_name},
          }
        ],
      },
      "Location": {
        "rich_text": [
          {
            "text": {"content": offer.location},
          }
        ],
      },
      "Apply URL": {"url": offer.apply_url},
      "Summary": {
        "rich_text": [
          {
            "text": {"content": offer.details},
          }
        ],
      },
      "Date Scrapped": {"date": {"start": offer.date_scraped, "end": None}},
      "Vertical": {
        "select": {
          "id": vertical_id,
        },
      },
      "Role": {
        "title": [
          {
            "text": {"content": offer.role},
          }
        ],
      },
    }

  @staticmethod
  def position_create(offer: OfferData):
    data = PositionsDS.offer_to_notion(offer)
    notion.pages.create(parent={"database_id": DB_ID}, properties=data)
