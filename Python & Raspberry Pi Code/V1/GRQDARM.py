# Tic Tac Toe class object with arm interactions
import random
import serial
import re

class GRQDGame:
    def __init__(self, port):
        self.choices = list()
        self.item = 'Andy'
        self.xCoords = list()
        self.yCoords = list()
        try:
            self.ser = serial.Serial(port, 115200) # Open serial line
        except  serial.serialutil.SerialException:
            ('Failed to open port: ' + port)
        print('Starting Arm')

    def drawObject(self, lines): # Comment out testing when connected to arm
        # Send the array of lines to be drawn
        return True # Testing

    def close(self):
            # Closes the serial port.
            self.ser.close()
            print('Serial port closed')
    
    def chooseObjects(self):
        with open('categories.txt') as f:
            lines = [line.rstrip('\n') for line in open('categories.txt')]
        self.choices = random.sample(lines,4)
        self.item = random.choice(choices)

    def generateCoordinates(self):
        with open('Drawing_Only/'+self.item+'.ndjson') as f:
            objectLines = [line.rstrip('\n') for line in open('Drawing_Only/'+self.item+'.ndjson')]
        drawingNum = random.randint(0,9)
        coords = objectLines[drawingNum]
        #Obtain X Y data
        xAxisStart = [m.start() for m in re.finditer('\[\[', coords)]
        xyMiddle = [m.start() for m in re.finditer('[0-9]\],\[', coords)]
        yAxisEnd = [m.start() for m in re.finditer('\]\]', coords)]
        #Gather into X and Y
        xStrokes = list()
        yStrokes = list()
        self.xCoords = list()
        self.yCoords = list()
        for i in range(len(xAxisStart)):
            xStrokes.append(coords[xAxisStart[i]+2:xyMiddle[i]+1])
            yStrokes.append(coords[xyMiddle[i]+4:yAxisEnd[i]])
            self.xCoords.append([int(x) for x in xStrokes[i].split(',')])
            self.yCoords.append([int(y) for y in yStrokes[i].split(',')])

    def play(self):
        # Change to audio prompts
        print('This game reverses the role of Google Quick Draw.')
        print('You have 5 seconds to decide which option the drawing best represents.')
        print('Options: ')
        print(', '.join(self.choices))
        answer = input('Which option is it?:\n')
        if choices[int(answer)-1] == item:
            print('You are correct!')
        else: print('Sorry the correct answer is:'+item)

if __name__ == '__main__':
    g = GRQDGame()
    play()