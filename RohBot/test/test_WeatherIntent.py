import pytest
from mock import patch, Mock
import responses
import intents.WeatherIntent as WI


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
    @patch("intents.NLPUtils.extractEntity")
    @patch('telegram.Bot.send_message')
    def test_executeWithValidLocation(self, BotMock, extractionMock):
        self.initRequestMockup()
        extractionMock.return_value = ["munich"]

        WI.execute('What is the weather in Munich?', 123)

        BotMock.assert_called_once_with(123, "In Munich there is a cloud and it has 30.2 degrees celcius.")

    @responses.activate
    @patch("intents.NLPUtils.extractEntity")
    @patch('telegram.Bot.send_message')
    def test_executeWithInvalidLocation(self, BotMock, extractionMock):
        self.initRequestMockupForInvalidLocation()
        extractionMock.return_value = []
        WI.execute('What is the weather in Tajsdklasdjaklsjd?', 123)

        BotMock.assert_called_once_with(123,
                                        "Error handling your request. Api-Call limit exceeded or invalid location.")
