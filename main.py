import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.bot.bot_main import dp, bot
from src.config import WEBHOOK_URL
from src.server.ctch_dt.router import router as router_bouquet
from src.bot.bot_main import router as router_bot

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("lifespan")
    bot.set_webhook(WEBHOOK_URL)
    logging.info(f"bot start, {await bot.get_webhook_info()}")
    yield
    await bot.session.close()



app = FastAPI(lifespan=lifespan)




# @app.post("/webhook")
# async def webhook(request: Request):
#     logging.info("Получен json file")
#     update = Update.model_validate(await request.json(), context={"bot": bot})
#     await dp.feed_update(update)
#     return {"status": "ok"}


app.include_router(router_bouquet)
app.include_router(router_bot)

