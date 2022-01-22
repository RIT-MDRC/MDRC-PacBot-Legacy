#!/usr/bin/python3

""" Wrapper for motors.
"""

import RPi.GPIO as GPIO

class Motor:

	# Initializes the motor
	# pin1: PWM pin
	# pin2: Control pin 1
	# pin3: Control pin 2
	def __init__(self, pin1, pin2, pin3):
		# Set up the PWM pin
		GPIO.setup(pin1, GPIO.OUT)
		self.pwm = GPIO.PWM(pin1, 1000)
		self.pwm.start(0)
		# Set up the control pins
		GPIO.setup(pin2, GPIO.OUT)
		GPIO.setup(pin3, GPIO.OUT)
		self.ctrl1 = pin2
		self.ctrl2 = pin3
		
	# Changes the amount of power being sent to the motor
	# pwr: ranges from [-1.0, 1.0]
	def set_pwr(self, pwr):
		# Set control state
		# TODO: If this is too slow, optimize
		if pwr > 0:
			GPIO.output(self.ctrl1, GPIO.HIGH)
			GPIO.output(self.ctrl2, GPIO.LOW)
		else:
			GPIO.output(self.ctrl1, GPIO.LOW)
			GPIO.output(self.ctrl2, GPIO.HIGH)
		# Set PWM
		self.pwm.ChangeDutyCycle(100 * abs(pwr))
		
	# Permanently stops the motor
	def stop(self):
		self.pwm.stop()