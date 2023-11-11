from datetime import datetime

import numpy as np
import pygame.time

import BaghchalEngine
import GRAPH as G

class GoatAgent:

    def __init__(self, board):
        self.score = 0
        self.current_board_state = board
        self.Q_table = {}
        self.totalGamesPlayed = 0
        self.nextValidMoves = []
        self.epsilon = 1

    def select_move(self, goat_moves):
        # Implement a reinforcement learning algorithm to select the best move.

        # Here, we will use a simple epsilon-greedy algorithm.
        move_to_make = []
        if np.random.rand() < self.epsilon:
            # Select a random move.
            index = np.random.randint(len(goat_moves))
            move_to_make = goat_moves[index]
        else:
            # Select the move with the highest Q-value.
            move_to_make = self.maxQmove(goat_moves)

        return move_to_make

    def maxQmove(self, goat_moves):
        move_to_make = []
        max_Q = -np.inf
        for move in goat_moves:
            Q = self.Q_table.get(self.getState_n_Action(self.current_board_state, move), 0)
            if Q > max_Q:
                max_Q = Q
                move_to_make = move
        if max_Q == 0:
            move_to_make = goat_moves[np.random.randint(len(goat_moves))]
        return move_to_make

    def reset_board(self):
        self.goat_count = 0

    def update_Q_table(self, reward, next_state, action, alpha=0.1, gamma=0.9):
        # Implement the Q-learning update rule.

        self.score += reward
        current_Q = self.Q_table.get(self.getState_n_Action(self.current_board_state, action), 0)
        max_next_Q = 0
        gs.getAllGoatMoves()
        for next_move in self.nextValidMoves:
            next_Q = self.Q_table.get(self.getState_n_Action(next_state, next_move), 0)
            max_next_Q = max(max_next_Q, next_Q)

        new_Q = current_Q + alpha * (reward + gamma * max_next_Q - current_Q)
        self.Q_table[self.getState_n_Action(self.current_board_state, action)] = new_Q

    def getState_n_Action(self, currentBoardState,  move):
        currentState = "".join(currentBoardState.reshape(1, -1)[0])

        # same state can exist in multiple rotation form, this gets a single representation
        mergedRotations = self.checkSymmetry(currentState, move)

        return (mergedRotations)

    def checkSymmetry(self, currentState, move):
        rotation_states = []
        moveToRotate = move
        next_state = currentState

        # roatation symmetry
        i = 0
        while i < 4:
            state = next_state

            s_rot = ''
            s_rot += state[4] + state[9] + state[14] + state[19] + state[24]
            s_rot += state[3] + state[8] + state[13] + state[18] + state[23]
            s_rot += state[2] + state[7] + state[12] + state[17] + state[22]
            s_rot += state[1] + state[6] + state[11] + state[16] + state[21]
            s_rot += state[0] + state[5] + state[10] + state[15] + state[20]

            startRotate = G.ROTATION[(moveToRotate[0], moveToRotate[1])]
            endRotate = G.ROTATION[(moveToRotate[2], moveToRotate[3])]
            moveToRotate = [startRotate[0], startRotate[1], endRotate[0], endRotate[1]]

            rotation_state = (
            s_rot, str(moveToRotate[0]) + str(moveToRotate[1]) + str(moveToRotate[2]) + str(moveToRotate[3]))
            rotation_states.append(rotation_state)

            s = s_rot
            # reflect along x = -y
            s_nxy = ''
            s_nxy += s[0] + s[5] + s[10] + s[15] + s[20]
            s_nxy += s[1] + s[6] + s[11] + s[16] + s[21]
            s_nxy += s[2] + s[7] + s[12] + s[17] + s[22]
            s_nxy += s[3] + s[8] + s[13] + s[18] + s[23]
            s_nxy += s[4] + s[9] + s[14] + s[19] + s[24]

            m = str(moveToRotate[1]) + str(moveToRotate[0]) + str(moveToRotate[3]) + str(moveToRotate[2])
            rotation_states.append((s_nxy, m))

            # reflect along x = 0
            s_x = 0
            s_x = s[20:25] + s[15:20] + s[10:15] + s[5:10] + s[0:5]

            m = str(4 - moveToRotate[0]) + str(moveToRotate[1]) + str(4 - moveToRotate[2]) + str(moveToRotate[3])
            rotation_states.append((s_x, m))

            # reflect along x = y
            s_xy = ''
            s_xy += s[24] + s[19] + s[14] + s[9] + s[4]
            s_xy += s[23] + s[18] + s[13] + s[8] + s[3]
            s_xy += s[22] + s[17] + s[12] + s[7] + s[2]
            s_xy += s[21] + s[16] + s[11] + s[6] + s[1]
            s_xy += s[20] + s[15] + s[10] + s[5] + s[0]

            m = str(4 - moveToRotate[1]) + str(4 - moveToRotate[0]) + str(4 - moveToRotate[3]) + str(
                4 - moveToRotate[2])
            rotation_states.append((s_xy, m))

            # reflect along y = 0
            s_y = s[0:5][::-1] + s[5:10][::-1] + s[10:15][::-1] + s[15:20][::-1] + s[20:25][::-1]

            m = str(moveToRotate[0]) + str(4 - moveToRotate[1]) + str(moveToRotate[2]) + str(4 - moveToRotate[3])
            rotation_states.append((s_y, m))

            next_state = s_rot
            moveToRotate = [startRotate[0], startRotate[1], endRotate[0], endRotate[1]]
            i += 1

        keys = self.Q_table.keys()
        for state in rotation_states:
            if state in keys:
                return state

        return (currentState, str(move[0]) + str(move[1]) + str(move[2]) + str(move[3]))

    def updateEpsilon(self):
        if self.totalGamesPlayed % 1000 == 0 and self.epsilon > 0.2:
            self.epsilon -= 0.05

