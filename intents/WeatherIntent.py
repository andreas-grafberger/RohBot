from intents.Intent import Intent
import requests
from Utils import loadOWMToken


class WeatherIntent(Intent):

    weatherUrl = 'http://api.openweathermap.org/data/2.5/weather?'
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
    def getWeather(location):
        data = {'location': location, 'APPID': loadOWMToken()}
        r = requests.get(WeatherIntent.weatherUrl, str(data))
        return r

    @staticmethod
    def execute(str, bot, chat_id):
        # type: (object, object, object) -> object
        location = WeatherIntent.filterKeyWords(str)[0]
        print (WeatherIntent.getWeather(location))
        return ""

WeatherIntent.execute("Wetter Augsburg", None, None);