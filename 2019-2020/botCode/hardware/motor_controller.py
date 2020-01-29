#!/usr/bin/python3

""" Controls the power to the motors using PID.
"""

import RPi.GPIO as GPIO
from motor import Motor
from encoder import Encoder

class MotorController:
	
	def __init__(self):
		GPIO.setmode(GPIO.BOARD)
		# Init devices
		self.motor_l = Motor(3, 4, 5)		# Replace these numbers with the correct pins
		self.motor_r = Motor(3, 4, 5)		# Replace these numbers with the correct pins
		
	# Starts the motor controller
	def start(self):
		self.thread = threading.Thread(target = self.run, daemon = True)
		self.thread.start()
		
	# Runs the motor controller continously
	def run(self):
		while True:
			# TODO: Actually implement the logic
			pass
		
	# Stops the motor controller
	def stop(self):
		# Stop thread
		self.thread.join()
		# Clean up resources
		self.motor_l.stop()
		self.motor_r.stop()
		GPIO.cleanup()