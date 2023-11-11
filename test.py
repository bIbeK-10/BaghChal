import BaghchalEngine as Engine
import BaghchalAgent as Agent
import numpy as np

Q_table_goat = {
                ('T...T...............T...T', '2222'):1,
                ('....T.T.....G.......T...T', '2222'):1,
                }

Q_table_tiger = {
                ('T...T.......G.......T...T', '0011'):1,
                }

gs = Engine.GameState()


Goat = Agent.GoatAgent(gs.board)
Goat.Q_table = Q_table_goat
moves = gs.getAllGoatMoves()

goatBestMove = Goat.maxQmove(moves)
gs.board = np.array([  # initial state of the board
            ['T', '.', '.', '.', 'T'],
            ['.', '.', '.', '.', '.'],
            ['.', '.', 'G', '.', '.'],
            ['.', '.', '.', '.', '.'],
            ['T', '.', '.', '.', 'T']
        ])

nextMoves = gs.getNextGoatMoves()
print(nextMoves)
Goat.update_Q_table(1, )