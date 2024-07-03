from contextlib import asynccontextmanager
from http import HTTPStatus
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from fastapi import FastAPI, Request, Response
from config import settings

import handlers


ptb = (
    Application.builder()
    .updater(None)
    .token(settings.bot_token)
    .read_timeout(7)
    .get_updates_read_timeout(42)
    .build()
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await ptb.bot.setWebhook(settings.webhook_url)
    async with ptb:
        await ptb.start()
        yield
        await ptb.stop()


app = FastAPI(lifespan=lifespan)


@app.post("/")
async def process_update(request: Request):
    req = await request.json()
    update = Update.de_json(req, ptb.bot)
    await ptb.process_update(update)
    return Response(status_code=HTTPStatus.OK)


ptb.add_handler(CommandHandler("start", handlers.start))
ptb.add_handler(MessageHandler(filters.ALL, handlers.echo))
ptb.add_handler(CallbackQueryHandler(handlers.choice))
