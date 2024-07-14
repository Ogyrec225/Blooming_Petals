from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.environ.get("TOKEN")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
WEBHOOK_PATH = os.environ.get("WEBHOOK_PATH")

# import json
#
# with open("config.json") as f:
#     data = json.load(f)
#     print(data)
#     TOKEN = data["TOKEN"]
#     DB_USER=data["DB_USER"]
#     DB_PASS=data["DB_PASS"]
#     DB_HOST=data["DB_HOST"]
#     DB_PORT=data["DB_PORT"]
#     DB_NAME=data["DB_NAME"]
#
#     WEBHOOK_URL=data["WEBHOOK_URL"]
#     WEBHOOK_PATH=data["WEBHOOK_PATH"]
