#!/usr/bin/python3

""" Wrapper for distance sensors.
"""

class DistSensor:

	# Initializes the distance sensor
	# pin: the detection pin
	def __init__(self, pin):
		GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		self.pin = pin
	
	# True if something is being detected
	def detected(self):
		return not GPIO.input(self.pin)