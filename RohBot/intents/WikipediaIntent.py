from Intent import Intent

from wikipedia import DisambiguationError, PageError, page, summary

from NLPUtils import filterKeyword


class WikipediaIntent(Intent):
    # TODO Refactor and add tests
    keywords = ['Define', 'weather', 'Weather']

    utterances = ["What is %s", "What's %s", "Define %s", "Tell me what %s is"]

    @staticmethod
    def getPageForTopic(topicName):
        found = None
        try:
            found = page(topicName)
        except (PageError, UnicodeEncodeError) as e:
            pass
        except DisambiguationError as e:
            options = e.options
            if len(options) == 0:
                sum = "Could not find page for " + topicName
            else:
                firstOption = options[0]
                found = page(firstOption)
        return found

    @staticmethod
    def getUrlSummaryForTopic(topicName):
        page = WikipediaIntent.getPageForTopic(topicName)
        if page is None:
            return "Could not find corresponding page."
        else:
            return page.summary

    @staticmethod
    def execute(str, chat_id):
        keyword = filterKeyword(str)
        if keyword is None:
            answer = "I don't know what to do, sorry. Please reword your request."
        else:
            answer = WikipediaIntent.getUrlSummaryForTopic(keyword)

        answer = ".".join(answer.split('.')[:2]) + "."

        from BotConnector import BotConnector
        BotConnector.getInstance().send_message(chat_id, answer)
