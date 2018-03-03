import telegram

from Utils import loadBotToken


class BotConnector:

    global instance
    instance = None

    @staticmethod
    def getInstance():
        global instance
        if instance is None:
            instance = telegram.Bot(token=loadBotToken())
        return instance
