from Intent import Intent

from wikipedia import DisambiguationError, PageError, page, summary
from rake_nltk import Rake


class WikipediaIntent(Intent):


    @staticmethod
    def getUrlSummaryForTopic(topicName):

        sum = None
        try:
            sum = summary(topicName, sentences=2)
        except PageError as e:
            sum = "Could not find page for " + topicName
        except DisambiguationError as e:
            options = e.options
            if len(options) == 0:
                sum = "Could not find page for " + topicName
            else:
                firstOption = options[0]
                sum = summary(firstOption, sentences=2)
        return sum

    @staticmethod
    def execute(str, chat_id):
        keyword = WikipediaIntent.filterKeyword(str)
        keyword = filterKeyword(str)
        if keyword is None:
            answer = "I don't know what to do, sorry. Please reword your request."
        else:
            answer = WikipediaIntent.getUrlSummaryForTopic(keyword)

        from BotConnector import BotConnector
        BotConnector.getInstance().send_message(chat_id, answer)
