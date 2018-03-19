import random
import re
import matplotlib.pyplot as plt
plt.rcParams['toolbar'] = 'None'

#Generate choices and item
with open('categories.txt') as f:
    lines = [line.rstrip('\n') for line in open('categories.txt')]
choices = random.sample(lines,4)
item = random.choice(choices)

with open('Drawing_Only/'+item+'.ndjson') as f:
    objectLines = [line.rstrip('\n') for line in open('Drawing_Only/'+item+'.ndjson')]

#Choose specific drawing and list options:
drawingNum = random.randint(0,9)
print('This game reverses the role of Google Quick Draw.')
print('You have 5 seconds to decide which option the drawing best represents.')
print('Options: ')
print(', '.join(choices))
input('Hit [Enter] when ready')
# print(item+' number '+str(drawingNum+1)+':') #Acutal item and number
coords = objectLines[drawingNum]
# print(coords)
# print()

#Obtain X Y data
xAxisStart = [m.start() for m in re.finditer('\[\[', coords)]
xyMiddle = [m.start() for m in re.finditer('[0-9]\],\[', coords)]
yAxisEnd = [m.start() for m in re.finditer('\]\]', coords)]
# print(xAxisStart)
# print(xyMiddle)
# print(yAxisEnd)
# print()

#Gather into X and Y
xStrokes = list()
yStrokes = list()
xCoords = list()
yCoords = list()
for i in range(len(xAxisStart)):
    xStrokes.append(coords[xAxisStart[i]+2:xyMiddle[i]+1])
    yStrokes.append(coords[xyMiddle[i]+4:yAxisEnd[i]])
    xCoords.append([int(x) for x in xStrokes[i].split(',')])
    yCoords.append([int(y) for y in yStrokes[i].split(',')])
# print('X coords:')
# print(xCoords)
# print('Y coords:')
# print(yCoords)

#Plot strokes
plt.axis([0, 300, 300, 0])
plt.ion()
for i in range(len(xCoords)):
    plt.plot(xCoords[i],yCoords[i])
    plt.draw()
    plt.pause(.1)
plt.pause(5)
plt.close()

#Game part
answer = input('Which option is it? (1-4):\n')
while answer not in '1234' or len(answer) != 1:
    answer = input('Which option is it? (1-4):\n')
if choices[int(answer)-1] == item:
    print('You are correct!')
else: print('Sorry the correct answer is:'+item)