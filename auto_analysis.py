#!/usr/bin/env python

from subprocess import Popen, PIPE
import time
import datetime
from gtp import parse_vertex, gtp_move, gtp_color
from gtp import BLACK, WHITE, PASS

class GTPSubProcess(object):

    def __init__(self, label, args):
        self.label = label
        self.subprocess = Popen(args, stdin=PIPE, stdout=PIPE)
        
    

    def send(self, data):
        print("sending {}: {}".format(self.label, data))
        self.subprocess.stdin.write(data)
        result = ""
        while True:
            data = self.subprocess.stdout.readline()
            print("=====the data is {}======".format(data))
            if not data.strip():
                break
            result += data
        print("got: {}".format(result))
        return result

    def send1(self, data):
        print("sending {}: {}".format(self.label, data))
        self.subprocess.stdin.write(data)
        data = self.subprocess.stdout.readline()
        print("=====the data is {}======".format(data))
        return data

    def waitUntilEnd(self):
        while True:
            oneline = self.subprocess.stdout.readline()
            if not oneline.strip():
                break

    def close(self):
        print("quitting {} subprocess".format(self.label))
        self.subprocess.communicate("quit\n")




class GTPFacade(object):

    def __init__(self, label, args):
        self.label = label
        self.moves = []
        self.gtp_subprocess = GTPSubProcess(label, args)

    def name(self):
        self.gtp_subprocess.send("name\n")

    def version(self):
        self.gtp_subprocess.send("version\n")

    def boardsize(self, boardsize):
        self.gtp_subprocess.send("boardsize {}\n".format(boardsize))

    def komi(self, komi):
        self.gtp_subprocess.send("komi {}\n".format(komi))

    def clear_board(self):
        self.gtp_subprocess.send("clear_board\n")

    def genmove(self, color):
        self.gtp_subprocess.send(
            "genmove {}\n".format(gtp_color(color)))
        # while True:
        #     isRunning = self.gtp_subprocess.send("check_running\n")
        #     print("=====================The running result is {}===========".format(isRunning))
        #     if not isRunning:
        #         print("============get out!!!!================")
        #         break
        # message = self.gtp_subprocess.send("lastmove\n")

        # print("genmove result is {}".format(message))
        # assert message[0] == "="
        # return parse_vertex(message[1:].strip())

    def genmove1(self, color):
        self.gtp_subprocess.send1(
            "genmove {}\n".format(gtp_color(color)))
        time.sleep(5)
        # while True:
        #     isRunning = self.gtp_subprocess.send("check_running\n")
        #     print("=====================The running result is {}===========".format(isRunning))
        #     if not isRunning:
        #         print("============get out!!!!================")
        #         break
        # message = self.gtp_subprocess.send("lastmove\n")

        # print("genmove result is {}".format(message))
        # assert message[0] == "="
        # return parse_vertex(message[1:].strip())

    def genmove_katago(self, color):
        self.gtp_subprocess.send(
            "genmove_debug {}\n".format(gtp_color(color)))

    def analysis_katago(self,move_json):
        self.gtp_subprocess.send(
            move_json + "\n")

    def checkRunning(self):
        isRunning = self.gtp_subprocess.send("check_running\n")
        return isRunning

    def setHandicap(self,stoneNumber):
        self.gtp_subprocess.send1("fixed_handicap "+str(stoneNumber)+"\n")

    def getLastMove(self):
        lastMove = self.gtp_subprocess.send1("lastmove\n")
        return lastMove.strip()

    def getLastWinrate(self):
        lastWinrate = self.gtp_subprocess.send1("lastwinrate\n")
        return lastWinrate.strip()

    def getLastVisitrate(self):
        lastVisitrate = self.gtp_subprocess.send1("lastVisitrate\n")
        return lastVisitrate.strip()

    def getfinalscore(self):
        finalscore = self.gtp_subprocess.send1("final_score\n")
        return finalscore.strip()

    def printSgf(self):
        return self.gtp_subprocess.send("printsgf\n")

    def showboard(self):
        print("========================show board========================")
        self.gtp_subprocess.send("showboard\n")

    def play(self, color, vertex):
        self.gtp_subprocess.send("play {}\n".format(gtp_move(color, vertex)))

    def final_score(self):
        final_score = self.gtp_subprocess.send1("final_score\n")
        return final_score.strip()

    def close(self):
        self.gtp_subprocess.close()

    def waitUntilEnd(self):
        self.gtp_subprocess.waitUntilEnd()

    def sendstr(self,str_):
        ana = self.gtp_subprocess.send(str_+"\n")
        return ana.strip()

KataGo = ["/home/ikeda-05444/users/fan/GoProjects/KataGo/cpp/katago","analysis","-config","/home/ikeda-05444/users/fan/GoProjects/KataGo/cpp/configs/analysis_example.cfg","-model","/home/ikeda-05444/users/fan/GoProjects/KataModels/model-20200120.txt.gz","-analysis-threads","16"]


KataGo_gtp = ["/home/ikeda-05444/users/fan/GoProjects/KataGo/cpp/katago","gtp","-config","/home/ikeda-05444/users/fan/GoProjects/KataGo/cpp/configs/gtp_example.cfg","-model","/home/ikeda-05444/users/fan/GoProjects/KataModels/model-20200120.txt.gz"]


teststr = '{"id": "test", "initialStones": [["B", "k10"], ["B", "d10"], ["B", "d4"], ["B", "k4"]], "moves": [["W", "f11"], ["B", "c11"], ["W", "h11"], ["B", "k11"], ["W", "l8"], ["B", "l9"], ["W", "k8"], ["B", "m9"], ["W", "h9"], ["B", "g4"], ["W", "l3"], ["B", "l4"], ["W", "k3"], ["B", "j3"], ["W", "j2"], ["B", "h3"], ["W", "h2"], ["B", "g2"], ["W", "f3"], ["B", "g3"], ["W", "c6"], ["B", "d5"], ["W", "b4"], ["B", "d6"], ["W", "c7"], ["B", "c3"], ["W", "b3"], ["B", "c2"], ["W", "m4"], ["B", "m5"], ["W", "m3"], ["B", "l6"], ["W", "m8"], ["B", "n9"], ["W", "c9"], ["B", "e10"], ["W", "e8"], ["B", "f10"], ["W", "g10"], ["B", "c10"], ["W", "d12"], ["B", "e12"], ["W", "f12"], ["B", "e11"], ["W", "e13"], ["B", "c12"], ["W", "b10"], ["B", "f9"], ["W", "f8"]], "rules": "tromp-taylor", "komi": 0.5, "boardXSize": 13, "boardYSize": 13, "maxVisits": 16000, "analyzeTurns": [1, 2, 5, 6, 21, 22, 23, 24, 33, 34, 35, 36, 39, 40]}'
enginne = GTPFacade("kata", KataGo)

time.sleep(8)

while (True):
    print(enginne.sendstr(teststr))
    
    break

