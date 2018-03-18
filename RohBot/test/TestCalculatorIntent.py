import pytest
from intents.CalculatorIntent import CalculatorIntent as CI


class TestCalculatorIntent(object):

    def test_CorrectAnswer(self):
        result = CI.evaluate("2+2")
        assert(result == 4)

    def test_ignoreWhitespacesAnswer(self):
        result = CI.evaluate("2+2\n")
        assert(result == 4)

    def test_returnNoneOnInvalidInput(self):
        result = CI.evaluate("2d+2\n")
        assert(result == None)