class TigerAgent:

    def __init__(self, board):
        self.score = 0
        self.current_board_state = board
        self.capturedGoats = 0
        self.Q_table = {}
        self.nextValidMoves = []

    def select_move(self, tiger_moves):
        # Implement a reinforcement learning algorithm to select the best move.
        # Here, we will use a simple epsilon-greedy algorithm.

        move_to_make = []
        epsilon = 0.8  # Exploration rate
        if np.random.rand() < epsilon:
            # Select a random move.
            index = np.random.randint(len(tiger_moves))
            move_to_make = tiger_moves[index]
            for move in tiger_moves:
                if self.isDoubleStep(move):
                    self.capturedGoats += 1
                    return move
        else:
            # Select the move with the highest Q-value.
            move_to_make = self.maxQMove(tiger_moves)

        if self.isDoubleStep(move_to_make):
            self.capturedGoats += 1
        return move_to_make

    def maxQMove(self, tiger_moves):
        move_to_make = []
        max_Q = -np.inf

        for move in tiger_moves:
            Q = self.Q_table.get(self.getState_n_Action(self.current_board_state, move), 0)
            if Q > max_Q:
                max_Q = Q
                move_to_make = move
        return move_to_make

    def update_Q_table(self, reward, next_state, action, alpha=0.1, gamma=0.9):
        # Implement the Q-learning update rule.
        self.score += reward
        current_Q = self.Q_table.get(self.getState_n_Action(self.current_board_state, action), 0)
        max_next_Q = 0

        for next_move in self.nextValidMoves:
            next_Q = self.Q_table.get(self.getState_n_Action(next_state, next_move), 0)
            max_next_Q = max(max_next_Q, next_Q)

        new_Q = current_Q + alpha * (reward + gamma * max_next_Q - current_Q)
        self.Q_table[self.getState_n_Action(self.current_board_state, action)] = new_Q

    def isDoubleStep(self, move):
        move_width = (np.abs(move[0] - move[2]), np.abs(move[1] - move[3]))
        if move_width in G.DOUBLESTEP:
            return True
        return False

    def getState_n_Action(self, currentBoardState,  move):
        currentState = "".join(currentBoardState.reshape(1, -1)[0])

        # same state can exist in multiple rotation form, this gets a single representation
        mergedRotations = self.checkSymmetry(currentState, move)

        return (mergedRotations)

    def checkSymmetry(self, currentState, move):
        rotation_states = []
        moveToRotate = move
        next_state = currentState

        # roatation symmetry
        i = 0
        while i<4:
            state = next_state

            s_rot = ''
            s_rot += state[4] + state[9] + state[14] + state[19] + state[24]
            s_rot += state[3] + state[8] + state[13] + state[18] + state[23]
            s_rot += state[2] + state[7] + state[12] + state[17] + state[22]
            s_rot += state[1] + state[6] + state[11] + state[16] + state[21]
            s_rot += state[0] + state[5] + state[10] + state[15] + state[20]

            startRotate = G.ROTATION[(moveToRotate[0], moveToRotate[1])]
            endRotate   = G.ROTATION[(moveToRotate[2], moveToRotate[3])]
            moveToRotate =  [startRotate[0], startRotate[1], endRotate[0], endRotate[1]]

            rotation_state = (s_rot, str(moveToRotate[0]) + str(moveToRotate[1]) + str(moveToRotate[2]) + str(moveToRotate[3]))
            rotation_states.append(rotation_state)

            s = s_rot
            # reflect along x = -y
            s_nxy = ''
            s_nxy += s[0] + s[5] + s[10] + s[15] + s[20]
            s_nxy += s[1] + s[6] + s[11] + s[16] + s[21]
            s_nxy += s[2] + s[7] + s[12] + s[17] + s[22]
            s_nxy += s[3] + s[8] + s[13] + s[18] + s[23]
            s_nxy += s[4] + s[9] + s[14] + s[19] + s[24]

            m = str(moveToRotate[1]) + str(moveToRotate[0]) + str(moveToRotate[3]) + str(moveToRotate[2])
            rotation_states.append((s_nxy, m))

            # reflect along x = 0
            s_x = 0
            s_x = s[20:25] + s[15:20] + s[10:15] + s[5:10] + s[0:5]

            m = str(4-moveToRotate[0]) + str(moveToRotate[1]) + str(4-moveToRotate[2]) + str(moveToRotate[3])
            rotation_states.append((s_x, m))

            # reflect along x = y
            s_xy = ''
            s_xy += s[24] + s[19] + s[14] + s[9] + s[4]
            s_xy += s[23] + s[18] + s[13] + s[8] + s[3]
            s_xy += s[22] + s[17] + s[12] + s[7] + s[2]
            s_xy += s[21] + s[16] + s[11] + s[6] + s[1]
            s_xy += s[20] + s[15] + s[10] + s[5] + s[0]

            m = str(4-moveToRotate[1]) + str(4-moveToRotate[0]) + str(4-moveToRotate[3]) + str(4-moveToRotate[2])
            rotation_states.append((s_xy, m))

            # reflect along y = 0
            s_y = s[0:5][::-1] + s[5:10][::-1] + s[10:15][::-1] + s[15:20][::-1] + s[20:25][::-1]

            m = str(moveToRotate[0]) + str(4-moveToRotate[1]) + str(moveToRotate[2]) + str(4-moveToRotate[3])
            rotation_states.append((s_y, m))

            next_state = s_rot
            moveToRotate = [startRotate[0], startRotate[1], endRotate[0], endRotate[1]]
            i+=1

        keys = self.Q_table.keys()
        for state in rotation_states:
            if state in keys:
                return state


        return (currentState, str(move[0]) + str(move[1]) + str(move[2]) + str(move[3]))

