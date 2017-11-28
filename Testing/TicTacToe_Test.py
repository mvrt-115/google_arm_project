# Text Based Tic Tac Toe for testing

import random

def drawBoard(board):
    # This function prints out the board that it was passed.

    # "board" is a list of 10 strings representing the board (ignore index 0)
    print('   |   |' + '         |   |')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3] + '     1 | 2 | 3')
    print('   |   |' + '         |   |')
    print('-----------' + '   -----------')
    print('   |   |' + '         |   |')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6] + '     4 | 5 | 6')
    print('   |   |' + '         |   |')
    print('-----------' + '   -----------')
    print('   |   |' + '         |   |')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9] + '     7 | 8 | 9')
    print('   |   |' + '         |   |')

def chooseDifficulty():
    # Lets the player choose the difficulty.
    # Returns the difficulty.
    diff = ''
    while not (diff == '1' or diff == '2' or diff == '3'):
        print('Choose the Difficulty:')
        print('1 = Easy, 2 = Normal, 3 = Impossible')
        diff = input()
    return diff

def inputPlayerLetter():
    # Lets the player type which letter they want to be.
    # Returns a list with the player's letter as the first item, and the computer's letter as the second.
    letter = ''
    while not (letter == 'X' or letter == 'O'):
        print('Do you want to be X or O?')
        letter = input().upper()

    # the first element in the tuple is the player's letter, the second is the computer's letter.
    if letter == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']

def whoGoesFirst(playerLetter):
    # Randomly choose the player who goes first.
    if playerLetter.lower() == 'x':
        return 'You'
    else:
        return 'The computer'

def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')

def makeMove(board, letter, move):
    board[move] = letter

def isWinner(bo, le):
    # Given a board and a player's letter, this function returns True if that player has won.
    # We use bo instead of board and le instead of letter so we don't have to type as much.
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or # across the top
    (bo[4] == le and bo[5] == le and bo[6] == le) or # across the middle
    (bo[1] == le and bo[2] == le and bo[3] == le) or # across the bottom
    (bo[7] == le and bo[4] == le and bo[1] == le) or # down the left side
    (bo[8] == le and bo[5] == le and bo[2] == le) or # down the middle
    (bo[9] == le and bo[6] == le and bo[3] == le) or # down the right side
    (bo[7] == le and bo[5] == le and bo[3] == le) or # diagonal
    (bo[9] == le and bo[5] == le and bo[1] == le)) # diagonal

def getBoardCopy(board):
    # Make a duplicate of the board list and return it the duplicate.
    dupeBoard = []

    for i in board:
        dupeBoard.append(i)

    return dupeBoard

def testWinMove(board, letter, i):
    # i = the square to check if makes a win.
    bCopy = getBoardCopy(board)
    bCopy[i] = letter
    return isWinner(bCopy, letter)

def getPlayerMove(board):
    # Let the player type in his move.
    move = ' '
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not board[int(move)] == ' ':
        print('What is your next move? (1-9)')
        move = input()
    return int(move)

def chooseRandomMoveFromList(board, movesList):
    # Returns a valid move from the passed list on the passed board.
    # Returns None if there is no valid move.
    possibleMoves = []
    for i in movesList:
        if board[i] == ' ':
            possibleMoves.append(i)

    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None

def testForkMove(board, letter, i):
    # Determines if a move opens up a fork.
    bCopy = getBoardCopy(board)
    bCopy[i] = letter
    winningMoves = 0
    for j in range(1, 10):
        if testWinMove(bCopy, letter, j) and bCopy[j] == ' ':
            winningMoves += 1
    return winningMoves >= 2

def getComputerMove(board, computerLetter, difficulty):
    # Given a board and the computer's letter, determine where to move and return that move.
    if computerLetter == 'X':
        playerLetter = 'O'
    else:
        playerLetter = 'X'

    # Easy Difficulty
    if difficulty == '1':
        # Move randomly.
        return chooseRandomMoveFromList(board, [1, 2, 3, 4, 5, 6, 7, 8, 9])
    
    # Here is our algorithm for our Tic Tac Toe AI:
    # First, check if we can win in the next move.
    for i in range(1, 10):
        if board[i] == ' ' and testWinMove(board, computerLetter, i):
            return i

    # Check if the player could win on his next move, and block them.
    for i in range(1, 10):
        if board[i] == ' ' and testWinMove(board, playerLetter, i):
            return i

    # Check for computer fork opportunities.
    for i in range(1, 10):
        if board[i] == ' ' and testForkMove(board, computerLetter, i):
            return i
    
    # Check player fork opportunities, incl. two forks, and block them.
    if difficulty == '2':
        randomChance = random.randint(0, 1)
        if randomChance < .2:
            #  Check player fork opportunities
            for i in range(1, 10):
                if board[i] == ' ' and testForkMove(board, playerLetter, i):
                    return i
    else:
        randomChance = 10
        playerForks = 0
        for i in range(1, 10):
            if board[i] == ' ' and testForkMove(board, playerLetter, i):
                playerForks += 1
                tempMove = i
        if playerForks == 1:
            return tempMove
        elif playerForks == 2:
            return chooseRandomMoveFromList(board, [2, 4, 6, 8])

    if randomChance < .4:
        # Move randomly.
        return chooseRandomMoveFromList(board, [1, 2, 3, 4, 5, 6, 7, 8, 9])

    # Try to take the center, if it is free.
    if board[5] == ' ':
        return 5

    # Try to take one of the corners, if they are free.
    move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
    if move != None:
        return move

    # Move on one of the sides.
    return chooseRandomMoveFromList(board, [2, 4, 6, 8])

def isBoardFull(board):
    # Return True if every space on the board has been taken. Otherwise return False.
    for i in range(1, 10):
        if board[i] == ' ':
            return False
    return True


print('Welcome to Tic Tac Toe!')
score = [0, 0]

while True:
    # Reset the board and print overarching score.
    print('Score: Player: ' + str(score[0]) + ' | Computer:'+ str(score[1]))
    theBoard = [' '] * 10
    difficulty = chooseDifficulty()
    playerLetter, computerLetter = inputPlayerLetter()
    turn = whoGoesFirst(playerLetter)
    print(turn + ' will go first.')
    gameIsPlaying = True

    while gameIsPlaying:
        if turn == 'You':
            # Player's turn.
            drawBoard(theBoard)
            move = getPlayerMove(theBoard)
            makeMove(theBoard, playerLetter, move)

            if isWinner(theBoard, playerLetter):
                drawBoard(theBoard)
                print('Hooray! You have won the game!')
                gameIsPlaying = False
                score[0] += 1
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('The game is a tie!')
                    break
                else:
                    turn = 'The computer'

        else:
            # Computer's turn.
            move = getComputerMove(theBoard, computerLetter, difficulty)
            makeMove(theBoard, computerLetter, move)

            if isWinner(theBoard, computerLetter):
                drawBoard(theBoard)
                print('The computer has beaten you! You lose.')
                gameIsPlaying = False
                score[1] +=1
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('The game is a tie!')
                    break
                else:
                    turn = 'You'

    if not playAgain():
        print('Final score: Player: ' + str(score[0]) + ' | Computer:'+ str(score[1]))
        break