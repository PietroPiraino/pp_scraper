import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
BETALAND_USERNAME = os.getenv("BETALAND_USERNAME")
BETALAND_PASSWORD = os.getenv("BETALAND_PASSWORD")