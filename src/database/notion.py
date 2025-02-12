from notion_database.database import Database
from src.constants.env import NOTION_KEY, DB_ID

D = Database(integrations_token=NOTION_KEY)
D.retrieve_database(database_id=DB_ID)
