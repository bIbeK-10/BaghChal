import numpy as np
import GRAPH as G


class GoatAgent:

    def __init__(self, board):
        self.score = 0
        self.current_board_state = board
        self.goat_count = 0
        self.Q_table = {}

    def select_move(self, goat_moves, tiger_moves):
        # Implement a reinforcement learning algorithm to select the best move.
        # Here, we will use a simple epsilon-greedy algorithm.

        epsilon = 0.1  # Exploration rate
        if np.random.rand() < epsilon:
            # Select a random move.
            index = np.random.randint(len(goat_moves))
            move_to_make = goat_moves[index]
        else:
            # Select the move with the highest Q-value.
            max_Q = -np.inf
            for move in goat_moves:
                Q = self.Q_table.get((self.current_board_state, move), 0)
                if Q > max_Q:
                    max_Q = Q
                    move_to_make = move

        self.track_own_goats(move_to_make)  # determine if the piece has been captured
        return move_to_make

    def track_own_goats(self, move_to_make):
        start, end = move_to_make[0:2], move_to_make[2:4]

        add_one = 0
        if start == end:
            add_one = 1  # goat added

        self.goat_count += add_one
        goat_on_board = self.count_goats() + add_one
        if goat_on_board + 1 == self.goat_count:
            self.goat_count -= 1

    def count_goats(self):
        count = 0
        flattened = self.current_board_state.reshape(-1, 1)
        for item in flattened:
            if item == "G":
                count += 1
        return count

    def reset_board(self):
        self.goat_count = 0

    def update_Q_table(self, reward, next_state, action, alpha=0.1, gamma=0.9):
        # Implement the Q-learning update rule.

        current_Q = self.Q_table.get((self.current_board_state, action), 0)
        max_next_Q = 0
        for next_move in G.get_valid_moves(next_state):
            next_Q = self.Q_table.get((next_state, next_move), 0)
            max_next_Q = max(max_next_Q, next_Q)

        new_Q = current_Q + alpha * (reward + gamma * max_next_Q - current_Q)
        self.Q_table[(self.current_board_state, action)] = new_Q


class TigerAgent:

    def __init__(self, board):
        self.score = 0
        self.current_board_state = board
        self.is_goat_captured = False
        self.Q_table = {}

    def select_move(self, goat_moves, tiger_moves):
        # Implement a reinforcement learning algorithm to select the best move.
        # Here, we will use a simple epsilon-greedy algorithm.

        epsilon = 0.1  # Exploration rate
        if np.random.rand() < epsilon:
            # Select a random move.
            index = np.random.randint(len(tiger_moves))
            move_to_make = tiger_moves[index]
        else:
            # Select the move with the highest Q-value.
            max_Q = -np.inf
            for move in tiger_moves:
                Q = self.Q_table.get((self.current_board_state, move), 0)
                if Q > max_Q:
                    max_Q = Q
                    move_to_make = move

        move_width = (np.abs(move_to_make[0] - move_to_make[2]),
                      np.abs(move_to_make[1]-move_to_make[3]))
        if move_width in G.DOUBLESTEP:
            self.score += 1
        return move_to_make

    def update_Q_table(self, reward, next_state, action, alpha=0.1, gamma=0.9):
        # Implement the Q-learning update rule.

        current_Q = self.Q_table.get((self.current_board_state, action), 0)
        max_next_Q = 0
        for next_move in G.get_valid_moves(next_state):
            next_Q = self.Q_table.get((next_state, next_move), 0)
            max_next_Q = max(max_next_Q, next_Q)

        new_Q = current_Q + alpha * (reward + gamma * max_next_Q - current_Q)
        self.Q_table[(self.current_board_state, action)] = new_Q


# Example usage:

board = np.array([["-"] * 9 for _ in range(9)])

goat_agent = GoatAgent(board)
tiger_agent = TigerAgent(board)

num_episodes = 10000

for episode in range(num_episodes):
    # Reset the board state.
    board = np.array([["-"] * 9 for _ in range(9)])

    # Play the game until one player wins.
    while True:
        # Get the goat's move.
        
        #### VALID MOVES MISSING
        goat_moves = G.get_valid_moves(board) 
        tiger_moves = []

        goat_move = goat_agent.select_move(goat_moves=goat_moves, tiger_moves=tiger_moves)

        # Update the board state.
        board[goat_move[0]][goat_move[1]] = "-"
        board[goat_move[2]][goat_move[3]] = "G"

        # Check if the goat has won.
        if goat_agent.count_goats() == 2:
            goat_agent.update_Q_table(1, board, goat_move)
            tiger_agent.update_Q_table(-1, board, goat_move)
            break

        # Get the tiger's move.

        ### VALID MOVES MISSING
        tiger_moves = G.get_valid_moves(board)

        tiger_move = tiger_agent.select_move(goat_moves=[], tiger_moves=tiger_moves)

        # Update the board state.
        board[tiger_move[0]][tiger_move[1]] = "-"
        board[tiger_move[2]][tiger_move[3]] = "T"

        # Check if the tiger has won.
        if tiger_agent.score == 3:
            goat_agent.update_Q_table(-1, board, tiger_move)
            tiger_agent.update_Q_table(1, board, tiger_move)
            break


