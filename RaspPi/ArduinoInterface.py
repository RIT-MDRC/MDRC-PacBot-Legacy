"""
ArduinoInterface.py
contains functionality for communication between RaspberryPi and Arduino
Ethan Yaccarino-Mims
"""


import serial
import RPi.GPIO as GPIO


def ArduinoInit():
    ser = serial.Serial("/dev/ttyACM&", 9600) #replace & with num found from ls /dev/tty/ACM*
    ser.baudrate = 9600
