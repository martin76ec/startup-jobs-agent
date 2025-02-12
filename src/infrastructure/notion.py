from src.constants.env import NOTION_KEY
from notion_client import Client

notion = Client(auth=NOTION_KEY)
