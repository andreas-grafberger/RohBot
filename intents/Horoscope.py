import requests
from intents.Intent import Intent

class Horoscope(Intent):
    @staticmethod
    def execute(str, bot, chat_id):
        str = str.lower()
        sunsigns = {"widder": "aries", "stier": "taurus", "zwilling": "gemini", "krebs": "cancer", "loewe": "leo", "jungfrau": "virgo",
                    "waage": "libra", "skorpion": "scorpio", "schuetze": "stagittarius", "steinbock": "capricorn", "wassermann": "aquarius", "fische": "pisces"}
        if sunsigns.has_key(str):  # for German sunsigns
            str = sunsigns[str]
        url = "http://horoscope-api.herokuapp.com/horoscope/today/" + str
        rsp = requests.get(url).json()  # parses json to python dictionary
        bot.send_message(chat_id, rsp["horoscope"])
