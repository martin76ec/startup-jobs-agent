import os
from typing import cast

from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()

# NOTION
DB_ID: str = os.getenv("DB_ID") or "default"
NOTION_KEY: str = os.getenv("NOTION_KEY") or "default"

# LINKEDIN
LINKEDIN_EMAIL: str = os.getenv("LINKEDIN_EMAIL") or "default"
LINKEDIN_PASSWORD: str = os.getenv("LINKEDIN_PASSWORD") or "default"

# CHROME
CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH") or "default"
CHROME_BINARY_PATH = os.getenv("CHROME_BINARY_PATH") or "default"

# GROQ
GROQ_KEY = cast(SecretStr, os.getenv("GROQ_KEY") or "default")

# GENAI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or "default"

# FIRECRAWL
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY" or "default")
