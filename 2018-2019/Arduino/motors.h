/**
 * motors.h
 * Ethan Yaccarino-Mims
 * adds driving functionality
 */

#include "Pinout.h"
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

//the Motor Shield object
Adafruit_MotorShield AFMS = Adafruit_MotorShield();

//the motor objects
Adafruit_DCMotor *leftMotor = AFMS.getMotor(1);
Adafruit_DCMotor *rightMotor = AFMS.getMotor(2);


/**
 * initializes all objects and values
 */
void InitMotors(void)
{
  //defines pin modes
  pinMode(InA_1, OUTPUT);
  pinMode(InB_1, OUTPUT);
  pinMode(PWM_1, OUTPUT);
  pinMode(InA_2, OUTPUT);
  pinMode(InB_2, OUTPUT);
  pinMode(PWM_2, OUTPUT);

  //starts the motor shield
  AFMS.begin();

  //initial values for motor speed
  leftMotor -> setSpeed(0);
  rightMotor -> setSpeed(0);

  //initial direction for motors
  leftMotor -> run(FORWARD);
  rightMotor -> run(FORWARD);
}


/**
 * drives the left motor at the given speed
 * 
 * @param pwmValue the speed to drive the motor at 
 * on the scale of a signed eight bit value
 */
int driveLeft(int pwmValue)
{
  if(pwmValue >= 0)
  {
    leftMotor -> run(FORWARD); 
  }
  else
  {
    leftMotor -> run(BACKWARD);
  }
  leftMotor -> setSpeed(pwmValue);
  
}


/**
 * drives the right moter at the given speed
 *
 * @param pwmValue the speed to drive the motor at 
 * on the scale of a signed eight bit value
 */ 
int driveRight(int pwmValue)
{
  if(pwmValue >= 0)
  {
    rightMotor -> run(FORWARD); 
  }
  else
  {
    rightMotor -> run(BACKWARD);
  }
  rightMotor -> setSpeed(pwmValue);
  
}

int driveMotors(int left, int right)
{
  driveLeft(constrain(left, -255, 255));
  driveRight(constrain(right, -255, 255));
}


int turnBot(int value)
{
  if(value >= 0)
  {
    driveLeft(value);
    driveRight(-value);
  }
  else
  {
    driveLeft(-value);
    driveRight(value);
  }
}

