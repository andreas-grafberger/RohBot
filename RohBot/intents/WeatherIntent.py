import spacy

from BotConnector import BotConnector
from Intent import Intent
import requests
from Utils import loadOWMToken
from NLPUtils import extractEntity


class WeatherIntent(Intent):
    weatherUrl = 'http://api.openweathermap.org/data/2.5/weather'
    keywords = ['weather', 'hot', 'cold', 'rain', 'sun']
    utterances = ["What is the weather in %s?",
                  "What's the weather in %s?",
                  "What is the weather like in %s?",
                  "What's the weather like in %s?",
                  "How hot is it in %s?",
                  "How cold is it in %s?",
                  "Does it rain in %s?",
                  ]

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
