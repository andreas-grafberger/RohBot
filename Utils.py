import yaml

def loadBotToken(configFile="./Config"):
    try:
        configObj = yaml.load(file(configFile, "r"))
        token = configObj["bot-token"]
    except Exception:
        print "Couldn't read config file"
        exit(2)
    return token
