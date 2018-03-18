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

    def test_filterKeyWords(self):
        params = WI.filterKeyWords("Wetter  ")
        assert(params, [])

    def test_filterKeyWords_one(self):
        params = WI.filterKeyWords("Wetter Berg")
        assert(params, ["Berg"])

    def test_filterKeyWords_more(self):
        params = WI.filterKeyWords("Berg Strasse Wetter Haus")
        assert(params, ["Berg", "Strasse", "Haus"])

    def test_filterKeyWords_none(self):
        params = WI.filterKeyWords("Berg")
        assert (params, None)