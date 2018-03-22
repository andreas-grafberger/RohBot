import yaml
import os

pathToConfig = os.path.dirname(os.path.abspath(__file__)) + "/../Config"


def loadBotToken(configFile=pathToConfig):
    try:
        configObj = yaml.safe_load(file(configFile, "r"))
        token = configObj["bot-token"]
    except Exception:
        print("Couldn't read config file")
        exit(2)
    return token


def loadOWMToken(configFile=pathToConfig):
    try:
        configObj = yaml.safe_load(file(configFile, "r"))
        token = configObj["owm-token"]
    except Exception:
        return None
    return token