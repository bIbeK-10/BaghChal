# This file implements storing data and game logic

import numpy as np
import GRAPH as G

class GameState():

    def __init__(self):
        # '.' represents empty space, 'T' for Tiger and 'G' for Goat.

        self.board = np.array([  # initial state of the board
            ['T', '.', '.', '.', 'T'],
            ['.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.'],
            ['T', '.', '.', '.', 'T']
        ])

        self.goatToMove = True
        self.unusedGoats = 20
        self.moveLog = []
        self.lastGoatMove = [(-1,-1),(-1,-1)]
        self.lastTigerMove = [(-1,-1),(-1,-1)]

        self.isGoatCaptured = False
        self.capturedGoats = 0          # total number of goat captured by tiger
        self.goatValidMoves = self.getAllGoatMoves()
        self.tigerValidMoves = []

    def makeMove(self, move):
        if not self.goatToMove:
            stride = (np.abs(move.startRow - move.endRow), np.abs(move.startCol-move.endCol))
            if stride in G.DOUBLESTEP:
                self.isGoatCaptured = True

        if self.isGoatCaptured:
            capturePos = [(move.startRow + move.endRow)//2, (move.startCol + move.endCol)//2]
            self.board[capturePos[0]][capturePos[1]] = '.'
            self.capturedGoats += 1
            self.isGoatCaptured = False

        self.board[move.startRow][move.startCol] = '.'
        self.board[move.endRow][move.endCol] = move.pieceMoved

        if (move.startRow, move.startCol) == (move.endRow, move.endCol):
            self.board[move.endRow][move.endCol] = 'G'
            self.unusedGoats -= 1

        if self.goatToMove:
            self.lastGoatMove = [(move.startRow,move.startCol), (move.endRow, move.endCol)]
        else:
            self.lastTigerMove = [(move.startRow,move.startCol), (move.endRow, move.endCol)]

        self.goatToMove = not self.goatToMove

    def getAllGoatMoves(self):
        moves = []

        goatPos, tigerPos = self.piecesPos()
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if self.board[i][j] == '.' and self.unusedGoats !=0:
                    if [(i, j), (i, j)] != self.lastGoatMove:  # repeating move not allowed
                        moves.append([i, j, i, j])

                elif self.board[i][j] == 'G' and self.unusedGoats ==0:
                    connectedNodes = G.GRAPH1[(i, j)]
                    EmptyNodes = [node for node in connectedNodes if (node not in goatPos) and (node not in tigerPos)]

                    if self.lastGoatMove[0] in EmptyNodes:  # not allowed to repeat move
                        if self.lastGoatMove[1] == (i, j):
                            EmptyNodes.remove(self.lastGoatMove[0])

                    for node in EmptyNodes:
                        moves.append([i, j, node[0], node[1]])

        self.goatValidMoves = moves
        return moves

    def getAllTigerMoves(self):
        moves = []

        goatPos, tigerPos = self.piecesPos()
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if self.board[i][j] == 'T':
                    connectedNodes = []
                    for node in G.GRAPH1[(i, j)]:
                        if node not in goatPos and node not in tigerPos:  # not allowed to repeat move
                            connectedNodes.append(node)

                    if self.lastTigerMove[0] in connectedNodes:
                        if self.lastTigerMove[1] == (i, j):
                            connectedNodes.remove(self.lastTigerMove[0])

                    # tiger jumping criteria
                    doubleStep = G.GRAPH2[(i, j)]
                    validDoubleSteps = []
                    for nextPos in doubleStep:
                        row, col = (i + nextPos[0]) // 2, (j + nextPos[1]) // 2
                        if self.board[row][col] == 'G' and self.board[nextPos[0]][nextPos[1]] == '.':
                            validDoubleSteps.append(nextPos)

                    possibleNodes = connectedNodes + validDoubleSteps
                    for node in possibleNodes:
                        moves.append([i, j, node[0], node[1]])

        self.tigerValidMoves = moves
        return moves

    def getNextGoatMoves(self):
        nextGoatMoves = []
        tigerValidMoves = getNextTigerMoves(self.board, self.lastTigerMove)

        for move in tigerValidMoves:
            board = self.board.copy()

            board[move[0]][move[1]] = '.'
            board[move[2]][move[3]] = 'T'
            if (np.abs(move[0]-move[2]), np.abs(move[1]-move[3])) in G.DOUBLESTEP:
                board[(move[0] + move[2])//2][(move[1] + move[3])//2] = '.'

            moves = getNextGoatMoves(board, self.unusedGoats, self.lastGoatMove)
            for move in moves:
                if move not in nextGoatMoves:
                    nextGoatMoves.append(move)

        return nextGoatMoves

    def getNextTigerMoves(self):
        nextTigerMoves = []
        goatValidMoves = getNextGoatMoves(self.board, self.unusedGoats, self.lastGoatMove)

        for move in goatValidMoves:
            board = self.board.copy()
            board[move[0]][move[1]] = '.'
            board[move[2]][move[3]] = 'G'

            moves = getNextTigerMoves(board,self.lastTigerMove)
            for move in moves:
                if move not in nextTigerMoves:
                    nextTigerMoves.append(move)

        return nextTigerMoves

    def piecesPos(self):
        goatPosition = []
        tigerPosition = []
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if self.board[i][j] == 'T':
                    tigerPosition.append((i,j))
                elif self.board[i][j] == 'G':
                    goatPosition.append((i,j))
        return goatPosition, tigerPosition

    def restart(self):
        newState = GameState()
        return newState

def getNextGoatMoves(board, unusedGoats, lastGoatMove):
    moves = []

    goatPos, tigerPos = piecesPos(board)
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i][j] == '.' and unusedGoats != 0:
                if [(i, j), (i, j)] != lastGoatMove:  # repeating move not allowed
                    moves.append([i, j, i, j])
            elif board[i][j] == 'G' and unusedGoats == 0:
                connectedNodes = G.GRAPH1[(i, j)]
                EmptyNodes = [node for node in connectedNodes if (node not in goatPos) and (node not in tigerPos)]

                if lastGoatMove[0] in EmptyNodes:  # not allowed to repeat move
                    if lastGoatMove[1] == (i, j):
                        EmptyNodes.remove(lastGoatMove[0])

                for node in EmptyNodes:
                    moves.append([i, j, node[0], node[1]])
    return moves

def getNextTigerMoves(board, lastTigerMove):
    moves = []

    goatPos, tigerPos = piecesPos(board)
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i][j] == 'T':
                connectedNodes = []
                for node in G.GRAPH1[(i, j)]:
                    if node not in goatPos and node not in tigerPos:  # not allowed to repeat move
                        connectedNodes.append(node)

                if lastTigerMove[0] in connectedNodes:
                    if lastTigerMove[1] == (i, j):
                        connectedNodes.remove(lastTigerMove[0])

                # tiger jumping criteria
                doubleStep = G.GRAPH2[(i, j)]
                validDoubleSteps = []
                for nextPos in doubleStep:
                    row, col = (i + nextPos[0]) // 2, (j + nextPos[1]) // 2
                    if board[row][col] == 'G' and board[nextPos[0]][nextPos[1]] == '.':
                        validDoubleSteps.append(nextPos)

                possibleNodes = connectedNodes + validDoubleSteps
                for node in possibleNodes:
                    moves.append([i, j, node[0], node[1]])

    return moves

def piecesPos(board):
    goatPosition = []
    tigerPosition = []
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i][j] == 'T':
                tigerPosition.append((i,j))
            elif board[i][j] == 'G':
                goatPosition.append((i,j))
    return goatPosition, tigerPosition

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