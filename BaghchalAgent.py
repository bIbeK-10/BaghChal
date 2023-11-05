# work on bot interface
import numpy as np
import GRAPH as G
class GoatAgent:

    def __init__(self,board):
        self.score = 0
        self.currentBoardState = board
        self.goatCount = 0

    def selectMove(self, goatMoves, tigerMoves):
        # np.random.seed(123)
        index = np.random.randint(len(goatMoves))
        moveToMake = goatMoves[index]
        self.trackOwnGoats(moveToMake)              # determine if the piece has been captured
        return moveToMake

    def trackOwnGoats(self, moveToMake):
        start, end = moveToMake[0:2], moveToMake[2:4]

        addOne = 0
        if start == end:
            addOne = 1  # goat added

        self.goatCount += addOne
        goatOnBoard = self.countGoat() + addOne
        if goatOnBoard + 1 == self.goatCount:
            self.goatCount -= 1

    def countGoat(self):
        count = 0
        flattened = self.currentBoardState.reshape(-1, 1)
        for item in flattened:
            if item == 'G':
                count+=1
        return count

    def resetBoard(self):
        self.goatCount = 0

class TigerAgent:

    def __init__(self, board):
        self.score = 0
        self.currentBoardState = board
        self.isGoatCaptured = False

    def selectMove(self, goatMoves, tigerMoves):
        # np.random.seed(123)
        index = np.random.randint(len(tigerMoves))
        moveToMake = tigerMoves[index]
        moveWidth = (np.abs(moveToMake[0] - moveToMake[2]),np.abs(moveToMake[1]-moveToMake[3]))
        if moveWidth in G.DOUBLESTEP:
            self.score += 1
        return moveToMake