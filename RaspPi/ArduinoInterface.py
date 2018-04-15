"""
ArduinoInterface.py
contains functionality for communication between RaspberryPi and Arduino
Ethan Yaccarino-Mims
"""


import serial
import RPi.GPIO as GPIO


"""
cmd: String
"""

class Comms:

	def __init(self, baud)
	ser = serial.Serial("/dev/ttyACM&", baud) #replace & with num found from ls /dev/tty/ACM*
	ser.baudrate = baud    


	def sendString(self, cmd):
		for ch in cmd:
			ser.write(bytes(ch.encode("ascii")))


	def getLine(self):
		return ser.readline()









def main():
	line = ""
	while(line != "q"):
		line = input("enter 'q' to quit")
		sendString(line)
	print("done")



if __name_ == "__main__":
	main()
