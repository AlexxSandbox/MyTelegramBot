import os

import requests
import telegram
import json
import datetime
from time import sleep

from dotenv import load_dotenv
from pprint import pprint


load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_ID')
# TIMEZONE = 'Asia/Yekaterinburg'
# TIMEZONE_COMMON_NAME = 'Yekaterinburg'
TELEGRAM_URL = 'https://api.telegram.org/bot{}/{}'


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.url = TELEGRAM_URL

    def get_updates(self, timeout=30, offset=-1):
        method = 'getUpdates'
        url = self.url.format(self.token, method)
        params = {'timeout': timeout, 'offset': offset}
        response = requests.get(url, params=params)
        result_json = response.json()['result']
        return result_json

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]
        return last_update

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        url = self.url.format(self.token, method)
        response = requests.post(url, params=params)
        return response

    def weather(self):
        url = 'http://ru.wttr.in/?0T'
        response = requests.get(url)
        return response.text


greet_bot = BotHandler(TELEGRAM_TOKEN)
greetings = ('hello', 'hi', 'greetings', 'sup')
request_weather = ('what weather', 'weather')
now = datetime.datetime.now()


def main():
    # new_offset = None
    today = now.day
    hour = now.hour
    last_update_id = greet_bot.get_last_update()['update_id']

    while True:
        # greet_bot.get_updates()
        last_update = greet_bot.get_last_update()

        update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']

        if update_id != last_update_id:
            if last_chat_text.lower() in greetings and today == now.day and 6 <= hour < 12:
                greet_bot.send_message(last_chat_id, 'Good Morning {}'.format(last_chat_name))
                # today += 1

            elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
                greet_bot.send_message(last_chat_id, 'Good Afternoon {}'.format(last_chat_name))
                # today += 1

            elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
                greet_bot.send_message(last_chat_id, 'Good evening {}'.format(last_chat_name))
                # today += 1

            elif last_chat_text.lower() in request_weather:
                weather = greet_bot.weather()
                greet_bot.send_message(last_chat_id, '{}'.format(weather))

            else:
                greet_bot.send_message(last_chat_id, 'Моя твоя не понимать {}'.format(last_chat_name))

            # new_offset = update_id + 1
            last_update_id = update_id
            sleep(5)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()