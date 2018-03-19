import pytest
from intents.WeatherIntent import WeatherIntent as WI


class TestWeatherIntent(object):

    def test_createMessage(self):
        data = {
            'name': 'Munich',
            'weather': [{'description': 'beautiful sky'}],
            'main': {'temp': 10}
        }
        message = WI.createMessage(data)
        assert(message, "In Munich there is a beautiful sky an it has 10 degrees celcius.")

