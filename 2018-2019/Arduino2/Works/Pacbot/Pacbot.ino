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
char *states[] = {"turnfull", "turnright", "turnleft", "stop", "straight"};
char *currentState;
int counter = 0; 

void setup() {
  Serial.begin(9600);

  leftServo.attach(9);
  rightServo.attach(10);
}


void adjustRight() {
  leftServo.write(97); //4 speed slow
  rightServo.write(87); //6 speed slow

}
void adjustLeft() {
  leftServo.write(99); //6 speed slow
  rightServo.write(89); //4 speed slow  
}

void stopMotors() {
  leftServo.write(93);
  rightServo.write(93);
}

void turnAround180() {
  //delay(1000);
  leftServo.write(180);
  rightServo.write(180);
  delay(1400);
}

void turnAround90CW() {
  //delay(1000);
  leftServo.write(180);
  rightServo.write(180);
  delay(800);  
}

void turnAround90CCW(){
  //delay(1000);
  leftServo.write(0);
  rightServo.write(0);
  delay(800);  
}

void moveStraight(int readRight, int readLeft) {
  if (readRight > 280 && readRight < 350) {
    Serial.print("stop right");
    //delay(1000);
    stopMotors();
    adjustRight();
  }
  else if (readLeft > 225 && readLeft < 365 ) {
    Serial.print("stop left");
    //delay(1000);
    stopMotors(); 
    adjustLeft();
  }
  else {
    leftServo.write(180);
    rightServo.write(0);
  }
  delay(1340);

}


void loop() {
  
  Serial.print(analogRead(rightSensor));
  Serial.print(" ");
  Serial.println(analogRead(leftSensor));

  int readRight = analogRead(rightSensor);
  int readLeft = analogRead(leftSensor);

  //straight
  if (strcmp(currentState, states[4]) == 0) {
    moveStraight(readRight, readLeft);
  }
  //turn 180 degrees
  else if (strcmp(currentState, states[0]) == 0) {
    turnAround180(); 
  }
  //turn right
  else if(strcmp(currentState, states[1]) == 0){
    turnAround90CW();  
  }
  //turn left
  else if(strcmp(currentState, states[2]) == 0){
    turnAround90CCW();  
  }
  //stop
  else{
    stopMotors();
  }
  //Execute commands
  char *commands[] = {states[4], states[4], states[1], states[4]}; 
  currentState = commands[counter];
  if(counter < 4){
    counter += 1;
  }
}
