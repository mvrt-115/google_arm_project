import serial

class Arm:
    def __init__(self, port, testing):
        if not testing:
            try:
                Arm.ser = serial.Serial(port, 115200) # Open serial line
            except  serial.serialutil.SerialException:
                print('Failed to open port: ' + port)
        print('Starting Arm')
        Arm.t = testing

    def drawLetter(self, letter, move): # Comment out testing when connected to arm
        xCoords = [0, 50, 150, 250, 50, 150, 250, 50, 150, 250]
        yCoords = [0, 50, 50, 50, 150, 150, 150, 250, 250, 250]
        if letter == 1:
            # Draw X
            stroke1 = ('L '+str(xCoords[move]-25)+','+str(yCoords[move]-25)+' '+str(xCoords[move]+25)+','+str(yCoords[move]+25)+'\n')
            stroke2 = ('L '+str(xCoords[move]-25)+','+str(yCoords[move]+25)+' '+str(xCoords[move]+25)+','+str(yCoords[move]-25)+'\n')
            if not Arm.t:
                Arm.ser.write(stroke1.encode())
                wait()
                Arm.ser.write(stroke2.encode())
                wait()
        else:
            # Draw O
            stroke = ('A '+str(xCoords[move])+','+str(yCoords[move])+' 25 '+'0 '+'360'+'\n')
            if not Arm.t:
                Arm.ser.write(stroke.encode())
                wait()
        return True # Testing

    def drawBoard(self): # Comment out testing when connected to arm
        stroke1 = ('L 100,0 100,300\n')
        stroke2 = ('L 200,0 200,300\n')
        stroke3 = ('L 0,100 300,100\n')
        stroke4 = ('L 0,200 300,200\n')
        if not Arm.t:
            Arm.ser.write(stroke1.encode())
            Arm.ser.write(stroke2.encode())
            Arm.ser.write(stroke3.encode())
            Arm.ser.write(stroke4.encode())
        return True # Testing

    def wait(self):
        while Arm.ser.readline() != 'Finish' or Arm.ser.readline() != 'Invalid':
            pass

    def close(self):
        # Closes the serial port.
        Arm.ser.close()
        print('Serial port closed')
