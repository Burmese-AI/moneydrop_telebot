from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext._contexttypes import ContextTypes


CHECK_CHAR = "✅"
UNCHECK_CHAR = "⬜"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("starting...")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(UNCHECK_CHAR + "Choice1", callback_data="Choice1"),
            InlineKeyboardButton(UNCHECK_CHAR + "Choice2", callback_data="Choice2"),
        ],
        [
            InlineKeyboardButton(UNCHECK_CHAR + "Choice3", callback_data="Choice3"),
            InlineKeyboardButton(UNCHECK_CHAR + "Choice4", callback_data="Choice4"),
        ],
        [
            InlineKeyboardButton("Submit", callback_data="Submit"),
        ],
    ]
    kb_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Answer this question!", reply_markup=kb_markup)


async def choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "Submit":
        await context.bot.send_message(query.message.chat.id, f"Submitted!")
    else:
        new_keyboard = []
        for i in query.message.reply_markup.inline_keyboard:
            kb_row = []
            for kb in i:
                new_text = kb.text
                if kb.callback_data == query.data:
                    if kb.text.startswith(CHECK_CHAR):
                        new_text = UNCHECK_CHAR + kb.text[1:]
                    else:
                        new_text = CHECK_CHAR + kb.text[1:]
                kb_row.append(
                    InlineKeyboardButton(new_text, callback_data=kb.callback_data)
                )
            new_keyboard.append(kb_row)
        await context.bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=query.message.text,
            reply_markup=InlineKeyboardMarkup(new_keyboard),
        )
