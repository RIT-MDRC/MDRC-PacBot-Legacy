#!/usr/bin/python3

""" Wrapper for encoders.
"""

class Encoder:
	
	# Initializes the encoder
	# pin1: encoder pin 1
	# pin2: encoder pin 2
	def __init__(self, pin1, pin2):
		# Set up read pins
		GPIO.setup(pin1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.setup(pin2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		self.pin1 = pin1
		self.pin2 = pin2
		# Set up tick event handler
		GPIO.add_event_detect(self.pin1, GPIO.RISING, callback=self.tick)
		# Misc tick stuff
		self.ticks = 0
		
	# Returns the amount of ticks the encoder turned since last read
	def read_ticks(self):
		ticks = self.ticks
		self.ticks = 0
		return ticks
		
	# Callback function that occurs when pin1 gets high
	def tick(self, channel):
		self.ticks += 1 if GPIO.input(self.pin1) else -1