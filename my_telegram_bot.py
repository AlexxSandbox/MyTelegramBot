import os

import requests
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
# CHAT_ID = os.getenv('TELEGRAM_ID')


def start(update, context):
    user_name = update.effective_user['first_name']
    update.message.reply_text(f'Привет, {user_name}, я бот. Напиши мне и я '
                              f'постараюсь тебе помочь. Чтобы узнать, '
                              f'что я умею набери /help.')


def help(update, context):
    update.message.reply_text('Вот что я умею!\n'
                              'Чтобы узнать погоду, набери /weather и добавь '
                              'город. Например /weather Тюмень.\n'
                              'Чтобы узнать текущий курс валют, набери /currency.')


def weather(update, context):
    city_request = ' '.join(context.args).capitalize()
    url = 'http://wttr.in/{}?format=j1&lang=ru'
    response = requests.get(url.format(city_request)).json()

    # city_response = response['nearest_area'][0]['region'][0]['value']
    weather_today = response['current_condition'][0]['lang_ru'][0]['value'].lower()
    temperature_feels = response['current_condition'][0]['FeelsLikeC']
    humidity_today = response['current_condition'][0]['humidity']
    wind_today = response['current_condition'][0]['windspeedKmph']

    result = f'Сейчас на улице {weather_today}.\n' \
             f'Температура по ощущениям: {temperature_feels}℃.\n' \
             f'Влажность: {humidity_today}%.\n' \
             f'Скорость ветра: {wind_today} км/ч.'

    update.message.reply_text(result)


def currency(update, context):
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    response = requests.get(url).json()
    usd_currency = response['Valute']['USD']['Value']
    eur_currency = response['Valute']['EUR']['Value']
    currency_date = response['Date'].split('T')[0]
    result = f'Курс валют на {currency_date}.\n' \
             f'1 USD={usd_currency:.2f} руб.\n' \
             f'1 EUR={eur_currency:.2f} руб.'

    update.message.reply_text(result)


def unknown(update, context):
    update.message.reply_text('Моя твоя не понимать, набери /help, чтобы понимать.')


def echo(update, context):
    user_message = update.message.text
    update.message.reply_text(f'Сам такой: {user_message}')


def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispather = updater.dispatcher

    dispather.add_handler(CommandHandler('start', start))
    dispather.add_handler(CommandHandler('help', help))
    dispather.add_handler(CommandHandler('weather', weather))
    dispather.add_handler(CommandHandler('currency', currency))
    dispather.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))
    dispather.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling(poll_interval=5)
    updater.idle()


if __name__ == '__main__':
    main()
