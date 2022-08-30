import code
from datetime import datetime
from distutils.cmd import Command
import random
import serial
import serial.tools.list_ports
import queue

q = queue.Queue()


class mCALCANCommand:
    type = None
    code = None
    operation = None
    data = []
def __init__(self):
    self.type = None
    self.code = None
    self.operation = None
    self.data = []

class Communication:
    baudrate = ''
    portName = ''
    dummyPlug = False
    ports = serial.tools.list_ports.comports()
    ser = serial.Serial()
    time = datetime.now()
    q = queue.Queue()

    def __init__(self):
        self.baudrate = 9600
        print("the available ports are (if none appear, press any letter): ")
        for port in sorted(self.ports):
            # obtener la lista de puetos: https://stackoverflow.com/a/52809180
            print(("{}".format(port)))
        self.portName = input("write serial port name (ex: /dev/ttyUSB0): ")
        try:
            self.ser = serial.Serial(self.portName, self.baudrate, timeout=1, write_timeout=1)
        except serial.serialutil.SerialException:
            print("Can't open : ", self.portName)
            self.dummyPlug = True
            print("Dummy mode activated")

    def close(self):
        if(self.ser.isOpen()):
            self.ser.close()
        else:
            print(self.portName, " it's already closed")
    
    def mission_start(self):
        command = mCALCANCommand()
        command.type = 0
        command.operation = 2
        command.code = 0
        q.put(command)

    def set_coordinates(self, lat, long):
        command = mCALCANCommand()
        command.type = 0
        command.operation = 1
        command.code = 2
        command.data = [lat, long]
        q.put(command)
        print('set coordinates')

    def ready_to_launch(self):
        command = mCALCANCommand()
        command.type = 0
        command.operation = 0
        command.code = 3
        q.put(command)
        print('ready to launch')

    def sendCommand(self):
        while(q.qsize() > 0):
            command = q.get()
            command_chain = []
            command_chain.append('gvie')
            command_chain.append(str(command.type))
            command_chain.append(str(command.operation) + str(command.code))
            if(command.data):
                for value in command.data:
                    command_chain.append(str(value))
            command_str = ','
            command_str = command_str.join(command_chain) + '\n\r'
            if(self.ser.isOpen()):
                print('Sending command ' + command_str)
                try:
                    self.ser.write(command_str.encode("utf-8"))
                except serial.SerialTimeoutException:
                    print('ERROR: unable to send command')

    def getCommand(self):
        command = mCALCANCommand()
        if(self.dummyPlug == False):
            value = self.ser.readline()  # read line (single value) from the serial port
            decoded_bytes = str(value[0:len(value) - 2].decode("utf-8"))
            print(decoded_bytes)
            command_chain = decoded_bytes.split(",")
            if(command_chain[0] != 'gvie'):
                return None
            command.type = int(command_chain[1])
            command.operation = int(command_chain[2][0])
            command.code = int(command_chain[2][1])
            if(len(command_chain) > 3):
                try:
                    command.data = command_chain[3:len(command_chain)]
                except IndexError:
                    print('ERROR: unable to get command data')
        else:
            command.type = 1
            command.operation = 1
            command.code = 4
            command.data = self.getData()
        return command


    def getData(self):
        actual_time = datetime.now()
        seconds = actual_time - self.time
        milisec = seconds.total_seconds() * 1000
        value_chain = [milisec] + random.sample(range(0, 300), 1) + \
            [random.getrandbits(1)] + random.sample(range(0, 20), 10) + \
                random.sample(range(1000, 3000), 2) +  random.sample(range(60, 90), 1)
        return value_chain

    def isOpen(self):
        return self.ser.isOpen()

    def dummyMode(self):
        return self.dummyPlug 
