import pytest
from intents import IntentDelegator, WikipediaIntent, WeatherIntent


class TestIntentDelegator(object):
    global delegator
    delegator = IntentDelegator.IntentDelegator()

    def test_recognizeWikipediaIntent(self):
        message = "What's Augsburg?"
        intent = delegator.recognizeIntent(message)
        assert (intent == WikipediaIntent.WikipediaIntent)

        message = "What is Augsburg?"
        intent = delegator.recognizeIntent(message)
        assert (intent == WikipediaIntent.WikipediaIntent)

        message = "Define Augsburg?"
        intent = delegator.recognizeIntent(message)
        assert (intent == WikipediaIntent.WikipediaIntent)

        message = "Tell me what Augsburg is?"
        intent = delegator.recognizeIntent(message)
        assert (intent == WikipediaIntent.WikipediaIntent)

    def test_recognizeWeatherIntent(self):
        message = "What's the weather in Augsburg?"
        intent = delegator.recognizeIntent(message)
        assert (intent == WeatherIntent.WeatherIntent)

        message = "How hot is it in Augsburg?"
        intent = delegator.recognizeIntent(message)
        assert (intent == WeatherIntent.WeatherIntent)
