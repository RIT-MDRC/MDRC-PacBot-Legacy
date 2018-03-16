#include "Pinout.h"
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

Adafruit_MotorShield AFMS = Adafruit_MotorShield();

Adafruit_DCMotor *myMotor1 = AFMS.getMotor(1);
Adafruit_DCMotor *myMotor2 = AFMS.getMotor(2);
Adafruit_DCMotor *myMotor3 = AFMS.getMotor(3);


void InitMotors(void)
{
  pinMode(InA_1, OUTPUT);
  pinMode(InB_1, OUTPUT);
  pinMode(PWM_1, OUTPUT);
  pinMode(InA_2, OUTPUT);
  pinMode(InB_2, OUTPUT);
  pinMode(PWM_2, OUTPUT);
  pinMode(InA_3, OUTPUT);
  pinMode(InB_3, OUTPUT);
  pinMode(PWM_3, OUTPUT);

  AFMS.begin();

  myMotor1->setSpeed(0);
  myMotor2->setSpeed(0);
  myMotor3->setSpeed(0);

  myMotor1->run(FORWARD);
  myMotor2->run(FORWARD);
  myMotor3->run(FORWARD);
}


int drive1(int pwmValue)
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


int drive2(int pwmValue)
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


int drive3(int pwmValue)
{
  if(pwmValue >= 0)
  {
    myMotor3 -> run(FORWARD); 
  }
  else
  {
    myMotor3 -> run(BACKWARD);
  }
  myMotor3->setSpeed(pwmValue);
  
}


void driveAll(int dir[])
{
  
  
}










