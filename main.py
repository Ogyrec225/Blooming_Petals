import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.bot.bot_main import dp, bot
from src.server.ctch_dt.router import router as router_bouquet
from src.bot.bot_main import router as router_bot

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("lifespan")
    await dp.start_polling(bot)
    logging.info("bot start")
    yield
    await dp.stop_polling(bot)



app = FastAPI(lifespan=lifespan)




# @app.post("/webhook")
# async def webhook(request: Request):
#     logging.info("Получен json file")
#     update = Update.model_validate(await request.json(), context={"bot": bot})
#     await dp.feed_update(update)
#     return {"status": "ok"}


app.include_router(router_bouquet)
app.include_router(router_bot)
