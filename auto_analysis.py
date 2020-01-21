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

enginne = GTPFacade("kata", KataGo)

teststr = '{"id":"foo","initialStones":[["B","E4"],["B","C4"]],"moves":[["W","D5"],["B","E6"]],"rules":"tromp-taylor","komi":7.5,"boardXSize":13,"boardYSize":13,"analyzeTurns":[0,1,2]}'

time.sleep(8)
while (True):
    print(enginne.sendstr(teststr))
    
    break

