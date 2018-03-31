#include "Pinout.h"
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

Adafruit_MotorShield AFMS = Adafruit_MotorShield();

Adafruit_DCMotor *leftMotor = AFMS.getMotor(1);
Adafruit_DCMotor *rightMotor = AFMS.getMotor(2);


void InitMotors(void)
{
  pinMode(InA_1, OUTPUT);
  pinMode(InB_1, OUTPUT);
  pinMode(PWM_1, OUTPUT);
  pinMode(InA_2, OUTPUT);
  pinMode(InB_2, OUTPUT);
  pinMode(PWM_2, OUTPUT);

  AFMS.begin();

  leftMotor->setSpeed(0);
  rightMotor->setSpeed(0);

  leftMotor->run(FORWARD);
  rightMotor->run(FORWARD);
}


int driveLeft(int pwmValue)
{
  if(pwmValue >= 0)
  {
    myMotor1 -> run(FORWARD); 
  }
  else
  {
    myMotor1 -> run(BACKWARD);
  }
  myMotor1->setSpeed(pwmValue);
  
}


int driveRight(int pwmValue)
{
  if(pwmValue >= 0)
  {
    myMotor2 -> run(FORWARD); 
  }
  else
  {
    myMotor2 -> run(BACKWARD);
  }
  myMotor2->setSpeed(pwmValue);
  
}












