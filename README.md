# MDRC-PacBot
RIT MDRC's robot competing in Harvard's Pacbot Competition.

## Hardware

# What you need

1. A Raspberry Pi 4b
2. An Arduino Uno
3. A USB-B to USB-A adapter
4. Adafruit Motor Shield v2
5. USC-C to USB-A cable for powering the Raspberry Pi
6. 5 distance sensors (Sharp 0A51SK F 02)
7. The Pacbot shell
8. Motors (2x DC motors, 30:1 Micro Metal Gearmotor LP 6V with Extended Motor Shaft (Item #2202))
9. 2 Wheels
10. 1 caster wheel
11. Code from MDRC pacbot repo (https://github.com/RIT-MDRC/MDRC-PacBot.git)

# How to build the robot

1. Put the distance sensors in the holes of the Pacbot shell.
2. Plug the motor shield into the Arduino.
3. Ensure the microSD card is inserted into the Raspberry Pi.
4. Plug the raspberry pi into a power source using the USB-C to A cord.
5. Plug the arduino into the Raspberry Pi using the USB-A to USB-B cable.
6. Plug the motors into the motor shield using the M1 and M2 slots.
7. Plug the power wires of the sensors (red + black) into the 5v power of the motor shield
8. Plug the data wire (white) into the analog input of the motor shield.
9. Put the wheels on the motor axles.
10. Plug the 9V battery into the motor shield using the 5-12V wire slots.
11. SSH into the raspberry pi at mdrcpi4.rit.edu
12. Run ls /dev/tty* to find the serial port of the Arduino (similar to "USB0").
13. Locate motorControllerPassthrough.py and run it on the Raspberry Pi with the argument of /dev/tty/USB0 (replace with serial port).
14. On your computer, locate motorControllerPassthrough.py and run it
15. Type "f", "b", "l", "r", or "s" (stop) to control the robot, or "q" to quit the program.
