# Tic Tac Toe class object with arm interactions
import random
import serial

class Board:
    board = []
    def __init__(self):
        self.board = [0]*10

    def draw(self):
        # This function prints out the board that it was passed.
        # "board" is a list of 10 strings representing the board (ignore index 0)
        print('   |   |' + '         |   |')
        print(' ' + str(self.board[1]) + ' | ' + str(self.board[2]) + ' | ' + str(self.board[3]) + '     1 | 2 | 3')
        print('   |   |' + '         |   |')
        print('-----------' + '   -----------')
        print('   |   |' + '         |   |')
        print(' ' + str(self.board[4]) + ' | ' + str(self.board[5]) + ' | ' + str(self.board[6]) + '     4 | 5 | 6')
        print('   |   |' + '         |   |')
        print('-----------' + '   -----------')
        print('   |   |' + '         |   |')
        print(' ' + str(self.board[7]) + ' | ' + str(self.board[8]) + ' | ' + str(self.board[9]) + '     7 | 8 | 9')
        print('   |   |' + '         |   |')

    def makeMove(self, letter, move):
        if self.board[move] == 0:
            self.board[move] = letter
            return True
        else:
            print("Error: Already occupied")
            return False

    def isWinner(self, le):
        # Given a board and a player's letter, this function returns True if that player has won.
        # We use bo instead of board and le instead of letter so we don't have to type as much.
        return ((self.board[7] == le and self.board[8] == le and self.board[9] == le) or # across the top
        (self.board[4] == le and self.board[5] == le and self.board[6] == le) or # across the middle
        (self.board[1] == le and self.board[2] == le and self.board[3] == le) or # across the bottom
        (self.board[7] == le and self.board[4] == le and self.board[1] == le) or # down the left side
        (self.board[8] == le and self.board[5] == le and self.board[2] == le) or # down the middle
        (self.board[9] == le and self.board[6] == le and self.board[3] == le) or # down the right side
        (self.board[7] == le and self.board[5] == le and self.board[3] == le) or # diagonal
        (self.board[9] == le and self.board[5] == le and self.board[1] == le)) # diagonal

    def isBoardFull(self):
        # Return True if every space on the board has been taken. Otherwise return False.
        for i in range(1, 10):
            if self.board[i] == 0:
                return False
        return True

class Arm:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0', 115200)
    # communication stuff

    def move(self, letter, move):
        # stuff


class TTTGame:
    def __init__(self):
        self.board = Board()
        self.diff = 0 # 0 = easiest, 1 = normal, 2 = impossible
        self.letter = 0 # 0 = blank, 1 = X, 2 = O
        self.arm = Arm()

    def draw(self):
        self.board.draw()

    def makeMove(self, letter, move):
        if self.board.makeMove(letter, move):
            print('Success: ' + str(letter) + ' placed at ' + str(move))
            # self.arm(stuff,stuff,stuff)
        else: print('Failed to place ' + str(letter) + ' at ' + str(move))

    def isWinner(self, le):
        if self.board.isWinner(le):
            return True
        return False

    def isBoardFull(self):
        if self.board.isBoardFull():
            return True
        return False

    def setDiff(difficulty):
        self.diff = difficulty
    def getDiff(self):
        return self.diff

    def setPLetter(le):
        self.letter = le
    def getPLetter(self):
        return self.letter

    def getComputerMove(self):
        print('i cant code')

    # more stuff



#Testing:
print('Testing:')
g = TTTGame()
g.makeMove(1,5)
g.makeMove(1,1)
g.makeMove(1,9)
g.makeMove(1,9)
g.draw()
print('X is winner: ' + str(g.isWinner(1)))
print('Is board full: ' + str(g.isBoardFull()))