from contextlib import asynccontextmanager
from http import HTTPStatus
from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from telegram.ext._contexttypes import ContextTypes
from fastapi import FastAPI, Request, Response
from config import settings


# Initialize python telegram bot
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


# Initialize FastAPI app
app = FastAPI(lifespan=lifespan)


@app.post("/")
async def process_update(request: Request):
    req = await request.json()
    update = Update.de_json(req, ptb.bot)
    await ptb.process_update(update)
    return Response(status_code=HTTPStatus.OK)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("starting...")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Correct", callback_data="Correct"),
            InlineKeyboardButton("Wrong", callback_data="Wrong"),
        ],
        [
            InlineKeyboardButton("Wrong", callback_data="Wrong"),
            InlineKeyboardButton("Wrong", callback_data="Wrong"),
        ],
    ]
    kb_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Answer this question!", reply_markup=kb_markup)


async def choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await ptb.bot.send_message(
        update.callback_query.message.chat.id, f"You are {query.data}!"
    )


ptb.add_handler(CommandHandler("start", start))
ptb.add_handler(MessageHandler(filters.ALL, echo))
ptb.add_handler(CallbackQueryHandler(choice))
