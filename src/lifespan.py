import logging

from pyngrok import ngrok
from fastapi import FastAPI

from src.config import NGROK_TOKEN, WEBHOOK_URL, WEB_SERVER_PORT


def ngrok_run() -> str:
    ngrok.set_auth_token(NGROK_TOKEN)
    public_url = ngrok.connect(WEB_SERVER_PORT, domain=WEBHOOK_URL[8:]).public_url
    logging.info(f"\nNgrok start via url: {public_url}, port: {WEB_SERVER_PORT}")
    return public_url


def ngrok_close():
    ngrok.disconnect(WEBHOOK_URL[8:])
    logging.info(f"\nNgrok stop via url: {WEBHOOK_URL[8:]}, port: {WEB_SERVER_PORT}")


async def set_webhook(_app: FastAPI):
    from src.config import WEBHOOK_URL, WEBHOOK_PATH, WEBHOOK_SECRET
    from src.bot.bot_main import bot

    if f"{WEBHOOK_URL}{WEBHOOK_PATH}" != await bot.get_webhook_info():
        await bot.set_webhook(f"{WEBHOOK_URL}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET)


    logging.info(f"\nBot start, {await bot.get_webhook_info()}")