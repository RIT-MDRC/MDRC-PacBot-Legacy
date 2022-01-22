#!/usr/bin/python3

from motor_controller import MotorController

def main():
	# Start motor controller
	motor_ctrl = MotorController()
	motor_ctrl.start()
	
if __name__ == "__main__":
	main()