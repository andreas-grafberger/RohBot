import telegram

import Utils


class BotConnector:

    global instance
    instance = None

    @staticmethod
    def getInstance():
        global instance
        if instance is None:
            instance = telegram.Bot(token=Utils.loadBotToken())
        return instance
