from notion_client import Client

from src.providers.constants.env import NOTION_KEY

notion = Client(auth=NOTION_KEY)
