#include <PID_v1.h>
#include <Servo.h>
#include <Wire.h>
#include <PID_AutoTune_v0.h>



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

void loop() {
  Serial.print(analogRead(rightSensor));
  Serial.print(" ");
  Serial.println(analogRead(leftSensor));

  int readRight = analogRead(rightSensor);
  int readLeft = analogRead(leftSensor);

  if (readRight > 235 && readRight < 350) {
    Serial.print("stop right");
    //delay(1000);
    leftServo.write(93);
    rightServo.write(93);
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
