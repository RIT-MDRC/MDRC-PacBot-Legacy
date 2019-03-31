#include <PID_v1.h>
#include <Servo.h>
#include <Wire.h>
#include <PID_AutoTune_v0.h>
#include <string.h>



/**
   Servo Motors
*/
Servo leftServo;
Servo rightServo;

/*
   Sensor values
*/

//PIN VALUES FOR SENSORS
int rightSensor = A0;
int leftSensor = A1;
int frontSensor = A2;

double rightInput = 0;
double leftInput = 0;
double frontInput = 0;

/*
   RPI values
*/
int rightRPI = 20;
int leftRPI = 18;
int upRPI = 16;
int downRPI = 14;

int directionState = 0;
char *states[3] = {"turning", "stop", "moving"};
char *currentState = states[1];

void setup() {
  Serial.begin(9600);

  leftServo.attach(9);
  rightServo.attach(10);
}

void adjustRight() {
  leftServo.write(97);
  rightServo.write(88);

}
void adjustLeft() {
  leftServo.write(99);
  rightServo.write(89);
}

void stopMotors() {
  leftServo.write(93);
  rightServo.write(93);
}

void turnAround180() {
  delay(1000);
  leftServo.write(180);
  rightServo.write(180);
  delay(1235);
}

void moveStraight(int readRight, int readLeft) {
  if (readRight > 235 && readRight < 350) {
    Serial.print("stop right");
    //delay(1000);
    stopMotors();
    adjustRight();
  }
  else if (readLeft > 225 && readLeft < 365 ) {
    Serial.print("stop left");
    //delay(1000);
    leftServo.write(93);
    rightServo.write(93);
    adjustLeft();
  }
  else {
    leftServo.write(180);
    rightServo.write(0);
  }

}

void loop() {
  Serial.print(analogRead(rightSensor));
  Serial.print(" ");
  Serial.println(analogRead(leftSensor));

  int readRight = analogRead(rightSensor);
  int readLeft = analogRead(leftSensor);

  if (strcmp(currentState, states[2]) == 0) {
    moveStraight(readRight, readLeft);
  }
  else if (strcmp(currentState, states[0]) == 0) {
    //turnAround180();
    currentState = states[2]; 
  }
  else{
    stopMotors();
    currentState = states[0];
  }

}
