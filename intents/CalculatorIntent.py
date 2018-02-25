from Intent import Intent
import re


class CalculatorIntent(Intent):

    @staticmethod
    def evaluate(input):

        # First remove whitespaces from string
        expression = ''.join(input.split())

        result = None
        match = re.search('([-+]?\d*\.\d+|\d+)([\+\-*/]|\*\*)([-+]?\d*\.\d+|\d+)', expression)
        if match:
            result = eval(expression)  # CAUTION: eval can cause security issues. (That is why there is the match before)
        return result

    @staticmethod
    def execute(string, bot, chat_id):
        answer = CalculatorIntent.evaluate(string)
        if answer is None:
            bot.send_message(chat_id, "I cannot calculate that...")
        else:
            bot.send_message(chat_id, "Answer: " + answer)
