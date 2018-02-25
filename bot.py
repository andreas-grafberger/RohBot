import telegram

from Utils import loadBotToken

if __name__ == "__main__":

    bot = telegram.Bot(token=loadBotToken())
    updates = bot.getUpdates()
    lastMessage = updates[-1]
    chat_id = lastMessage.message.chat_id

    lastText = lastMessage.message.text
    lastOffset = lastMessage.update_id

    bot.send_message(chat_id, "Test!")