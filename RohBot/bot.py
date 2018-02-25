import telegram
import time
from Utils import loadBotToken

def lookupLastMessage(bot):
    global lastOffset
    updates = []
    try:
        updates = bot.getUpdates(offset=lastOffset + 1, timeout=3)
    except telegram.error.TimedOut as e:
        print e
    if len(updates) == 0:
        return
    lastMessage = updates[-1]
    chat_id = lastMessage.message.chat_id
    print("Received message from {} with id {} and text \"{}\"".format(lastMessage.message.chat.first_name,lastMessage.update_id, lastMessage.message.text))

    lastText = lastMessage.message.text
    lastOffset = lastMessage.update_id

    bot.send_message(chat_id, "You wrote: " + lastText)

if __name__ == "__main__":
    lastOffset = 0

    bot = telegram.Bot(token=loadBotToken())

    while True:
        try:
            lookupLastMessage(bot)
        except (UnicodeEncodeError, TypeError) as e:
            print(e)
        time.sleep(1)
