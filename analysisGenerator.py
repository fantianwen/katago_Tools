#!/usr/bin/env python

import sgf
import matplotlib.pyplot as pyplot
import os
import json

locationdic = "abcdefghijklmn"

totalMoves = 0


def transferMoveLocation(location):
    x = location[:1]
    new_x = x
    x_index = int(locationdic.find(x))
    if x_index >= 8:
        new_x = locationdic[x_index + 1]

    y = location[1:2]
    y_index = int(locationdic.find(y))
    new_y = 13 - y_index
    return new_x + str(new_y)


def getInitialMoves(moves, handicapStoneNumber):
    initialMovesStr = []

    if handicapStoneNumber == 0:
        return initialMovesStr

    for i in range(handicapStoneNumber):
        moveBlock = []
        moveBlock.append("B")
        moveBlock.append(transferMoveLocation(moves[i]))
        initialMovesStr.append(moveBlock)

    return initialMovesStr


def getMoves(moves, handicapStoneNumber):
    movesStr = []
    for i in range(handicapStoneNumber, len(moves)):
        moveBlock = []
        if i % 2 == 0:
            moveBlock.append("W")
        else:
            moveBlock.append("B")
        moveBlock.append(transferMoveLocation(moves[i]))
        movesStr.append(moveBlock)
    return movesStr


def saveToFile(json_tuple, fileName, turnNumber):
    fileFolderName = fileName[:-4]
    _rootfile = '/home/radasm/GoProjects/katago_Tools/dec_ana_good/' + fileFolderName
    if not os.path.exists(_rootfile):
        os.mkdir(_rootfile)
    fileObject = open(_rootfile + "/" + fileFolderName + "_" + str(turnNumber) + ".ana", 'w')
    fileObject.write(str(json_tuple))
    fileObject.close()


def deleteFile(fileName, turnNumber):
    fileFolderName = fileName[:-4]
    _rootfile = '/home/radasm/GoProjects/katago_Tools/dec_ana_good/' + fileFolderName
    if not os.path.exists(_rootfile):
        os.mkdir(_rootfile)
    forDeleteFile1 = _rootfile + "/" + fileFolderName + "_" + str(turnNumber) + ".ana"
    forDeleteFile2 = _rootfile + "/" + fileFolderName + "_" + str(turnNumber-1) + ".ana"
    if os.path.exists(forDeleteFile1):
        os.remove(forDeleteFile1)
    if os.path.exists(forDeleteFile2):
        os.remove(forDeleteFile2)

def parseForAnalysis(filePath):
    moves = []
    komi = ''
    begin = False
    with open(filePath) as f:
        collection = sgf.parse(f.read())
        children = collection.children
        gameTree = children[0]

        analysisTurns = []
        json_tuple = {}

        handicapStones = 1

        for node in gameTree.nodes:
            for property in node.properties:

                if property == 'KM':
                    komis = node.properties[property]
                    komi = komis[0]

                if property == 'B' or property == 'W':
                    move = node.properties[property]
                    # print(move[0])
                    if move[0] != 'tt':
                        moves.append(move[0])
                    else:
                        handicapStones += 1

                if property == 'W':
                    move = node.properties[property]
                    if move[0] != 'tt':
                        begin = True

                if begin:
                    analysisTurns.clear()

                    analysisTurns.append(len(moves) - handicapStones - 1)

                    json_tuple["id"] = os.path.basename(filePath)

                    json_tuple['initialStones'] = getInitialMoves(moves, handicapStones)

                    json_tuple['moves'] = getMoves(moves, handicapStones)

                    json_tuple['rules'] = 'tromp-taylor'

                    json_tuple['komi'] = float(komi)

                    json_tuple['boardXSize'] = 13

                    json_tuple['boardYSize'] = 13

                    json_tuple['maxVisits'] = 2000

                    json_tuple['analyzeTurns'] = analysisTurns
                    saveToFile(json.dumps(json_tuple), os.path.basename(filePath), len(moves) - handicapStones)

                # if property == 'C':
                #     comments = node.properties[property]
                #     _comments = ''.join(comments)
                #     if _comments.strip() != '':
                #         analysisTurns.clear()
                #
                #         analysisTurns.append(len(moves) - handicapStones - 1)
                #
                #         json_tuple["id"] = os.path.basename(filePath)
                #
                #         json_tuple['initialStones'] = getInitialMoves(moves, handicapStones)
                #
                #         json_tuple['moves'] = getMoves(moves, handicapStones)
                #
                #         json_tuple['rules'] = 'tromp-taylor'
                #
                #         json_tuple['komi'] = float(komi)
                #
                #         json_tuple['boardXSize'] = 13
                #
                #         json_tuple['boardYSize'] = 13
                #
                #         json_tuple['maxVisits'] = 1600
                #
                #         json_tuple['analyzeTurns'] = analysisTurns
                #         saveToFile(json.dumps(json_tuple), os.path.basename(filePath), len(moves) - handicapStones - 1)
                #
                #         analysisTurns.clear()
                #         analysisTurns.append(len(moves) - handicapStones)
                #
                #         json_tuple["id"] = os.path.basename(filePath)
                #
                #         json_tuple['initialStones'] = getInitialMoves(moves, handicapStones)
                #
                #         json_tuple['moves'] = getMoves(moves, handicapStones)
                #
                #         json_tuple['rules'] = 'tromp-taylor'
                #
                #         json_tuple['komi'] = float(komi)
                #
                #         json_tuple['boardXSize'] = 13
                #
                #         json_tuple['boardYSize'] = 13
                #
                #         json_tuple['maxVisits'] = 1600
                #
                #         json_tuple['analyzeTurns'] = analysisTurns
                #         saveToFile(json.dumps(json_tuple), os.path.basename(filePath), len(moves) - handicapStones)
                if property == 'C':
                    comments = node.properties[property]
                    _comments = ''.join(comments)
                    if _comments.strip() != '':
                        deleteFile(os.path.basename(filePath), len(moves) - handicapStones)

        f.close()
        # print(len(moves)-handicapStones-1)
        return len(moves)-handicapStones-1


RootPath = '/home/radasm/GoProjects/Go_data/detection'

files = os.listdir(RootPath)
s = []
moveNumbers = 0
sgfNumber = 0

for file in files:
    if not os.path.isdir(file):
        sgfNumber += 1
        moveNumbers += parseForAnalysis(RootPath + "/" + file)

print(sgfNumber)
print(moveNumbers)
