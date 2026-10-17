import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

ADMIN_IDS_STR = os.getenv("ADMIN_IDS", "123456789")
ADMIN_IDS = [int(i.strip()) for i in ADMIN_IDS_STR.split(",") if i.strip()]

# Kino/serial kanalining ID si (baza kanal)
# Misol: -1001234567890
BASE_CHANNEL_ID = os.getenv("BASE_CHANNEL_ID", "-1001234567890")

DB_PATH = "database/kino_bot.db"
