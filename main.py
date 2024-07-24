from fastapi import FastAPI

import logging
import sys
from contextlib import asynccontextmanager
from typing import Any
from aiogram import types

from src.config import WEBHOOK_PATH
from src.bot.bot_main import dp, bot
from src.lifespan import set_webhook, ngrok_close, ngrok_run
from src.server.ctch_dt.bouquet.router_bouquet import router as router_bouquet
from src.server.ctch_dt.flower.router_flower import router as router_flower


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.info("lifespan run")
    ngrok_run()
    await set_webhook(_app)
    _app.include_router(router_bouquet)
    _app.include_router(router_flower)
    yield
    await bot.session.close()
    ngrok_close()
    logging.info("bot session close")


app = FastAPI(lifespan=lifespan)


@app.post(WEBHOOK_PATH, tags=["Bot"])
async def webhook(update: dict[str, Any]) -> None:
    await dp.feed_webhook_update(bot=bot, update=types.Update(**update))
