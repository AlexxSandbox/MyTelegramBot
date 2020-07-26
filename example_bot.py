import os

import requests
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_ID')


updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispather = updater.dispatcher


# действие на команду /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='I am bot, please talk to me!')


start_handler = CommandHandler('start', start)
dispather.add_handler(start_handler)
updater.start_polling()


# ответ на сообщение от пользователя - эхо
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=update.message.text)


echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispather.add_handler(echo_handler)


# выводим введеный текс в верхнем регистре
def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


caps_handler = CommandHandler('caps', caps)
dispather.add_handler(caps_handler)


# отвечаем на незвестные команды
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Моя твоя не понимать!')


unknown_handler = MessageHandler(Filters.command, unknown)
dispather.add_handler(unknown_handler)


updater.idle()