def train(goat_agent, tiger_agent, num_episodes = 1):

    goat_wins = 0
    # episode = 0
    # while goat_wins < 5:
    for episode in range(num_episodes):
        if episode % 1000 == 0:
            currentTime = (datetime.now()).strftime('%H:%M:%S.%f')
            print(f"Iteration {episode} : {currentTime} : exploration rate: {goat_agent.epsilon}")
        # episode += 1

        # Reset the board state.
        gs = BaghchalEngine.GameState()

        # Play the game until one player wins.
        per_round = 0
        nextRound = False
        goat_to_move = True
        previous_tiger_moves = []
        while True:
            # Get the goat's move.

            reward = {'goat':0, 'tiger':0}
            goat_moves = gs.getAllGoatMoves()
            goat_agent.current_board_state = gs.board
            goat_move = []


            if goat_to_move:
                goat_move = goat_agent.select_move(goat_moves)
                # make move
                gs.makeMove(BaghchalEngine.Move((goat_move[0], goat_move[1]),(goat_move[2], goat_move[3]), gs.board))
                goat_to_move = False
                per_round += 1

            # compute next valid moves for goat
            goat_agent.nextValidMoves = gs.getNextGoatMoves()

            # Get the tiger's move.
            tiger_moves = gs.getAllTigerMoves()
            tiger_agent.current_board_state = gs.board
            tiger_move = []

            if not goat_to_move and len(tiger_moves) != 0:
                tiger_move = tiger_agent.select_move(tiger_moves)

                # Update the board state.
                gs.makeMove(BaghchalEngine.Move((tiger_move[0], tiger_move[1]), (tiger_move[2], tiger_move[3]), gs.board))
                goat_to_move = True
                per_round += 1

            # compute next valid moves for tiger
            tiger_agent.nextValidMoves = gs.getNextTigerMoves()

            # reward every turn
            if per_round == 2:
                per_round = 0
                # if goat is captured, reward tiger and penalize goat.
                if tiger_agent.isDoubleStep(tiger_move):
                    reward['goat'] += -1.5
                    reward['tiger'] += 1

                # else, since goat survived, reward goat by small amount.
                else:
                    reward['goat'] += 0.5

                    # if goat occupied tiger capture positions, reward goat
                    for move in previous_tiger_moves:
                        if tiger_agent.isDoubleStep(move) and goat_move[2:4] == move[2:4]:
                            reward['goat'] += 2
                        else:   # penalize goat for not choosing that move
                            reward['goat'] += -1

                    # if piece placed in a corner, give points
                    if goat_move[2:4] in G.CORNERS:
                        reward['goat'] += 1

            # Check if the goat has won.
            if len(tiger_moves) == 0 and not goat_to_move:
                tiger_move = [2, 2, 2, 2]
                reward['goat'] += 1
                reward['tiger'] += -1
                if gs.unusedGoats > 15:     # if more than 15 goats used, reward the goat
                    reward['goat'] += 1
                goat_wins += 1
                nextRound = True

            # Check if the tiger has won.
            if tiger_agent.capturedGoats >= 5:
                reward['goat'] += -1
                reward['tiger'] += 1
                if gs.unusedGoats > 15:     # if more than 15 goats used, reward the goat
                    reward['goat'] += 4
                gs= gs.restart()
                nextRound = True

            goat_agent.update_Q_table(reward['goat'], tiger_agent.current_board_state, goat_move)
            tiger_agent.update_Q_table(reward['tiger'], gs.board, tiger_move)
            previous_tiger_moves = tiger_moves

            # backpropagate final outcome rewards and penalties
            if nextRound:
                goat_agent.update_Q_table(reward['goat'], tiger_agent.current_board_state, goat_move)
                tiger_agent.update_Q_table(reward['tiger'], gs.board, tiger_move)
                tiger_agent.capturedGoats = 0
                goat_agent.totalGamesPlayed += 1
                goat_agent.updateEpsilon()
                break

gs = BaghchalEngine.GameState()
# train(GoatAgent(gs.board), TigerAgent(gs.board), 1)