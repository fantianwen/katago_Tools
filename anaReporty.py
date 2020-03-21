#!/usr/bin/env python

import json
import pandas as pd
import os
import math

moveIndexes = 'ABCDEFGHJKLMN'
moveIndexes_low = 'abcdefghjklmn'

anaFileRoot = '/home/fan/GoProjects/katago_Tools/ana_report_good'
# anaTestFile = '/home/radasm/GoProjects/katago_Tools/ana_report/Kat01_cho_0323_1.report'
# anaPD = pd.DataFrame(columns=['name', 'move', 'wr', 'tr'])
# anaPD.append(pd.Series(['222', '22', '11', '22'], index=anaPD.columns), ignore_index=True)
anaPD_BA = pd.DataFrame(columns=['name', 'handi', 'move', 'shaperate', 'shapelog', 'wrbefore', 'wrafter', 'wrdiff', 'trbefore', 'trafter', 'trdiff', 'dist1b', 'ownbefore', 'ownafter', 'owndiff'])

# def setInfo(name, anaText):
#     for moveAnaReport in anaText:
#         turnMove = moveAnaReport['turnNumber']
#         moveInfos = moveAnaReport['moveInfos']
#         bestMoveInfo = moveInfos[0]
#         winrate = bestMoveInfo['winrate']
#         scoreLead = bestMoveInfo['scoreLead']
#
#         anaPD.loc[len(anaPD)] = [name, turnMove, winrate, scoreLead]

def calulateDistance(originalMove, bestMoveInfo):
    original_x = originalMove[0]
    original_y = originalMove[1:]

    original_x_i = moveIndexes_low.index(original_x)
    original_y_i = int(original_y)

    best_x = bestMoveInfo[0]
    best_y = bestMoveInfo[1:]

    best_x_i = moveIndexes.index(best_x)
    best_y_i = int(best_y)

    return float(math.pow(math.pow(original_x_i-best_x_i, 2)+math.pow(original_y_i-best_y_i, 2), 0.5))

# def getvertextNumber_upper(turnMove):
#     original_x = turnMove[0]
#     original_y = turnMove[1:]
#
#     best_x_i = moveIndexes.index(original_x)
#     best_y_i = int(original_y)
#
#     return best_y_i*13+best_x_i

def getvertextNumber_upper(turnMove):
    original_x = turnMove[0]
    original_y = turnMove[1:]
    original_x_i = moveIndexes.index(original_x)
    original_y_i = int(original_y)-1
    return original_y_i*13+original_x_i

def changeToKata(originalBlackMove):
    original_x = originalBlackMove[0]
    original_y = originalBlackMove[1:]
    original_x_i = moveIndexes_low.index(original_x)
    return moveIndexes[original_x_i]+str(original_y)

def setDiffInfo(name, anaText, filePath):
    handi = filePath[-8:-7]
    for moveAnaReport in anaText:
        turnMove = moveAnaReport['turnNumber']

        if turnMove % 2 == 1:
            moveInfos = moveAnaReport['moveInfos']
            bestMoveInfo = moveInfos[0]
            winrate = bestMoveInfo['winrate']
            scoreLead = bestMoveInfo['scoreLead']
            if bestMoveInfo['move'] == 'pass':
                break
            ownbefore = moveAnaReport['ownership'][getvertextNumber_upper(bestMoveInfo['move'])]

            # get actual black move
            # filepath [search] (turnMove + 1)
            originalFilePath = '/home/fan/GoProjects/katago_Tools/dec_ana_good'+'/'+filePath[:-7]+"/"+filePath[:-7]+"_"+str(turnMove+1)+".ana"
            if os.path.exists(originalFilePath):
                with open(originalFilePath, 'r') as moveInfomation:
                    move_json = json.loads(moveInfomation.read())
                    originalBlackMove = move_json['moves'][move_json['analyzeTurns'][0]-1]
            else:
                break
            dis1b = calulateDistance(originalBlackMove[1], bestMoveInfo['move'])
            originalKataMove = changeToKata(originalBlackMove[1])

            shaperate = 0.001
            shapelog = math.log(shaperate)
            for moveAnaReport_ in anaText:
                turnMove_ = moveAnaReport_['turnNumber']
                moveInfos_ = moveAnaReport_['moveInfos']
                # init (visit = 2)
                for moveInfo in moveInfos_:
                        if originalKataMove == moveInfo['move']:
                            print('found it')
                            shaperate = moveInfo['prior']
                            shapelog = math.log(shaperate)
                if turnMove_ == (turnMove + 1):
                    bestMoveInfo_ = moveInfos_[0]
                    winrate_ = bestMoveInfo_['winrate']
                    scoreLead_ = bestMoveInfo_['scoreLead']
                    ownafter = moveAnaReport_['ownership'][getvertextNumber_upper(bestMoveInfo_['move'])]
                    anaPD_BA.loc[len(anaPD_BA)] = [name, handi, turnMove, shaperate, shapelog, winrate, winrate_, winrate_ - winrate, scoreLead,
                                                   scoreLead_, scoreLead_ - scoreLead, dis1b, ownbefore, ownafter, ownbefore-ownafter]

                    break

for anaFile_ in os.listdir(anaFileRoot):
    if not os.path.isdir(anaFile_):
        with open(anaFileRoot + '/' + anaFile_, 'rt') as anafile:
            anaText = json.loads(anafile.read())
            # print(anaText)
            nameWithType = os.path.basename(anaFile_)
            moveFileName = nameWithType[:-9]
            # handicap stones
            # setInfo(name=moveFileName, anaText=anaText)
            # file path
            # FAN --- here should be checked
            setDiffInfo(name=moveFileName, anaText=anaText, filePath=anaFile_)

# anaPD.to_csv('testAnaExcel.csv')
anaPD_BA.to_csv('testAnaGoodDiff.csv')
