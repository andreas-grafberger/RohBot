from intents.Intent import Intent
import yaml
import os
import errno



class Field:
    def __init__(self, size, player1, player2):
        self.size = size
        self.data = ""
        for i in xrange(0, size*size):
            self.data = self.data + ' '
        self.data = list(self.data)
        self.player = player1
        self.player1 = player1
        self.player2 = player2

    def get(self, x, y):
        if not self.isValid(x, y): return ' '

        return self.data[y * self.size + x]

    def set(self, x, y, c):
        if not self.isValid(x, y): return False

        self.data[y * self.size + x] = c
        return True

    def isValid(self, x, y):
        if x < 0: return False
        if x >= self.size: return False
        if y < 0: return False
        if y >= self.size: return False
        return True

    def getPlayer(self):
        return self.player

    def togglePlayer(self):
        if self.player == self.player1:
            self.player = self.player2
        else:
            self.player = self.player1

    def isPlayer(self, id):
        return id == self.player1 or id == self.player2

    def getPlayerChar(self, id):
        if id == self.player1: return 'X'
        if id == self.player2: return 'O'
        return ' '

    def getPrint(self):
        printfield = "";

        for y in xrange(0, self.size):
            if y == 0:
                printfield = printfield + unichr(0x250D)
                for x in xrange(0, self.size-1):
                    printfield = printfield + unichr(0x2500)
                    printfield = printfield + unichr(0x252C)
                printfield = printfield + unichr(0x2500)
                printfield = printfield + unichr(0x2511)
                printfield = printfield + "\n"
            else:
                printfield = printfield + unichr(0x251C)
                for x in xrange(0, self.size - 1):
                    printfield = printfield + unichr(0x2500)
                    printfield = printfield + unichr(0x253C)
                printfield = printfield + unichr(0x2500)
                printfield = printfield + unichr(0x2524)
                printfield = printfield + "\n"

            printfield = printfield + unichr(0x2502)
            for x in xrange(0, self.size):
                if self.get(x, y)==' ':
                    printfield = printfield + unichr(0x2004) + unichr(0x2004)
                else:
                    printfield = printfield + self.get(x, y)
                printfield = printfield + unichr(0x2502)
            printfield = printfield + "\n"

            if y == self.size-1:
                printfield = printfield + unichr(0x2514)
                for x in xrange(0, self.size - 1):
                    printfield = printfield + unichr(0x2500)
                    printfield = printfield + unichr(0x2534)
                printfield = printfield + unichr(0x2500)
                printfield = printfield + unichr(0x2518)
                printfield = printfield + "\n"

        return printfield;


