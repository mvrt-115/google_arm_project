################################################
#           __  ___ _   __ ___  ______         #
#          /  |/  /| | / // _ \/_  __/         #
#         / /|_/ / | |/ // , _/ / /            #
#        /_/  /_/  |___//_/|_| /_/             #
#                                              #
################################################

# Class: Arm.py
# Description: Uses pySerial to communicate with the Arduino on the Robotic Arm.

# Project: MVRTxGoogle Robotic Arm
# Project Descripton:
# 2018 Monta Vista Robotics Team, Cupertino, CA

import serial

class Arm:
    def __init__(self, port, testing):
        if not testing:
            try:
                Arm.ser = serial.Serial(port, 115200) # Open serial line
                print("Connected to Serial: " + Arm.ser.portstr)
            except  serial.serialutil.SerialException:
                print('Failed to open port: ' + port)
        print('Starting Arm')
        Arm.t = testing

    def aWrite(self, message): # Comment out testing when connected to arm
        if not Arm.t:
            Arm.ser.write(message.encode())
            Arm.wait(self)

    def drawLetter(self, letter, move): # Comment out testing when connected to arm
        xCoords = [0, 50, 150, 250, 50, 150, 250, 50, 150, 250]
        yCoords = [0, 50, 50, 50, 150, 150, 150, 250, 250, 250]
        if letter == 1:
            # Draw X
            stroke1 = ('L '+str(xCoords[move]-25)+','+str(yCoords[move]-25)+' '+str(xCoords[move]+25)+','+str(yCoords[move]+25)+'\n')
            stroke2 = ('L '+str(xCoords[move]-25)+','+str(yCoords[move]+25)+' '+str(xCoords[move]+25)+','+str(yCoords[move]-25)+'\n')
            if not Arm.t:
                Arm.ser.write(b'U')
                Arm.wait(self)
                Arm.ser.write(stroke1.encode())
                Arm.wait(self)
                Arm.ser.write(b'U')
                Arm.wait(self)
                Arm.ser.write(stroke2.encode())
                Arm.wait(self)
                Arm.ser.write(b'U')
                Arm.wait(self)
        else:
            # Draw O
            stroke = ('A '+str(xCoords[move])+','+str(yCoords[move])+' 25 '+'0 '+'360'+'\n')
            if not Arm.t:
                Arm.ser.write(stroke.encode())
                Arm.wait(self)
        return True # Testing

    def wait(self):
        incoming = Arm.ser.readline()
        while True:
            if incoming == b'Finish\r\n' or incoming == b'Invalid\r\n':
                break
            incoming = Arm.ser.readline()

    def close(self):
        # Closes the serial port.
        Arm.ser.close()
        print('Serial port closed')
