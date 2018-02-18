#include "Pinout.h"

int Motor1(int speed);
int Motor2(int speed);
int Motor3(int speed);


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

  Motor1(0);
  Motor2(0);
  Motor3(0);
}


void strafe(int pwmValue){
  Motor1(pwmValue);
  Motor2(pwmValue);
  Motor3((int)(-0.5*pwmValue));
}


void climb(int pwmValue){
  Motor1(pwmValue);
  Motor2(-pwmValue);
  Motor3(0)
}