class AndIntent(Intent):
    nameToID = dict()
    idToName = dict()
    games = dict()

    try:
        os.makedirs("./anddata/")
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    try:
        nameToID = yaml.load(file("./anddata/name_to_id", "r"))
        idToName = yaml.load(file("./anddata/id_to_name", "r"))
    except Exception:
        nameToID = dict()
        idToName = dict()
    try:
        games = yaml.load(file("./anddata/games", "r"))
    except Exception as e:
        print(e)
        games = dict()

    @staticmethod
    def execute(message, bot, chat_id):
        str_split = unicode.split(unicode(message), ' ')

        str_split[0] = str_split[0].lower()

        if not AndIntent.isRegistered(chat_id):
            if str_split[0] != "register":
                AndIntent.sendError(bot, chat_id, "Bitte mit register [name] registrieren!")
                return "";

        if len(str_split)>=1:
            if str_split[0] == "register":
                if len(str_split)!=2:
                    AndIntent.sendError(bot, chat_id, "Bitte Namen angeben!")
                    return ""

                result = AndIntent.setName(chat_id, str_split[1])
                if result==0:
                    AndIntent.sendReply(bot, chat_id, "Erfolgreich registriert!")
                    return ""
                elif result==1:
                    AndIntent.sendError(bot, chat_id, "Bereits registriert!\n'help' fuer mehr Informationen")
                    return ""
                elif result==2:
                    AndIntent.sendError(bot, chat_id, "Name bereits vergeben!")
                    return ""
                else:
                    AndIntent.sendError(bot, chat_id, "Name ungueltig! (3-12 Zeichen)")
                    return ""

            elif str_split[0] == "list":
                glist = AndIntent.listGames(chat_id)
                reply = "Aktuelle Spiele ("+str(len(glist))+"):"
                reply = reply + "\n"
                pos = 1
                for game in glist:
                    reply = reply + str(pos)+": "+AndIntent.getName(game.getPlayer())+"s Zug"
                    reply = reply + "\n"
                    pos = pos + 1

                AndIntent.sendReply(bot, chat_id, reply)
                return ""

            elif str_split[0] == "challenge":
                if len(str_split)!=2:
                    AndIntent.sendError(bot, chat_id, "challange [name]\nFordert einen Spieler zu einem Spiel heraus")
                    return ""

                other = str_split[1]
                if other==AndIntent.getName(chat_id):
                    AndIntent.sendError(bot, chat_id, "Selbst herausfordern nicht moeglich!")
                    return ""

                if not AndIntent.nameExists(other):
                    AndIntent.sendError(bot, chat_id, "Spieler "+other+" nicht gefunden!")
                    return ""

                other_id = AndIntent.getChatID(other)

                game_id = 0
                while game_id in AndIntent.games:
                    game_id = game_id + 1

                game = Field(3, other_id, chat_id)
                AndIntent.games[game_id] = game

                with open("./anddata/games", 'w') as f:
                    yaml.dump(AndIntent.games, f)

                AndIntent.sendReply(bot, chat_id, "Herausforderung versandt")
                return ""

            elif str_split[0] == "show":
                if len(str_split)!=2:
                    AndIntent.sendError(bot, chat_id, "Bitte Spielnummer angeben!")
                    return ""

                try:
                    int(str_split[1])
                except:
                    AndIntent.sendError(bot, chat_id, "Ungueltige Spielnummer!")
                    return ""

                num = int(str_split[1])
                glist = AndIntent.listGames(chat_id)

                if num<1 or num>len(glist):
                    AndIntent.sendError(bot, chat_id, "Ungueltige Spielnummer!")
                    return ""

                game = glist[num-1]

                state = game.getPrint()
                state = state + "\n"
                state = state + "Am Zug: " + AndIntent.getName(game.getPlayer())
                AndIntent.sendReply(bot, chat_id, state)

                return ""

            elif str_split[0] == "play":
                if len(str_split)!=4:
                    AndIntent.sendError(bot, chat_id, "Bitte Spielnummer und Position(X,Y) angeben!\nplay [spiel] [x] [y]")
                    return ""

                try:
                    int(str_split[1])
                except:
                    AndIntent.sendError(bot, chat_id, "Ungueltige Spielnummer!")
                    return ""

                num = int(str_split[1])
                glist = AndIntent.listGames(chat_id)

                if num < 1 or num > len(glist):
                    AndIntent.sendError(bot, chat_id, "Ungueltige Spielnummer!")
                    return ""

                game = glist[num-1]

                if game.getPlayer() != chat_id:
                    AndIntent.sendError(bot, chat_id, "Nicht dein Zug!")
                    return "";

                try:
                    int(str_split[2])
                    int(str_split[3])
                except:
                    AndIntent.sendError(bot, chat_id, "Ungueltige Position!")
                    return ""

                posx = int(str_split[2])-1
                posy = int(str_split[3])-1

                if not game.isValid(posx, posy):
                    AndIntent.sendError(bot, chat_id, "Ungueltige Position!")
                    return "";

                if game.get(posx, posy)!=' ':
                    AndIntent.sendError(bot, chat_id, "Feld bereits belegt!")
                    return "";

                game.set(posx, posy, game.getPlayerChar(chat_id))
                game.togglePlayer()

                with open("./anddata/games", 'w') as f:
                    yaml.dump(AndIntent.games, f)

                state = "Zug durchgefuehrt:"
                state = state + "\n"
                state = state + game.getPrint()
                state = state + "\n"
                state = state + "Am Zug: " + AndIntent.getName(game.getPlayer())
                AndIntent.sendReply(bot, chat_id, state)
                return ""

            else:
                glist = AndIntent.listGames(chat_id)
                reply = "Hallo "+AndIntent.getName(chat_id)
                reply = reply + "\n"
                reply = reply + "Verfuegbare Befehle: \n"
                reply = reply + " - list\n"
                reply = reply + " - challenge [Spieler]\n"
                reply = reply + " - show [Spiel]\n"
                reply = reply + " - play [Spiel] [X 1-3] [Y 1-3]\n"
                reply = reply + "\n"

                reply = reply + "Aktuelle Spiele ("+str(len(glist))+"):"
                reply = reply + "\n"
                pos = 1
                for game in glist:
                    reply = reply + str(pos)+": "+AndIntent.getName(game.getPlayer())+"s Zug"
                    reply = reply + "\n"
                    pos = pos + 1

                AndIntent.sendReply(bot, chat_id, reply)
                return ""


        return ""

    @staticmethod
    def sendError(bot, chat_id, error):
        if bot!=0: bot.send_message(chat_id, "Error: \n"+error)
        print("Error: \n"+error)
        return ""

    @staticmethod
    def sendReply(bot, chat_id, reply):
        if bot!=0: bot.send_message(chat_id, reply)
        print(reply)
        return ""

    @staticmethod
    def setName(chat_id, name):
        # do not allow duplicated entries
        if chat_id in AndIntent.idToName:
            return 1
        if name in AndIntent.nameToID:
            return 2

        # check name
        if len(name) < 3:
            return 3
        if len(name) > 12:
            return 4
        if unicode.count(name, ' ') > 0:
            return 5
        pos = 0
        for c in name:
            if not (unicode.isalpha(c) or (pos > 0 and unicode.isdigit(c))):
                return 6
            pos = pos + 1

        AndIntent.nameToID[name] = chat_id
        AndIntent.idToName[chat_id] = name

        with open("./anddata/name_to_id", 'w') as f:
            yaml.dump(AndIntent.nameToID, f)
        with open("./anddata/id_to_name", 'w') as f:
            yaml.dump(AndIntent.idToName, f)

        return 0

    @staticmethod
    def getName(chat_id):
        return AndIntent.idToName[chat_id]

    @staticmethod
    def getChatID(name):
        return AndIntent.nameToID[name]

    @staticmethod
    def nameExists(name):
        return name in AndIntent.nameToID

    @staticmethod
    def isRegistered(chat_id):
        return chat_id in AndIntent.idToName

    @staticmethod
    def listGames(chat_id):
        glist = []

        for key in AndIntent.games:
            if AndIntent.games[key].isPlayer(chat_id):
                glist.append(AndIntent.games[key])

        return glist;

