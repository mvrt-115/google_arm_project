# Tic Tac Toe class object with arm interactions
import random
import re

from Arm import Arm

class GRQDGame:
    def __init__(self, arm):
        GRQDGame.choices = list()
        GRQDGame.item = 'Andy'
        GRQDGame.xCoords = list()
        GRQDGame.yCoords = list()
        Arm = arm

    def drawObject(self, lines): # Comment out testing when connected to arm
        # Send the array of lines to be drawn
        return True # Testing

    def close(self):
            # Closes the serial port.
            GRQDGame.Arm.ser.close()
            print('Serial port closed')
    
    def chooseObjects(self):
        with open('categories.txt') as f:
            lines = [line.rstrip('\n') for line in open('categories.txt')]
        GRQDGame.choices = random.sample(lines,4)
        GRQDGame.item = random.choice(GRQDGame.choices)

    def generateCoordinates(self):
        with open('Drawing_Only/'+GRQDGame.item+'.ndjson') as f:
            objectLines = [line.rstrip('\n') for line in open('Drawing_Only/'+GRQDGame.item+'.ndjson')]
        drawingNum = random.randint(0,9)
        coords = objectLines[drawingNum]
        #Obtain X Y data
        xAxisStart = [m.start() for m in re.finditer('\[\[', coords)]
        xyMiddle = [m.start() for m in re.finditer('[0-9]\],\[', coords)]
        yAxisEnd = [m.start() for m in re.finditer('\]\]', coords)]
        #Gather into X and Y
        xStrokes = list()
        yStrokes = list()
        GRQDGame.xCoords = list()
        GRQDGame.yCoords = list()
        for i in range(len(xAxisStart)):
            xStrokes.append(coords[xAxisStart[i]+2:xyMiddle[i]+1])
            yStrokes.append(coords[xyMiddle[i]+4:yAxisEnd[i]])
            GRQDGame.xCoords.append([int(x) for x in xStrokes[i].split(',')])
            GRQDGame.yCoords.append([int(y) for y in yStrokes[i].split(',')])

    def play(self):
        GRQDGame.chooseObjects(self)
        # Change to audio prompts
        print('This game reverses the role of Google Quick Draw.')
        print('You have 5 seconds to decide which option the drawing best represents.')
        print('Options: ')
        print(', '.join(GRQDGame.choices))
        answer = input('Which option is it?:\n')
        if GRQDGame.choices[int(answer)-1] == GRQDGame.item:
            print('You are correct!')
        else: print('Sorry the correct answer is:'+GRQDGame.item)

if __name__ == '__main__':
    arm = Arm('/dev/ttyACM0', True)
    g = GRQDGame(arm)
    g.play()