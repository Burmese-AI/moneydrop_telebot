from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext._contexttypes import ContextTypes
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from config import settings
from telegram.ext import ConversationHandler

import crud, models, schemas, constants


CHECK_CHAR = "✅"
UNCHECK_CHAR = "⬜"

models.Base.metadata.create_all(bind=engine)


async def create_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == settings.admin_id:
        context.user_data["field_names"] = ["name"]
        await update.message.reply_text(f"Enter {context.user_data['field_names'][0]}")
        return constants.INPUT
    else:
        await update.message.reply_text("You're not admin!")


async def input_state(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == settings.admin_id:
        field_name = context.user_data["field_names"].pop(0)
        context.user_data[field_name] = update.message.text
        if context.user_data["field_names"]:
            next_field = context.user_data["field_names"][0]
            await update.message.reply_text(f"Enter {next_field}")
            return constants.INPUT
        else:
            print("Got all fields!", context.user_data)
            context.user_data.clear()
            await update.message.reply_text("Operation completed!")
            return ConversationHandler.END
    else:
        await update.message.reply_text("You're not admin!")


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("Operation canceled!")
    return ConversationHandler.END


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    categories = crud.get_categories(db)
    for c in categories:
        print(c)
    db.close()
    await update.message.reply_text("starting...")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(context.user_data["hello"])
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
