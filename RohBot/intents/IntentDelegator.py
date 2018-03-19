from rake_nltk import Rake

from WeatherIntent import WeatherIntent
from WikipediaIntent import WikipediaIntent
from ImageIntent import ImageIntent
from NLPUtils import matchUtterance, filterKeywords
from intents.PokemonIntent import PokemonIntent


class IntentDelegator:

    global intents
    intents = [WeatherIntent, WikipediaIntent]

    def __init__(self):
        pass

    def matchUtterances(self, message):
        matchingIntents = []
        for intent in intents:
            for utterance in intent.utterances:
                if matchUtterance(message, utterance):
                    matchingIntents.append((len(utterance), intent))
        if len(matchingIntents) == 0:
            return None
        matchingIntents = sorted(matchingIntents, key=lambda x: x[0], reverse=True)
        return matchingIntents[0][1]

    def recognizeIntent(self, message):

        detectedIntent = self.matchUtterances(message)
        if detectedIntent is not None:
            return detectedIntent

        fallBackIntent = WikipediaIntent
        finalIntent = fallBackIntent

        keyWords = filterKeywords(message)
        for intent in intents:
            for word in intent.keywords:
                if word in keyWords:
                    finalIntent = WeatherIntent
        return finalIntent


    def handleRequest(self, chat_id, message):
        intent = self.recognizeIntent(message)
        intent.execute(message, chat_id)

