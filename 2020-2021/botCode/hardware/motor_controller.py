#!/usr/bin/python3

""" Controls the power to the motors using PID.
"""

import RPi.GPIO as GPIO
import enum
import time
from motor import Motor
from dist_sensor import DistSensor
from encoder import Encoder

# Enum for movement state machine
class MoveState(enum.Enum):
	STRAIGHT = 0
	TURN_LEFT = 1
	TURN_RIGHT = 2

class MotorController:
	
	def __init__(self):
		GPIO.setmode(GPIO.BOARD)
		# Init devices
		# TODO: Replace these numbers with the correct pins
		self.motor_l = Motor(3, 4, 5)
		self.motor_r = Motor(3, 4, 5)
		self.encoder_l = Encoder(0, 0)
		self.encoder_r = Encoder(0, 0)
		self.sensors = [DistSensor(0), DistSensor(0), DistSensor(0), DistSensor(0), DistSensor(0)]
		# Misc state
		self.move_state = MoveState.STRAIGHT
		self.spd = 0
		self.running = True
		# Constants, probably gonna rewrite how the bot turns
		self.outer_ticks = 10
		self.inner_ticks = 0
		self.max_ticks = 50
		
	# Starts the motor controller
	def start(self):
		self.thread = threading.Thread(target = self.run, daemon = True)
		self.thread.start()
		
	# Runs the motor controller continously
	def run(self):
		last_time = 0
		last_left_spd = 0
		last_right_spd = 0
		while self.running:
			# Movement state machine
			# Why doesn't python have switch statements
			if self.move_state == MoveState.STRAIGHT:
				# Calculate delta time
				curr_time = time.time()
				delta_time = curr_time - last_time
				last_time = curr_time
				# Run motors with PID
				left_spd = self.encoder_l.read_ticks() / self.max_ticks / delta_time
				left_pwr = 1 * (self.spd - left_spd) - 1 * (left_spd - last_left_spd) / delta_time + 1 * self.sensors[0].detected()
				last_left_spd = left_spd
				left_pwr = min(max(left_pwr, -1), 1)
				right_spd = self.encoder_r.read_ticks() / self.max_ticks / delta_time
				right_pwr = 1 * (self.spd - right_spd) - 1 * (right_spd - last_right_spd) / delta_time + 1 * self.sensors[4].detected()
				last_right_spd = right_spd
				right_pwr = min(max(right_pwr, -1), 1)
				self.motor_l.set_pwr(left_pwr)
				self.motor_r.set_pwr(right_pwr)
			elif self.move_state == MoveState.TURN_LEFT:
				# Turn the bot
				enc_out = 0
				enc_in = 0
				self.motor_l.set_pwr(-0.1)
				self.motor_l.set_pwr(0.1)
				while enc_out > self.outer_ticks and enc_in < self.inner_ticks:
					enc_out += self.encoder_l.read_ticks()
					enc_in += self.encoder_r.read_ticks()
				self.motor_l.set_pwr(0)
				self.motor_l.set_pwr(0)
				# Set state back to straight
				self.move_state = MoveState.STRAIGHT
			elif self.move_state == MoveState.TURN_RIGHT:
				# Turn the bot
				enc_out = 0
				enc_in = 0
				self.motor_l.set_pwr(0.1)
				self.motor_l.set_pwr(-0.1)
				while enc_out > self.outer_ticks and enc_in < self.inner_ticks:
					enc_out += self.encoder_l.read_ticks()
					enc_in += self.encoder_r.read_ticks()
				self.motor_l.set_pwr(0)
				self.motor_l.set_pwr(0)
				# Set state back to straight
				self.move_state = MoveState.STRAIGHT

	# Makes the robot turn left 90 degrees
	# If the robot is in the middle of a turn, this does nothing
	def turn_left(self):
		# Turn check
		if self.move_state is not MoveState.STRAIGHT:
			return
		# Temporarily stop thread
		self.running = False
		self.thread.join()
		# Set turning state
		self.move_state = MoveState.TURN_LEFT
		# Restart thread
		self.running = True
		self.thread.start()
		
	# Makes the robot turn right 90 degrees
	# If the robot is in the middle of a turn, this does nothing
	def turn_right(self):
		# Turn check
		if self.move_state is not MoveState.STRAIGHT:
			return
		# Temporarily stop thread
		self.running = False
		self.thread.join()
		# Set turning state
		self.move_state = MoveState.TURN_RIGHT
		# Restart thread
		self.running = True
		self.thread.start()
		
	# Sets the robot's linear speed
	def set_spd(self, spd):
		self.running = False
		self.thread.join()
		self.spd = spd
		self.running = True
		self.thread.start()
	
	# Stops the motor controller
	def stop(self):
		# Stop thread
		self.running = False
		self.thread.join()
		# Clean up resources
		self.motor_l.stop()
		self.motor_r.stop()
		GPIO.cleanup()