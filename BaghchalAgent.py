# work on bot interface
import numpy as np
class Agent:

    def __init__(self, role):
        self.role = role
        self.score = 0

    def selectMove(self, goatMoves, tigerMoves):
        np.random.seed(123)
        if self.role == 'G':
            index = np.random.randint(len(goatMoves))
            moveToMake = goatMoves[index]
            return moveToMake
        elif self.role == 'B':
            index = np.random.randint(len(tigerMoves))
            moveToMake = tigerMoves[index]
            return moveToMake