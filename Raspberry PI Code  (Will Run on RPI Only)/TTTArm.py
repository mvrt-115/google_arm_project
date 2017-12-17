# Tic Tac Toe class object with arm interactions
import random
import serial
from gtts import gTTS

class Arm: # Uncomment stuff when arm is actually connected
    def __init__(self, port):
        # try:
        #     self.ser = serial.Serial(port, 115200) # Open serial line
        #     while self.ser.read_until('$').decode('utf-8') != 'ready':
        #         self.ser.write(b'N$')
        # except  serial.serialutil.SerialException:
        #     print('Failed to open port: ' + port)
        #     exit()
        print('Starting Arm')
    
    # Communication with Arduino
    # decode('utf-8') converts bytes into string
    # read_until('$') $ will be used as dividers between messages
    # Gautham knows the most about the communication part

    def isBusy(self):
        # Checkes if the Arduino is busy.
        # self.ser.write(b'Busy$')
        # if self.ser.read_until('$').decode('utf-8') == 'busy':
            # return True
        return False

    def movePos(self, letter, move): # Not done yet
        # Sends a signal to the arm to draw the input letter at the input position.
        # if self.isBusy() != True:
            # self.ser.write(b('P'+str(letter)+str(move)+'$'))
            # if self.ser.read_until('$').decode('utf-8') == 'Invalid':
                # print('Falied: Invalid request')
                # return False
            # else:
                # print('Success: ' + str(letter) + ' placed at ' + str(move))
                # return True
        # print('Falied: Arduino is Busy')
        # return False
        # Wait for finished signal
        return True # Testing

    def drawWinLine(self, winNum):
        print(str(winNum))

    def close(self):
        # Closes the serial port.
        # self.ser.close()
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
        # Given a board and a letter, this function returns a number corresponding to the win line if that letter has won.
        # Using bo instead of board and le instead of letter.
        if (self.board[7] == le and self.board[8] == le and self.board[9] == le): return 1 # across the top
        elif (self.board[4] == le and self.board[5] == le and self.board[6] == le): return 2 # across the middle
        elif (self.board[1] == le and self.board[2] == le and self.board[3] == le): return 3 # across the bottom
        elif (self.board[7] == le and self.board[4] == le and self.board[1] == le): return 4 # down the left side
        elif (self.board[8] == le and self.board[5] == le and self.board[2] == le): return 5 # down the middle
        elif (self.board[9] == le and self.board[6] == le and self.board[3] == le): return 6 # down the right side
        elif (self.board[7] == le and self.board[5] == le and self.board[3] == le): return 7 # diagonal
        elif (self.board[9] == le and self.board[5] == le and self.board[1] == le): return 8# diagonal
        return 0

    def isBoardFull(self):
        # Return True if every space on the board has been taken. Otherwise return False.
        for i in range(1, 10):
            if self.board[i] == 0:
                return False
        return True

    def getBoardCopy(self):
        # Make a duplicate of the board list and return it the duplicate.
        dupeBoard = Board()

        for i in self.board:
            dupeBoard.board[i] = i

        return dupeBoard

class TTTGame:
    def __init__(self):
        self.board = Board()
        self.playerLetter = 1 # 1 = 'X', 2 = 'O'
        self.arm = Arm('/dev/ttyACM0')

    def makeMove(self, move): # Not done yet
        # Given a board and the computer's letter, determine where to move and return that move.
        if self.playerLetter == 1:
            computerLetter = 2
        else:
            computerLetter = 1
        # Makes a move on the board with the player letter at input position.
        # Calculates the next move and places it at the position with the other letter.
        # Checks for winners. If so, sends the signal to draws the win line.
        if self.board.makeMove(self.playerLetter, move):
            print('Ok: ' + str(self.playerLetter) + ' can be placed at ' + str(move))
            # self.arm.movePos(self.playerLetter,move)
            if self.board.isWinner(self.playerLetter) > 0:
                self.arm.drawWinLine(self.board.isWinner(self.playerLetter))
                return self.playerLetter # Player Won
            elif self.board.isBoardFull():
                return 0 # Tie
            print('Making Comp Move') # Testing
            self.board.makeMove(computerLetter, self.getComputerMove(computerLetter))# Calculate next move and place
            # self.arm.movePos(computerLetter,move)
            if self.board.isWinner(computerLetter) > 0:
                self.arm.drawWinLine(self.board.isWinner(computerLetter))
                return computerLetter # Computer Won
            elif self.board.isBoardFull():
                return 0 # Tie
        else:
            print('Error: ' + str(self.playerLetter) + ' cannot be placed at ' + str(move))
            return -1

    def setPLetter(self, le):
        self.playerLetter = le
        # If player letter it 'O':
            # Make first move with computer as X
    def getPLetter(self):
        return self.playerLetter

    def chooseRandomMoveFromList(self, movesList):
        # Returns a valid move from the passed list on the passed board.
        # Returns None if there is no valid move.
        possibleMoves = []
        for i in movesList:
            if self.board.board[i] == 0:
                possibleMoves.append(i)

        if len(possibleMoves) != 0:
            return random.choice(possibleMoves)
        else:
            return None
    
    def testWinMove(self, board, letter, i):
        # i = the square to check if makes a win.
        bCopy = board.getBoardCopy()
        bCopy.board[i] = letter
        return bCopy.isWinner(letter) > 0

    def testForkMove(self, letter, i):
        # Determines if a move opens up a fork.
        bCopy = self.board.getBoardCopy()
        bCopy.board[i] = letter
        winningMoves = 0
        for j in range(1, 10):
            if self.testWinMove(bCopy, letter, j) and bCopy[j] == 0:
                winningMoves += 1
        return winningMoves >= 2

    def getComputerMove(self, computerLetter):
        # Determines the optimal move for the computer and tells arm to do so.

        # First, check if we can win in the next move.
        for i in range(1, 10):
            if self.board.board[i] == 0 and self.testWinMove(self.board, computerLetter, i):
                return i

        # Check if the player could win on his next move, and block them.
        for i in range(1, 10):
            if self.board.board[i] == 0 and self.testWinMove(self.board, self.playerLetter, i):
                return i

        # Check for computer fork opportunities.
        for i in range(1, 10):
            if self.board.board[i] == 0 and self.testForkMove(computerLetter, i):
                return i
        
        # Check player fork opportunities, incl. two forks, and block them.
        playerForks = 0
        for i in range(1, 10):
            if self.board.board[i] == 0 and self.testForkMove(self.playerLetter, i):
                playerForks += 1
                tempMove = i
        if playerForks == 1:
            return tempMove
        elif playerForks == 2:
            return self.chooseRandomMoveFromList([2, 4, 6, 8])

        # Try to take the center, if it is free.
        if self.board.board[5] == 0:
            return 5

        # Try to take one of the corners, if they are free.
        move = self.chooseRandomMoveFromList([1, 3, 7, 9])
        if move != None:
            return move

        # Move on one of the sides.
        return self.chooseRandomMoveFromList([2, 4, 6, 8])

    def quit(self):
        # self.arm.close() # Close Serial Port
        exit()


#Testing:
print('Testing:')
g = TTTGame()
print(str(g.makeMove(5)))
g.board.draw()
print(str(g.makeMove(1)))
g.board.draw()
print(str(g.makeMove(9)))
g.board.draw()
print(str(g.makeMove(9)))
g.board.draw()
g.quit()
