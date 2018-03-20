import pytest
from intents import IntentDelegator, WikipediaIntent, WeatherIntent


class TestIntentDelegator(object):
    global delegator
    delegator = IntentDelegator()

    def test_recognizeWikipediaIntent(self):
        message = "What's Augsburg?"
        intent = delegator.recognizeIntent(message)
        assert (intent == WikipediaIntent)

        message = "What is Augsburg?"
        intent = delegator.recognizeIntent(message)
        assert (intent == WikipediaIntent)

        message = "Define Augsburg?"
        intent = delegator.recognizeIntent(message)
        assert (intent == WikipediaIntent)

        message = "Tell me what Augsburg is?"
        intent = delegator.recognizeIntent(message)
        assert (intent == WikipediaIntent)

    def test_recognizeWeatherIntent(self):
        message = "What's the weather in Augsburg?"
        intent = delegator.recognizeIntent(message)
        assert (intent == WeatherIntent)

        message = "How hot is it in Augsburg?"
        intent = delegator.recognizeIntent(message)
        assert (intent == WeatherIntent)
