# This file implements storing data and game logic

import numpy as np
import GRAPH as G

class GameState():

    def __init__(self):
        # '.' represents empty space, 'B' for Tiger and 'G' for Goat.

        self.board = np.array([  # initial state of the board
            ['B', '.', '.', '.', 'B'],
            ['.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.'],
            ['B', '.', '.', '.', 'B']
        ])

        self.goatToMove = True
        self.unusedGoats = 20
        self.moveLog = []
        self.lastGoatMove = [(-1,-1),(-1,-1)]
        self.lastTigerMove = [(-1,-1),(-1,-1)]

        self.goatCaptured = False
        self.capturedGoats = 0          # total number of goat captured by tiger
        self.goatValidMoves = []
        self.tigerValidMoves = []

    def makeMove(self, move):
        if not self.goatToMove:
            stride = (np.abs(move.startRow - move.endRow),np.abs(move.startCol-move.endCol))
            if stride in G.DOUBLESTEP:
                self.goatCaptured = True

        if self.goatCaptured:
            capturePos = [(move.startRow + move.endRow)//2,(move.startCol + move.endCol)//2]
            self.board[capturePos[0]][capturePos[1]] = '.'
            self.capturedGoats += 1
            self.goatCaptured = False

        self.board[move.startRow][move.startCol] = '.'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        if move.pieceMoved == '.':
            self.board[move.endRow][move.endCol] = 'G'
        self.moveLog.append(move)

        if self.goatToMove:
            self.lastGoatMove = [(move.startRow,move.startCol), (move.endRow, move.endCol)]
        else:
            self.lastTigerMove = [(move.startRow,move.startCol), (move.endRow, move.endCol)]

        self.goatToMove = not self.goatToMove

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.goatToMove = not self.goatToMove  # switch turn back

    def getAllPosssibleMoves(self):
        moves = []
        self.goatValidMoves = []
        self.tigerValidMoves = []

        piecePositions = self.piecesPos()

        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):

                piece = self.board[i][j]
                if self.goatToMove:
                    if piece == '.' and self.unusedGoats !=0:
                        self.getNewGoat(i, j, moves)
                    elif piece == 'G' and self.unusedGoats ==0:
                        self.getGoatMoves(i, j, moves, piecePositions[0], piecePositions[1])

                elif not self.goatToMove and piece == 'B':
                    self.getTigerMoves(i, j, moves, piecePositions[0], piecePositions[1])

        return moves

    # move a new goat piece to the board
    def getNewGoat(self, i, j, moves):
        if [(i, j), (i, j)] == self.lastGoatMove: # repeating move not allowed
            return
        moves.append(Move((i, j), (i, j), self.board))
        self.goatValidMoves.append([i, j, i, j])

    # moves of an existing goat piece on the board
    def getGoatMoves(self, i, j, moves, goatPos, tigerPos):
        connectedNodes = G.GRAPH1[(i,j)]
        EmptyNodes = [node for node in connectedNodes if (node not in goatPos) and (node not in tigerPos)]

        if self.lastGoatMove[0] in EmptyNodes:  # not allowed to repeat move
            if self.lastGoatMove[1] == (i,j):
                EmptyNodes.remove(self.lastGoatMove[0])

        for node in EmptyNodes:
            self.goatValidMoves.append([i,j,node[0],node[1]])
            moves.append(Move((i,j),node,self.board))

    # moves of the tiger on the board
    def getTigerMoves(self, i, j, moves, goatPos, tigerPos):

        connectedNodes = []
        for node in G.GRAPH1[(i,j)]:
            if node not in goatPos and node not in tigerPos:    # not allowed to repeat move
                connectedNodes.append(node)

        if self.lastTigerMove[0] in connectedNodes:
            if self.lastTigerMove[1] == (i, j):
                connectedNodes.remove(self.lastTigerMove[0])

        # tiger jumping criteria
        doubleStep = G.GRAPH2[(i,j)]
        validDoubleSteps = []
        for nextPos in doubleStep:
            row, col = (i+nextPos[0])//2,(j+nextPos[1])//2
            if self.board[row][col] == 'G' and self.board[nextPos[0]][nextPos[1]] == '.':
                validDoubleSteps.append(nextPos)

        possibleNodes = connectedNodes + validDoubleSteps
        for node in possibleNodes:
            self.tigerValidMoves.append([i,j,node[0],node[1]])
            moves.append(Move((i,j),node,self.board))

    def piecesPos(self):
        goatPosition = []
        tigerPosition = []
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if self.board[i][j] == 'B':
                    tigerPosition.append((i,j))
                elif self.board[i][j] == 'G':
                    goatPosition.append((i,j))

        return goatPosition, tigerPosition

    def restart(self):
        print("Game Restart")
        return GameState(), self.getAllPosssibleMoves()


class Move():
    # maps keys to values
    # key : value
    ranksToRows = {'1': 4, '2': 3, '3': 2, '4': 1, '5': 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow, self.startCol]
        self.pieceCaptured = board[self.endRow, self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    # Override '=' notation to determine equivalent move
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def addGoatNotation(self):
        return '+' + self.getRankFile(self.startRow, self.startCol)

    def getNotation(self):
        # notation similar to chess
        notation = self.pieceMoved + self.getRankFile(self.endRow, self.endCol)

        if self.pieceCaptured == 'G':
            notation = self.pieceMoved + 'x' + notation[1:]

        return notation

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]