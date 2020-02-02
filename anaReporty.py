#!/usr/bin/env python

import json
import pandas as pd
import os

anaFileRoot = '/home/radasm/GoProjects/katago_Tools/ana_report'
# anaTestFile = '/home/radasm/GoProjects/katago_Tools/ana_report/Kat01_cho_0323_1.report'
anaPD = pd.DataFrame(columns=['name', 'move', 'wr', 'tr'])
# anaPD.append(pd.Series(['222', '22', '11', '22'], index=anaPD.columns), ignore_index=True)

def setInfo(name, anaText):
    for moveAnaReport in anaText:
        turnMove = moveAnaReport['turnNumber']
        moveInfos = moveAnaReport['moveInfos']
        bestMoveInfo = moveInfos[0]
        winrate = bestMoveInfo['winrate']
        scoreLead = bestMoveInfo['scoreLead']

        anaPD.loc[len(anaPD)] = [name, turnMove, winrate, scoreLead]


for anaFile_ in os.listdir(anaFileRoot):
    if not os.path.isdir(anaFile_):
        with open(anaFileRoot+'/'+anaFile_, 'rt') as anafile:
            anaText = json.loads(anafile.read())
            # print(anaText)
            nameWithType = os.path.basename(anaFile_)
            moveFileName = nameWithType[:-7]
            setInfo(name=moveFileName, anaText=anaText)

print(anaPD.head())
anaPD.to_csv('testAnaExcel.csv')