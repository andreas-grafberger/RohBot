import pytest
from mock import patch, Mock
import responses
import intents.WeatherIntent as WI
from telegram import Bot


class TestWeatherIntent(object):

    @pytest.yield_fixture(autouse=True)
    def changeOWMToken(self):
        # Before test
        oldToken = WI.owmToken
        WI.owmToken = "1234"
        # A test function will be run at this point
        yield
        # Code that will run after your test, for example:
        WI.owmToken = oldToken
        assert oldToken == WI.owmToken

    def initRequestMockup(self):
        # Mockup data
        query = "?q=munich&units=metric&APPID=1234"
        response = {'name': 'Munich', 'weather': [{'description': 'cloud'}], 'main': {'temp': 30.2}}

        responses.add(responses.GET, WI.weatherUrl + query,
                      json=response, status=200,
                      match_querystring=True)
        return response

    def initRequestMockupForInvalidLocation(self):
        # Mockup data
        query = "?units=metric&APPID=1234"
        response = {'Error': 'Location not found!'}

        responses.add(responses.GET, WI.weatherUrl + query,
                      json=response, status=404,
                      match_querystring=True)
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
    @patch("intents.NLPUtils.extractEntity")
    def test_createResponse(self, extractionMock):
        response = self.initRequestMockup()
        extractionMock.return_value = ["munich"]

        res = WI.createResponse('Munich')
        assert (res == response)

    @responses.activate
    @patch("intents.NLPUtils.extractEntity")
    def test_callAndFormat(self, extractionMock):
        self.initRequestMockup()
        extractionMock.return_value = ["munich"]

        weatherData = WI.createResponse('Weather in Munich')
        answer = WI.formatMessage(weatherData)

        assert (answer == "In Munich there is a cloud and it has 30.2 degrees celcius.")

    @responses.activate
    @patch("BotConnector.loadBotToken")
    @patch("intents.NLPUtils.extractEntity")
    @patch('BotConnector.BotConnector.getInstance')
    def test_executeWithValidLocation(self, instanceMock, extractionMock, tokenMock):
        self.initRequestMockup()
        extractionMock.return_value = ["munich"]
        tokenMock.return_value = "123:abcd"

        instanceMock.return_value = Mock()

        WI.execute('What is the weather in Munich?', 123)
        instanceMock.return_value.send_message.assert_called_once_with(123,
                                                                  "In Munich there is a cloud and it has 30.2 degrees celcius.")

    @responses.activate
    @patch("BotConnector.loadBotToken")
    @patch("intents.NLPUtils.extractEntity")
    @patch('BotConnector.BotConnector.getInstance')
    def test_executeWithInvalidLocation(self, instanceMock, extractionMock, tokenMock):
        self.initRequestMockupForInvalidLocation()
        extractionMock.return_value = []
        tokenMock.return_value = "123:abcd"

        instanceMock.return_value = Mock()

        WI.execute('What is the weather in Tajsdklasdjaklsjd?', 123)

        instanceMock.return_value.send_message.assert_called_once_with(123,
                                                                  "Error handling your request. "
                                                                  "Api-Call limit exceeded or invalid location.")
