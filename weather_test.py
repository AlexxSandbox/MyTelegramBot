import requests
import json
from pprint import pprint

def weather(city):
    url = 'http://wttr.in/{}?format=j1&lang=ru'
    weather = requests.get(url.format(city)).json()
    # temperature = weather['current_condition']['temp_C']
    # result = f'Сегодня {temperature} градусов'
    # pprint(weather['nearest_area'])
    # pprint(weather['current_condition'])
    pprint(weather)

def gismeteo():
    token = '56b30cb255.3443075'
    url = 'https://api.gismeteo.net/v2/weather/current/?latitude=54.35&longitude=52.52'
    headers = {'X-Gismeteo-Token': token}
    response = requests.get(url, headers=headers).json()
    pprint(response)