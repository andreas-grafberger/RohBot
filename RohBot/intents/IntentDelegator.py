from rake_nltk import Rake

from WeatherIntent import WeatherIntent
from WikipediaIntent import WikipediaIntent


class IntentDelegator:

    def __init__(self):
        pass

    def filterKeywords(self, str):
        r = Rake()
        r.extract_keywords_from_text(str)
        return r.get_ranked_phrases()

    def handleRequest(self, chat_id, message):
        intent = WikipediaIntent

        keyWords = self.filterKeywords(message)
        print(keyWords)
        for word in WeatherIntent.keywords:
            if word in keyWords:
                intent = WeatherIntent

        intent.execute(message, chat_id)

