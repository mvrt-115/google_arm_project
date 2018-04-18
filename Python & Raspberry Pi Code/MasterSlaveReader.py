import serial

# Connect to Arduino
port1 = "COM4" # COM# for Windows, /dev/ttyACM0 for Linux
port2 = "COM5"
try:
    ser = serial.Serial(port1, 115200) # Open serial line
    arm = serial.Serial(port2, 115200) # Open serial line
except  serial.serialutil.SerialException:
    print('Failed to open ports.')
    exit()

# Open text file
try:
    f= open("Data.txt","w+") # Note! Old file WILL be deleted
except  serial.serialutil.SerialException:
    print('Failed to open file: Data.txt')
    exit()

# Parse data
angle1 = []
angle2 = []
count = 1
while True:
    incoming = ser.readline()
    if incoming == 'Start': # Record button pressed
        while True:
            incoming = ser.readline()
            arm.write(b(str(angle1[i]) + ',' + str(angle2[i]) + '\n')) # Send values to arm in <a1>,<a2> format
            if incoming == 'End':
                f.write('Set ' + str(count) + ':\n')
                for i in range(len(angle1)):
                    f.write(str(angle1[i]) + ',' + str(angle2[i]) + '\n')
                count = count + 1
                angle1 = []
                angle2 = []
                break
            angle1.append(incoming[0:incoming.index(' ')])
            angle2.append(incoming[incoming.index(' ')+1:])
f.close()
ser.close()
arm.close()
