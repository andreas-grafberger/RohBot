from telegram import Bot
from Utils import loadBotToken

class BotConnector:
    instance = None
    token = None

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.token = loadBotToken()
            cls.instance = Bot(cls.token)
        return cls.instance
