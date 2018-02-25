from Intent import Intent
import re

class CalculatorIntent(Intent):

    @staticmethod
    def execute(string, bot, chat_id):
        # type: (object, object, object) -> object
        match = re.search('([-+]?\d*\.\d+|\d+)([\+\-*/]|\*\*)([-+]?\d*\.\d+|\d+)', str(string))
        if not match:
            return "I cannot calculate that..."
        result = eval(string) # CAUTION: eval can cause security issues. (That is why there is the match before)
        bot.send_message(chat_id, eval(string))