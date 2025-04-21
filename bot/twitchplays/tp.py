#!/usr/bin/env python3

import socket
import threading
from ahk import AHK

message = ""
user = ""
# install from https://www.autohotkey.com/download/
ahk = AHK("C:\\Program Files\\AutoHotkey\\AutoHotkey.exe")

class TwitchPlays:
    def __init__(self, name, OAUTH):
        self.CHANNEL = name #monitored channel
        self.OWNER = name #account, WARNING lower case
        self.PASS = OAUTH #authentication https://twitchapps.com/tmi/
        self.BOT = "TwitchPlays"
        
        self.SERVER = "irc.twitch.tv"
        self.PORT = 6667
        self.irc = socket.socket() #connecting
        self.irc.connect((self.SERVER, self.PORT))
        self.irc.send(
            (
                f"PASS {self.PASS}"
                + "\n"
                + "NICK {self.BOT}"
                + "\n"
                + "JOIN #"
                + self.CHANNEL
                + "\n"
            ).encode()
        )
    
    def gamecontrol(self):
        global message
        
        while True:
            if "hoch" == message.lower():
                ahk.key_press('up')
                message = ""

            if "runter" == message.lower():
                ahk.key_press('down')
                message = ""

            if "links" == message.lower():
                ahk.key_press('left')
                message = ""

            if "rechts" == message.lower():
                ahk.key_press('right')
                message = ""

            if "w" == message.lower():
                ahk.key_press('w')
                message = ""

            if "a" == message.lower():
                ahk.key_press('a')
                message = ""

            if "s" == message.lower():
                ahk.key_press('s')
                message = ""

            if "d" == message.lower():
                ahk.key_press('d')
                message = ""

            if "e" == message.lower():
                ahk.key_press('e')
                message = ""

            if "q" == message.lower():
                ahk.key_press('q')
                message = ""

    def twitch(self):
        global user
        global message

        def joinchat():
            Loading = True
            while Loading:
                readbuffer_join = self.irc.recv(1024)
                readbuffer_join = readbuffer_join.decode()
                print(readbuffer_join)
                for line in readbuffer_join.split("\n")[0:-1]:
                    print(line)
                    Loading = loadingComplete(line)

        def loadingComplete(line):
            if ("End of /NAMES list" in line):
                print(f'{self.BOT} running on {self.CHANNEL}' + "'s channel!")
                sendMessage("Hey Leute, ihr könnt mit euren Eingaben das Spiel steuern! Einfach bspw. w, a, s oder d in den Chat!")
                return False #if joined the chat, don't try to join again
            else:
                return True

        def sendMessage(msg):
            messageTemp = f"PRIVMSG #{self.CHANNEL} : {msg}"
            self.irc.send((messageTemp + "\n").encode())

        def getUser(line):
            #global user
            colons = line.count(":")
            colonless = colons-1
            separate = line.split(":", colons)
            user = separate[colonless].split("!", 1)[0]
            return user

        def getMessage(line):
            #global message
            try:
                colons = line.count(":")
                message = (line.split(":", colons))[colons]
            except:
                message = ""
            return message

        def console(line):
            return "PRIVMSG" not in line

        #running the functions above
        joinchat()
        self.irc.send("CAP REQ :twitch.tv/tags\r\n".encode())
        while True:
            try:
                readbuffer = self.irc.recv(1024).decode()
            except:
                readbuffer = ""
                
            for line in readbuffer.split("\r\n"):
                if line == "":
                    continue
                if "PING :tmi.twitch.tv" in line:
                    print(line)
                    msgg = "PONG :tmi.twitch.tv\r\n".encode()
                    self.irc.send(msgg)
                    print(msgg)
                    continue
                else:
                    try:
                        user = getUser(line) #reading the user and its message from chat
                        message = getMessage(line)
                        print(user + " : " + message)
                    except Exception:
                        pass
    
    def runTwitchPlays(self):
        t1 = threading.Thread(target = self.twitch)
        t1.start()
        t2 = threading.Thread(target = self.gamecontrol)
        t2. start()

def main():
    tp = TwitchPlays("<username all in lowercase>", "oauth:XXXXXXXXXXXXXXXXXXXXX")
    tp.runTwitchPlays()

if __name__ == '__main__':
    main()
