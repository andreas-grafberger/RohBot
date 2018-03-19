import spacy

from BotConnector import BotConnector
from Intent import Intent
import requests
from Utils import loadOWMToken
import json
from NLPUtils import extractEntity


class WeatherIntent(Intent):

    weatherUrl = 'http://api.openweathermap.org/data/2.5/weather'
    keywords = ['Wetter', 'weather']

    @staticmethod
    def filterKeyWords(str):
        split = str.split(' ')
        for keyword in WeatherIntent.keywords:
            if keyword not in split:
                return None
            else:
                split.remove(keyword)
        return split # params will be returned

    @staticmethod
    def getWeatherData(location, appid=loadOWMToken()):
        data = {'q': location, 'units': 'metric', 'APPID': appid}
        r = requests.get(WeatherIntent.weatherUrl, data)
        if r.status_code != 200:
            return None
        return r.json()

    @staticmethod
    def formatMessage(data):
        ioData = {
            'name': data['name'],
            'description': data['weather'][0]['description'],
            'temp': data['main']['temp']
        }
        return "In {name} there is a {description} and it has {temp} degrees celcius.".format(**ioData)

    @staticmethod
    def createResponse(str):
        location = extractEntity(str, 'GPE', removeWords=["weather"])
        data = WeatherIntent.getWeatherData(location)
        return data

    @staticmethod
    def execute(str, chat_id):
        data = WeatherIntent.createResponse(str)
        bot = BotConnector.getInstance()
        if data is None:
            bot.send_message(chat_id,
                             "Error handling your request. Api-Call limit exceeded or invalid location.")  # TODO: Differentiate different failures
        else:
            bot.send_message(chat_id, WeatherIntent.formatMessage(data))
