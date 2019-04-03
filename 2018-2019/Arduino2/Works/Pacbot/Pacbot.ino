#include <MPU6050_tockn.h>
#include <MeOrion.h>
#include <Servo.h>
#include <Wire.h>
#include <string.h>

MPU6050 mpu6050(Wire);
/**
   Servo Motors
*/
Servo leftServo;
Servo rightServo;

/*
   Sensor values
*/

//PIN VALUES FOR SENSORS
int rightSensorPin = A1;
int leftSensorPin = A0;
int frontSensorPin = A2;


MeUltrasonicSensor leftSensor(PORT_8);
MeUltrasonicSensor rightSensor(PORT_7);
MeUltrasonicSensor frontSensor(PORT_6);

double rightInput = 0;
double leftInput = 0;
double frontInput = 0;

/*
   RPI values
*/
int rightRPI = 13;
int leftRPI = 12;
int upRPI = 11;
int downRPI = 8;
int stopRPI = 4;

/*
 *  0 = up
 *  1 = down
 *  2 = left
 *  3 = right
 *  4 = stop
 */
int directionState = 0; 
int queueState = 0;

char *states[] = {"turnfull", "turnright", "turnleft", "stop", "straight"};
char *currentState;
int counter = 0; 

double gyroStartVal = 0.0;
double gyroTurnedVal = -88.1;
double gyro180Val= -176.5;

boolean completedTurn = true;
boolean completed180 = true;



void setup() {
  Serial.begin(9600);

  leftServo.attach(9);
  rightServo.attach(10);
  mpu6050.begin();

  mpu6050.setGyroOffsets( -3.85, -.65, .33);
}


void adjustRight() {
  leftServo.write(97); //4 speed slow
  rightServo.write(87); //6 speed slow

}

void adjustTurnRight(){
  leftServo.write(93);
  rightServo.write(93);
  }

void adjustTurnLeft(){
  leftServo.write(93);
  rightServo.write(93); 
  }

void adjustForward(){
  
  }

void adjustBackward(){
  
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
  turnAround90CW();
  turnAround90CW();
}


boolean wallRight(){
  
  
  }


boolean wallLeft(){
    return leftSensor.distanceCm() < 5;
  
  }

boolean wallFront(){
  }

void turnAround90CW() {
  while(mpu6050.getAngleZ() < gyroTurnedVal){
        if(wallRight()){
          completedTurn = false;
          break;}
        leftServo.write(180);
        rightServo.write(180);
    }
    if(!completedTurn){
        adjustTurnLeft();
        if(wallFront){
        adjustForward();
        }else{
          adjustBackward();
          }
        turnAround90CW();
        completedTurn = true;
      }
}

void turnAround90CCW(){
  Serial.println("Trying");
 Serial.println(mpu6050.getAngleZ());
   mpu6050.update();
  while(mpu6050.getAngleZ() < abs(gyroTurnedVal)){
     mpu6050.update();
        if(wallLeft()){
          leftServo.write(93);
        rightServo.write(93); break;}
        
          //Serial.println("wallLEft");
          //completedTurn = false;
          //break;}
          Serial.println("turning");
        leftServo.write(0);
        rightServo.write(0);
    }
    if(!completedTurn){
        adjustTurnRight();
        if(wallFront){
        adjustForward();
        }else{
          adjustBackward();
          }
        turnAround90CCW();
        completedTurn = true;
      };  
              leftServo.write(93);
        rightServo.write(93);
}



void moveStraight(int readRight, int readLeft) {
  if (wallRight()) {
    Serial.print("stop right");
    //delay(1000);
    stopMotors();
    adjustRight();
  }
  else if (wallLeft() ) {
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
  /*
  Serial.print(analogRead(rightSensor));
  Serial.print(" ");
  Serial.println(analogRead(leftSensor));
  */

/*
  if(digitalRead(upRPI) == HIGH ){
      if(directionState != 0){
          
      }

    
    }else if(digitalRead(downRPI) ==HIGH){
        if(directionState != 1){
          
        }


      
      }else if(digitalRead(leftRPI) == HIGH){
        if(directionState != 2){
          
        }


        
        }else if(digitalRead(rightRPI) == HIGH){
            if(directionState != 3){
          
            }

          
          }else{

            
            }
            */
     /*       
  int readRight = analogRead(rightSensor);
  int readLeft = analogRead(leftSensor);
  int readFront = analogRead(frontSensor);
  mpu6050.update();

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
    */

    turnAround90CCW();
    while(1){};
  }

  


  
