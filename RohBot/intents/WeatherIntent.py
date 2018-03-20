import spacy

from BotConnector import BotConnector
from Intent import Intent
import requests
from Utils import loadOWMToken
import NLPUtils


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

    owmToken = loadOWMToken()

    @classmethod
    def getWeatherData(cls, location):
        data = {'q': location, 'units': 'metric', 'APPID': cls.owmToken}
        r = requests.get(cls.weatherUrl, data)
        if r.status_code != 200:
            return None
        return r.json()

    @classmethod
    def formatMessage(cls, data):
        ioData = {
            'name': data['name'],
            'description': data['weather'][0]['description'],
            'temp': data['main']['temp']
        }
        return "In {name} there is a {description} and it has {temp} degrees celcius.".format(**ioData)

    @classmethod
    def createResponse(cls, str):
        location = NLPUtils.extractEntity(str, 'GPE', removeWords=["weather"])
        data = WeatherIntent.getWeatherData(location)
        return data

    @classmethod
    def execute(cls, str, chat_id):
        data = WeatherIntent.createResponse(str)
        bot = BotConnector.getInstance()
        if data is None:
            bot.send_message(chat_id,
                             "Error handling your request. Api-Call limit exceeded or invalid location.")  # TODO: Differentiate different failures
        else:
            bot.send_message(chat_id, WeatherIntent.formatMessage(data))
