from intents.Intent import Intent
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

    @staticmethod
    def getWeatherData(location):
        data = {'q':location, 'units': 'metric','APPID':loadOWMToken()}
        r = requests.get(WeatherIntent.weatherUrl, data)
        if r.status_code != 200:
            return None
        return r.json()

    @staticmethod
    def execute(str, bot, chat_id):
        # type: (object, object, object) -> object
        location = WeatherIntent.filterKeyWords(str)[0]
        data = WeatherIntent.getWeatherData(location)
        ioData = {
            'name': data['name'],
            'description': data['weather'][0]['description'],
            'temp': data['main']['temp']
        }
        message = "In {name} there is a {description} and it has {temp} degree celcius".format(**ioData)
        bot.send_message(chat_id, message)
