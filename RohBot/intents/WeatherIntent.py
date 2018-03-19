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
    def extractLocation(message):
        nlp = spacy.load('en')
        doc = nlp(unicode(message))
        locs = [ent.text for ent in doc.ents if ent.label_ == 'GPE' and ent.text.lower() != 'weather']
        return locs[0]

    @staticmethod
    def getWeatherData(location):
        appid = loadOWMToken()
        if appid is None:
            return None
        data = {'q':location, 'units': 'metric','APPID':appid}
        r = requests.get(WeatherIntent.weatherUrl, data)
        if r.status_code != 200:
            return None
        return r.json()

    @staticmethod
    def createMessage(data):
        ioData = {
            'name': data['name'],
            'description': data['weather'][0]['description'],
            'temp': data['main']['temp']
        }
        return "In {name} there is a {description} and it has {temp} degree celcius".format(**ioData)

    @staticmethod
    def execute(str, chat_id):
        # type: (object, object, object) -> object
        location = extractEntity(str, 'GPE', removeWords=["weather"])
        if location is None:
            return None
        data = WeatherIntent.getWeatherData(location)
        bot = BotConnector.getInstance()
        if data is None:
            bot.send_message(chat_id, "Weather Service can not be accessed right now.")
        else:
            bot.send_message(chat_id, WeatherIntent.createMessage(data))
