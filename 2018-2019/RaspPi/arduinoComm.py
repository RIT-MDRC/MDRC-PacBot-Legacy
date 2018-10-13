import serial
from .robomodules import ProtoModule


class ArduinoComm(ProtoModule):
    def __init__(self, baud):
        super()
        ser = serial.Serial("/dev/ttyACM&", baud) # replace & with num found from ls /dev/tty/ACM*
        ser.baudrate = baud

    def sendCommand(self, cmd):
        """
        cmd: single char (i.e. n, s, e, w)
        """
        ser.write(bytes(cmd.strip().encode("ascii")))



