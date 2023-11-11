# handle input output and current game state

import pygame as pg
import pygame.time

import BaghchalEngine
import BaghchalAgent

WIDTH = 700
HEIGHT = 800
DIMENSION = 5  # 5x5 board
SEPARATION = 125
MAX_FPS = 10

# Load Images at the beginning
IMAGES = {}
def loadImages():
    IMAGES['T'] = pg.transform.scale(pg.image.load("Assets/tiger_emoji.png"), (50, 50))
    IMAGES['G'] = pg.transform.scale(pg.image.load("Assets/goat_emoji.png"), (50, 50))
    IMAGES['board'] = pg.transform.scale(pg.image.load("Assets/board2.png"), (700, 800))

# main loop
def main():
    # initialize pygame
    pg.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption('Baghchal')
    pg.display.set_icon(pg.image.load("Assets/tiger_emoji.png"))

    # GameState
    gs = BaghchalEngine.GameState()

    # setup image and font
    loadImages()
    font = pg.font.Font('freesansbold.ttf', 24)

    # variables to hold player moves
    sqSelected = ()
    playerClicks = []
    notations = []

    # track moves
    moveMade = False

    # game mode '11': player vs player, '00': bot vs bot
    pvp = '00'
    if pvp == '00':
        PlayerGoat = BaghchalAgent.GoatAgent(gs.board)
        PlayerTiger = BaghchalAgent.TigerAgent(gs.board)
        BaghchalAgent.train(PlayerGoat, PlayerTiger, 10)

        file = open("q_table_goat.txt", "w")
        file.write(str(PlayerGoat.Q_table))
        file.close()

        file2 = open("q_table_tiger.txt", "w")
        file2.write(str(PlayerTiger.Q_table))
        file2.close()

        file = open("game.play", 'w')

    # pvp = '10' : player vs bot
    playerTurn = False


    # main game loop
    totalGamesPlayed = 0
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            # keyboard events
            elif event.type == pg.KEYDOWN:
                # undo: Z
                if event.key == pg.K_z:
                    gs.undoMove()
                    moveMade = True

            # player vs player
            if pvp == '11':
                # mouse events
                if event.type == pg.MOUSEBUTTONDOWN:
                    location = pg.mouse.get_pos()
                    col = location[0] // SEPARATION
                    row = location[1] // SEPARATION

                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)

                    if (gs.board[row][col] == '.') and (len(playerClicks) == 1):  # if empty is selected
                        if gs.unusedGoats != 0:
                            move = BaghchalEngine.Move(playerClicks[0], playerClicks[0], gs.board)

                            if move in validMoves:
                                print(move.addGoatNotation())
                                gs.makeMove(move)
                                gs.unusedGoats = gs.unusedGoats - 1
                                moveMade = True
                            sqSelected = []
                            playerClicks = []

                    if len(playerClicks) == 2:
                        move = BaghchalEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        if move in validMoves:
                            print(move.getNotation())
                            gs.makeMove(move)
                            moveMade = True
                        sqSelected = []
                        playerClicks = []

        # bot vs bot
        if pvp == '00':
            if totalGamesPlayed > 50:
                pvp = '10'
                continue

            if gs.capturedGoats >= 5:    # game ends when more than 5 goats are captured
                file.write("Tiger Won\n")
                PlayerGoat.reset_board()
                gs = gs.restart()
                totalGamesPlayed += 1
                PlayerTiger.score += 1
                continue

            if gs.goatToMove:
                bestMove = PlayerGoat.select_move(gs.getAllGoatMoves())

            if not gs.goatToMove:
                if len(gs.tigerValidMoves) == 0 :
                    file.write("Goat Won \n")
                    gs = gs.restart()
                    totalGamesPlayed += 1
                    PlayerGoat.score += 1
                    continue
                else:
                    bestMove = PlayerTiger.select_move(gs.tigerValidMoves)
            move = BaghchalEngine.Move((bestMove[0], bestMove[1]),(bestMove[2],bestMove[3]), gs.board)


            gs.makeMove(move)
            if gs.goatToMove:
                file.write("Goat move: \n" + str(gs.board) + '\n\n')
            elif not gs.goatToMove:
                file.write("Tiger move: \n" + str(gs.board) + '\n\n')
            moveMade = True

        if pvp == '10':
            if playerTurn:
                # player as tiger
                # print("Player Move")

                if event.type == pg.MOUSEBUTTONDOWN:
                    location = pg.mouse.get_pos()
                    col = location[0] // SEPARATION
                    row = location[1] // SEPARATION

                    if sqSelected == (row, col):
                        sqSelected = []
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)

                    if (gs.board[row][col] == '.') and (len(playerClicks) == 1):
                        sqSelected = []
                        playerClicks = []

                    if len(playerClicks) == 2:
                        move = [playerClicks[0][0], playerClicks[0][1], playerClicks[1][0], playerClicks[1][1]]
                        if move in validMoves:
                            gs.makeMove(BaghchalEngine.Move((move[0], move[1]),(move[2], move[3]), gs.board))
                            playerTurn = not playerTurn
                            moveMade = True
                        sqSelected = []
                        playerClicks = []

            elif not playerTurn:
                pg.time.delay(1000)
                bestMove = PlayerGoat.maxQmove(gs.getAllGoatMoves())
                gs.makeMove(BaghchalEngine.Move((bestMove[0], bestMove[1]),(bestMove[2],bestMove[3]), gs.board))
                playerTurn = not playerTurn
                moveMade = True

            if gs.capturedGoats >= 5:
                PlayerGoat.reset_board()
                gs = gs.restart()
                continue

        if moveMade:
            if gs.goatToMove:
                validMoves = gs.getAllGoatMoves()
            else:
                validMoves = gs.getAllTigerMoves()
            moveMade = False

        drawGameState(screen, gs)
        # render texts
        drawText(screen, font, str(gs.unusedGoats), (200, 750), pg.color.Color(0,100,0), False)
        drawText(screen, font, str(gs.capturedGoats), (300, 750), pg.color.Color(200, 100, 10), True)
        drawText(screen, font, str(totalGamesPlayed), (100, 750), pg.color.Color(255, 255, 255), True)
        if pvp == '00':
            drawText(screen, font, str(PlayerGoat.score), (200, 775), pg.color.Color(0,100,0), False)
            drawText(screen, font, str(PlayerTiger.score), (300, 775), pg.color.Color(200, 100, 10), True)

        clock.tick(MAX_FPS)
        pg.display.flip()
        pg.display.update()
    file.close()

def drawGameState(screen, gs):
    # draw background
    screen.blit(IMAGES['board'], pg.Rect(0, 0, WIDTH, HEIGHT))
    drawPieces(screen, gs.board)

def drawPieces(screen, board):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            piece = board[i][j]
            if piece != '.':
                screen.blit(IMAGES[piece], pg.Rect(75+j*SEPARATION, 75+i*SEPARATION, 50, 50))

def drawText(screen, font, text, position, color, bold):
    if bold:
        font.set_bold(10)
    text = font.render(text, True, color, None)
    textRect = text.get_rect()
    textRect.center = position
    screen.blit(text, textRect)

if __name__ == "__main__":
    main()