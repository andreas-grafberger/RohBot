# coding=utf-8
import pytest
from intents.NLPUtils import *


class TestNLPUtils(object):

    def test_doesMatchUtterance(self):
        template = "What is %s"
        userInput = "Hey, what is Augsburg?"

        doesMatch = matchUtterance(userInput, template)
        assert (doesMatch)

        template = "What is the weather in %s?"
        userInput = "Hey, what is the weather in Augsburg?"
        doesMatch = matchUtterance(userInput, template)
        assert(doesMatch)

    def test_doesNotMatchUtterance(self):
        template = "What is %s"
        userInput = "Hey, what Augsburg?"

        doesMatch = matchUtterance(userInput, template)
        assert (not doesMatch)

    def test_doesNotMatchUtteranceOnShorterInput(self):
        template = "What is %s"
        userInput = "Hey, what?"

        doesMatch = matchUtterance(userInput, template)
        assert (not doesMatch)

    def test_extractCorrectEntities(self):
        sentence = "What's the weather in Germany today?"
        detectedEnts = extractEntities(sentence, entities=["GPE", "DATE"])

        assert (len(detectedEnts) == 2)
        assert ("Germany" in detectedEnts and "today" in detectedEnts)

        sentence = "What's the weather in Germany today?"
        detectedEnts = extractEntities(sentence, entities=["GPE", "DATE"], removeWords=["today"])

        assert (len(detectedEnts) == 1)
        assert ("Germany" in detectedEnts)

    def test_extractCorrectEntity(self):
        sentence = "How high is the Mount Everest"
        detectedEnts = extractEntity(sentence, entity="LOC")

        assert (len(detectedEnts) == 1)
        assert ("the Mount Everest" in detectedEnts)

    def test_extractEntityOnEmptyInput(self):
        sentence = ""
        detectedEnts = extractEntity(sentence, entity="", removeWords=[])

        assert (len(detectedEnts) == 0)

    def test_extractEntitiesOnEmptyInput(self):
        sentence = ""
        detectedEnts = extractEntities(sentence, entities=[], removeWords=[])

        assert (len(detectedEnts) == 0)

    def test_extractAllEntities(self):
        sentence = "Jesus, They’re good dogs Jeff. Why don't you visit France and return 10€"  # TODO Brent unfortunately didn't get classified correctly :-(
        detectedEnts = extractAllEntities(sentence)

        assert (len(detectedEnts) == 4)
        assert (("Jesus", "PERSON") in detectedEnts)
        assert (("Jeff", "PERSON") in detectedEnts)
        assert (("France", "GPE") in detectedEnts)
        assert ((u"10€", "MONEY") in detectedEnts)

    def test_filterKeywords(self):
        sentence = "Who is Donald Trump and was he born in Kenya?"
        keywords = filterKeywords(sentence)
        assert("donald trump" in keywords)
        assert ("kenya" in keywords)

    def test_filterKeywordsOnEmptyString(self):
        sentence = ""
        keywords = filterKeywords(sentence)
        assert ([] == keywords)

    def test_filterKeyword(self):
        sentence = "Who is Barack Obama?"
        keywords = filterKeyword(sentence)
        assert("barack obama" == keywords)

    def test_filterKeywordOnEmptyString(self):
        sentence = ""
        keywords = filterKeyword(sentence)
        assert (None == keywords)
