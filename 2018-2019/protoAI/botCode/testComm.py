import os, sys, curses, random, copy

import RPi.GPIO as GPIO



def __init__(self):

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(37, GPIO.OUT)
    GPIO.setup(35, GPIO.OUT)
    GPIO.setup(33, GPIO.OUT)
    GPIO.setup(31, GPIO.OUT)

def print_direction( value):
    if (value == 0):
        print("Moving Right")
        GPIO.output(37, GPIO.HIGH)
        GPIO.output(35, GPIO.LOW)
        GPIO.output(33, GPIO.LOW)
        GPIO.output(31, GPIO.LOW)
    elif (value == 1):
        print("Moving Left")
        GPIO.output(37, GPIO.LOW)
        GPIO.output(35, GPIO.HIGH)
        GPIO.output(33, GPIO.LOW)
        GPIO.output(31, GPIO.LOW)
    elif (value == 2):
        print("Moving Up")
        GPIO.output(37, GPIO.LOW)
        GPIO.output(35, GPIO.LOW)
        GPIO.output(33, GPIO.HIGH)
        GPIO.output(31, GPIO.LOW)
    elif (value == 3):
        print("Moving Down")
        GPIO.output(37, GPIO.LOW)
        GPIO.output(35, GPIO.LOW)
        GPIO.output(33, GPIO.LOW)
        GPIO.output(31, GPIO.HIGH)
    elif (value == 4):
        print("Stop")
        GPIO.output(37, GPIO.LOW)
        GPIO.output(35, GPIO.LOW)
        GPIO.output(33, GPIO.LOW)
        GPIO.output(31, GPIO.HIGH)




def main():
    try:
        print_direction(2)
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()