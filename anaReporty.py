#!/usr/bin/env python

import json
import pandas as pd
import os

anaFileRoot = '/home/radasm/GoProjects/katago_Tools/ana_report'
# anaTestFile = '/home/radasm/GoProjects/katago_Tools/ana_report/Kat01_cho_0323_1.report'
anaPD = pd.DataFrame(columns=['name', 'move', 'wr', 'tr'])
# anaPD.append(pd.Series(['222', '22', '11', '22'], index=anaPD.columns), ignore_index=True)
anaPD_BA = pd.DataFrame(columns=['name', 'move', 'wrbefore', 'wrafter', 'wrdiff', 'trbefore', 'trafter', 'trdiff'])


def setInfo(name, anaText):
    for moveAnaReport in anaText:
        turnMove = moveAnaReport['turnNumber']
        moveInfos = moveAnaReport['moveInfos']
        bestMoveInfo = moveInfos[0]
        winrate = bestMoveInfo['winrate']
        scoreLead = bestMoveInfo['scoreLead']

        anaPD.loc[len(anaPD)] = [name, turnMove, winrate, scoreLead]

def setDiffInfo(name,anaText):
    for moveAnaReport in anaText:
        turnMove = moveAnaReport['turnNumber']

        if turnMove%2 == 1:
            moveInfos = moveAnaReport['moveInfos']
            bestMoveInfo = moveInfos[0]
            winrate = bestMoveInfo['winrate']
            scoreLead = bestMoveInfo['scoreLead']

            for moveAnaReport_ in anaText:
                turnMove_ = moveAnaReport_['turnNumber']
                moveInfos_ = moveAnaReport_['moveInfos']
                if turnMove_ == (turnMove + 1):
                    bestMoveInfo_ = moveInfos_[0]
                    winrate_ = bestMoveInfo_['winrate']
                    scoreLead_ = bestMoveInfo_['scoreLead']
                    anaPD_BA.loc[len(anaPD_BA)] = [name, turnMove, winrate, winrate_, winrate_-winrate, scoreLead,scoreLead_, scoreLead_-scoreLead]

                    break

for anaFile_ in os.listdir(anaFileRoot):
    if not os.path.isdir(anaFile_):
        with open(anaFileRoot+'/'+anaFile_, 'rt') as anafile:
            anaText = json.loads(anafile.read())
            # print(anaText)
            nameWithType = os.path.basename(anaFile_)
            moveFileName = nameWithType[:-7]
            # setInfo(name=moveFileName, anaText=anaText)
            setDiffInfo(name=moveFileName,anaText = anaText)

# anaPD.to_csv('testAnaExcel.csv')
anaPD_BA.to_csv('testAnaDiff.csv')