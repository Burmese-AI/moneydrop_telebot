from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext._contexttypes import ContextTypes


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
    await context.bot.send_message(
        update.callback_query.message.chat.id, f"You are {query.data}!"
    )