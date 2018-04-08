"""
ArduinoInterface.py
contains functionality for communication between RaspberryPi and Arduino
Ethan Yaccarino-Mims
"""


import serial
import RPi.GPIO as GPIO

ser = serial.Serial("/dev/ttyACM&", 9600) #replace & with num found from ls /dev/tty/ACM*
ser.baudrate = 9600    

"""
cmd: String
"""
def sendString(cmd):
	for ch in cmd:
		ser.write(bytes(ch.encode("ascii")))


def getLine():
	return ser.readline()

