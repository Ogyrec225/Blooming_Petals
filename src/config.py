import requests
from dotenv import load_dotenv
import os
import ngrok


load_dotenv()

TOKEN = os.environ.get("TOKEN")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
WEBHOOK_PATH = os.environ.get("WEBHOOK_PATH")
WEB_SERVER_HOST = os.environ.get("WEB_SERVER_HOST")
WEB_SERVER_PORT = os.environ.get("WEB_SERVER_PORT")
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET")

NGROK_TOKEN = os.environ.get("NGROK_TOKEN")