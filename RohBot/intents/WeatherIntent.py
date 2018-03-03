from Intent import Intent
import requests
from RohBot.Utils import loadOWMToken
import json


class WeatherIntent(Intent):

    weatherUrl = 'http://api.openweathermap.org/data/2.5/weather'
    keywords = ['Wetter']

    @staticmethod
    def filterKeyWords(str):
        split = str.split(' ')
        for keyword in WeatherIntent.keywords:
            if keyword not in split:
                return None
            else:
                split.remove(keyword)
        return split # params will be returned

    def getWeatherData(self, location):
        appid = loadOWMToken()
        if appid is None:
            return None
        data = {'q':location, 'units': 'metric','APPID':appid}
        r = requests.get(WeatherIntent.weatherUrl, data)
        if r.status_code != 200:
            return None
        return r.json()

    def createMessage(self, data):
        ioData = {
            'name': data['name'],
            'description': data['weather'][0]['description'],
            'temp': data['main']['temp']
        }
        return "In {name} there is a {description} and it has {temp} degree celcius".format(**ioData)

    @staticmethod
    def execute(str, bot, chat_id):
        # type: (object, object, object) -> object
        location = WeatherIntent.filterKeyWords(str)[0]
        if location is None:
            return None
        data = WeatherIntent.getWeatherData(location)
        if data is None:
            bot.send_message(chat_id, "Weather Service can not be accessed right now.")
        else:
            bot.send_message(chat_id, WeatherIntent.createMessage(data))
