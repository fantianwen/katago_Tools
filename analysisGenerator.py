#!/usr/bin/env python

import sgf
import matplotlib.pyplot as pyplot
import os

locationdic = "abcdefghjklmn"


def transferMoveLocation(location):
    x = location[:1]
    y = location[1:2]
    new_y = int(locationdic.find(y)) + 1
    return x + str(new_y)


def getInitialMoves(moves, handicapStoneNumber):
    initialMovesStr = ''

    if handicapStoneNumber == 0:
        return initialMovesStr

    initialMovesStr += '['
    for i in range(handicapStoneNumber):
        initialMovesStr += '["B","' + transferMoveLocation(moves[i]) + '"],'
    initialMovesStr = initialMovesStr[0:len(initialMovesStr) - 1]
    initialMovesStr += ']'
    return initialMovesStr


def getMoves(moves, handicapStoneNumber):
    movesStr = ''
    movesStr += '['
    for i in range(handicapStoneNumber, len(moves)):
        if i%2 == 0:
            movesStr += '["W","' + transferMoveLocation(moves[i]) + '"],'
        else:
            movesStr += '["B","' + transferMoveLocation(moves[i]) + '"],'
    movesStr = movesStr[0:len(movesStr) - 1]
    movesStr += ']'
    return movesStr


def parseWinrate(filePath):
    winrates = []
    moves = []
    komi = ''
    with open(filePath) as f:
        collection = sgf.parse(f.read())
        children = collection.children
        gameTree = children[0]

        handicapStones = 1

        for node in gameTree.nodes:
            for property in node.properties:

                if property == 'KM':
                    komi = node.properties[property]

                if property == 'B' or property == 'W':
                    move = node.properties[property]
                    print(move[0])
                    if move[0] != 'tt':
                        moves.append(move[0])
                    else:
                        handicapStones += 1

                if property == 'C':
                    comments = node.properties[property]
                    _comments = ''.join(comments)
                    if _comments.strip() != '':
                        json_tuple = {}
                        json_tuple['id'] = 'test'

                        json_tuple['initailStones'] = getInitialMoves(moves, handicapStones)

                        json_tuple['moves'] = getMoves(moves, handicapStones)

                        json_tuple['rules'] = 'tromp-taylor'

                        json_tuple['komi'] = komi

                        json_tuple['boardXSize'] = 13

                        json_tuple['boardYSize'] = 13

                        json_tuple['analyzeTurns'] = len(moves)-handicapStones

                        print(json_tuple)

        f.close()


parseWinrate("/home/radasm/GoProjects/Go_data/detection/Kat01_cho_0323_1.sgf")
