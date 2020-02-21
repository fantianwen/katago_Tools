#!/usr/bin/env python

import json
import pandas as pd
import os
import math

anaFileRoot = '/home/radasm/GoProjects/katago_Tools/ana_report_good'
# anaTestFile = '/home/radasm/GoProjects/katago_Tools/ana_report/Kat01_cho_0323_1.report'
anaPD = pd.DataFrame(columns=['name', 'move', 'wr', 'tr'])
# anaPD.append(pd.Series(['222', '22', '11', '22'], index=anaPD.columns), ignore_index=True)
anaPD_BA = pd.DataFrame(columns=['name', 'move', 'wrbefore', 'wrafter', 'wrdiff', 'trbefore', 'trafter', 'trdiff', 'dist1b', 'ownbefore', 'ownafter', 'owndiff'])

# def setInfo(name, anaText):
#     for moveAnaReport in anaText:
#         turnMove = moveAnaReport['turnNumber']
#         moveInfos = moveAnaReport['moveInfos']
#         bestMoveInfo = moveInfos[0]
#         winrate = bestMoveInfo['winrate']
#         scoreLead = bestMoveInfo['scoreLead']
#
#         anaPD.loc[len(anaPD)] = [name, turnMove, winrate, scoreLead]

moveIndexes = 'abcdefghijklmn'

def calulateDistance(originalMove, bestMoveInfo):
    original_x = originalMove[0]
    original_y = originalMove[1:]

    original_x_i = moveIndexes.index(original_x)

    if moveIndexes.index(original_x)>9:
        original_x_i = moveIndexes.index(original_x)-1

    original_y_i = int(original_y) if int(original_y < 9) else int(original_y) -1

    best_x = bestMoveInfo[0]
    best_y = bestMoveInfo[1:]

    best_x_i = moveIndexes.index(best_x)

    if moveIndexes.index(best_x) > 9:
        best_x_i = moveIndexes.index(best_x) - 1

    best_y_i = int(best_y) if int(best_y < 9) else int(best_y) - 1

    return float(math.pow(math.pow(original_x_i-best_x_i,2)+math.pow(original_y_i-best_y_i,2), 0.5))

def setDiffInfo(name, anaText, filePath):
    for moveAnaReport in anaText:
        turnMove = moveAnaReport['turnNumber']

        if turnMove % 2 == 1:
            moveInfos = moveAnaReport['moveInfos']
            bestMoveInfo = moveInfos[0]
            winrate = bestMoveInfo['winrate']
            scoreLead = bestMoveInfo['scoreLead']

            # get actual black move
            # filepath + (turnMove + 1)
            with open(filePath) as moveInfomation:
                move_json = json.dumps(moveInfomation)
                originalBlackMove = move_json['moves'][move_json['analyzeTurns']-1]
            dis1b = calulateDistance(originalBlackMove, bestMoveInfo['move'])

            for moveAnaReport_ in anaText:
                turnMove_ = moveAnaReport_['turnNumber']
                moveInfos_ = moveAnaReport_['moveInfos']
                if turnMove_ == (turnMove + 1):
                    bestMoveInfo_ = moveInfos_[0]
                    winrate_ = bestMoveInfo_['winrate']
                    scoreLead_ = bestMoveInfo_['scoreLead']



                    anaPD_BA.loc[len(anaPD_BA)] = [name, turnMove, winrate, winrate_, winrate_ - winrate, scoreLead,
                                                   scoreLead_, scoreLead_ - scoreLead,dis1b,]

                    break

for anaFile_ in os.listdir(anaFileRoot):
    if not os.path.isdir(anaFile_):
        with open(anaFileRoot + '/' + anaFile_, 'rt') as anafile:
            anaText = json.loads(anafile.read())
            # print(anaText)
            nameWithType = os.path.basename(anaFile_)
            moveFileName = nameWithType[:-7]
            # handicap stones
            # setInfo(name=moveFileName, anaText=anaText)
            # file path
            # FAN --- here should be checked
            filePath = '/home/radasm/GoProjects/katago_Tools/dec_ana_good/'+ anaFile_ + '/' + anaFile_ + '.ana'
            setDiffInfo(name=moveFileName, anaText=anaText, filePath)

# anaPD.to_csv('testAnaExcel.csv')
anaPD_BA.to_csv('testAnaGoodDiff.csv')
