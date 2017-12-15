# Tic Tac Toe class object with arm interactions
# Custom Traits (triggerd from pushtotalk.py):
#             -startGame
#             -setLetter
#             -choosePosition
# Game Logic: -when startGame is triggered, create a new game and override any existing ones
#             -player can select letter through setLetter (default letter is x)
#             -IF player letter is 'O':
#                 -calculate starting move and send signal to arm to draw X at calculated postition
#                 -wait for arm to finish and signal when done
#             -repeat until game is finished:
#                 -wait for input from choosePostition
#                 -place player letter at input position
#                 -calculate computer move and place opposite letter
#                 -wait for arm to finish and signal when done
#             -draw winning line



# This code is messy and weird, the structure will probably change
import serial

class Arm:
    def __init__(self, port):
        try:
            self.ser = serial.Serial(port, 115200) # Open serial line
            while self.ser.read_until('$').decode('utf-8') != 'ready':
                self.ser.write(b'N$')
        except  serial.serialutil.SerialException:
            print('Failed to open port: ' + port)
            exit()
    
    def isBusy(self):
        # Checkes if the Arduino is busy.
        self.ser.write(b'Busy$')
        if self.ser.read_until('$').decode('utf-8') == 'busy':
            return True
        return False

    # Communication with Arduino

    def movePos(self, letter, move):
        # Sends a signal to the arm to draw the input letter at the input position.
        if self.isBusy() != True:
            self.ser.write(b('P'+str(letter)+str(move)+'$'))
            if self.ser.read_until('$').decode('utf-8') == 'Invalid':
                print('Falied: Invalid request')
                return False
            else:
                print('Success: ' + str(letter) + ' placed at ' + str(move))
                return True
        print('Falied: Arduino is Busy')
        return False

    # Optional commands can be added

    def close(self):
        # Closes the serial port.
        self.ser.close()
        print('Serial port closed')

class Board: # Should be complete
    def __init__(self):
        self.board = [0]*10

    def draw(self):
        # Prints out the board in current state.
        # "board" is a list of 10 ints representing the board (ignore index 0).
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
        # Makes a move on the board based on the input letter and position.
        if self.board[move] == 0:
            self.board[move] = letter
            return True
        else:
            print("Error: Already occupied")
            return False

    def isWinner(self, le):
        # Given a board and a letter, this function returns True if that letter has won.
        # Using bo instead of board and le instead of letter.
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

class TTTGame:
    def __init__(self):
        self.board = Board()
        self.playerLetter = 0 # 0 = blank, 1 = X, 2 = O
        # self.arm = Arm('/dev/ttyACM0')

    def draw(self):
        # Prints the board, mainly used for debugging.
        self.board.draw()

    def whichTurn(self,letter):
        # Determines the letter for the current turn.
        if letter == 1:
            return 2
        return 1


    def makeMove(self, letter, move):
        # Moves the letter (determined by whichTurn()) to the imput move.
        # Upon being verified, sends a signal for the arm to physically draw the letter at the postion.
        if self.board.makeMove(letter, move):
            print('Ok: ' + str(letter) + ' can be placed at ' + str(move))
            # self.arm.movePos(letter,move)
        else:
            print('Error: ' + str(letter) + ' cannot be placed at ' + str(move))

    def isWinner(self, le):
        # Checks if the given letter has won.
        if self.board.isWinner(le):
            return True
        return False

    def isBoardFull(self):
        # Checks if the board is full.
        if self.board.isBoardFull():
            return True
        return False

    def setPLetter(self, le):
        self.playerLetter = le
    def getPLetter(self):
        return self.playerLetter

    def getComputerMove(self):
        # Determines the optimal move for the computer.
        print('i cant code') # use logic from ttt test code

    # Game logic and more need to be added
    # Not sure how to have the game "run", but still take input from pushtotalk program
    # Game Logic may have to be implemented in pushtotalk program

    def quit(self):
        # self.arm.close()
        exit()


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
g.quit()