from intents.Intent import Intent

from wikipedia import DisambiguationError, PageError, page
from rake_nltk import Rake


class WikipediaIntent(Intent):

    @staticmethod
    def filterKeyword(str):
        r = Rake()
        r.extract_keywords_from_text(str)
        p = r.get_ranked_phrases()
        if len(p) < 1:
            return None
        return p[0]

    @staticmethod
    def getUrlSummaryForTopic(topicName):

        sum = None
        try:
            wikiPage = page(topicName)
        except PageError as e:
            sum = "Could not find page for " + topicName
        except DisambiguationError as e:
            options = e.options
            if len(options) == 0:
                sum = "Could not find page for " + topicName
            else:
                firstOption = options[0]
                wikiPage = page(firstOption)
                sum = wikiPage.summary
        else:
            sum = wikiPage.summary
        return sum

    @staticmethod
    def execute(str, bot, chat_id):
        answer = ""
        keyword = WikipediaIntent.filterKeyword(str)
        if keyword is None:
            answer = "I don't know what to do, sorry. Please reword your request."
        else:
            answer = WikipediaIntent.getUrlSummaryForTopic(keyword)

        bot.send_message(chat_id, answer)
        return ""
