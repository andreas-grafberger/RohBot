import pytest
import responses
from intents.WeatherIntent import WeatherIntent as WI
from Utils import loadOWMToken
from telegram import Bot
from mock import Mock, patch


class TestWeatherIntent(object):

    def initRequestMockup(self):
        # Mockup data
        data = {'q': 'Munich', 'units': 'metric', 'APPID': loadOWMToken()}
        response = {'name': 'Munich', 'weather': [{'description': 'cloud'}], 'main': {'temp': 30.2}}

        responses.add(responses.GET, WI.weatherUrl,
                      headers=data, json=response, status=200)
        return response

    def initRequestMockupForInvalidLocation(self):
        # Mockup data
        data = {'q': 'ThisIsNoValidLocation', 'units': 'metric', 'APPID': loadOWMToken()}
        response = {'Error': 'Location not found!'}

        responses.add(responses.GET, WI.weatherUrl,
                      headers=data, json=response, status=404)
        return response

    def test_formatMessage(self):
        data = {
            'name': 'Munich',
            'weather': [{'description': 'beautiful sky'}],
            'main': {'temp': 10}
        }
        message = WI.formatMessage(data)
        assert message == "In Munich there is a beautiful sky and it has 10 degrees celcius."

    @responses.activate
    def test_createResponse(self):
        response = self.initRequestMockup()

        res = WI.createResponse('Munich')
        assert (res == response)

    @responses.activate
    def test_callAndFormat(self):
        self.initRequestMockup()

        weatherData = WI.createResponse('Munich')
        answer = WI.formatMessage(weatherData)

        assert (answer == "In Munich there is a cloud and it has 30.2 degrees celcius.")

    @responses.activate
    @patch('telegram.Bot.send_message')
    def test_executeWithValidLocation(self, BotMock):
        self.initRequestMockup()

        WI.execute('What is the weather in Munich?', 123)

        BotMock.assert_called_once_with(123, "In Munich there is a cloud and it has 30.2 degrees celcius.")

    @responses.activate
    @patch('telegram.Bot.send_message')
    def test_executeWithInvalidLocation(self, BotMock):
        self.initRequestMockupForInvalidLocation()

        WI.execute('What is the weather in ThisIsNoValidLocation?', 123)

        BotMock.assert_called_once_with(123, "Error handling your request. Api-Call limit exceeded or invalid location.")