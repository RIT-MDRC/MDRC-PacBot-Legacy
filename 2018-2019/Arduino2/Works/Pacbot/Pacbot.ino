#include <MPU6050_tockn.h>
#include <MeOrion.h>
#include <Servo.h>
#include <Wire.h>
#include <string.h>

uint32_t offset = (.5) * 1000L;       // .5 sec

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
   RPI pin values
*/
int rightRPI = 13;
int leftRPI = 12;
int upRPI = 11;
int downRPI = 8;
int stopRPI = 4;

/*
    0 = up
    1 = down
    2 = left
    3 = right
*/
int directionState = 0;
int queueState = 0;

char currentPosition = "inWalls";
char previousPosition = "inWalls";

char *robotStates[] = {"turnfull", "turnright", "turnleft", "stop", "straight"};
char *currentState;
int counter = 0;

double gyroStartVal = 0.0;
double gyroRightVal = -78.1;
double gyroLeftVal = 74.2;
double gyro180Val = -700.5;

boolean completedTurn = true;
boolean completed180 = true;

int servoStopValue = 93;
int leftFull = 180;
int rightFull = 0;





void setup() {
  Serial.begin(9600);

  leftServo.attach(9);
  rightServo.attach(10);
  mpu6050.begin();

  mpu6050.setGyroOffsets( -3.85, -.65, .33);
}


void updatePosition() {
  if (seeWallRight() && seeWallLeft()) {
    if (currentPosition != "inWalls") {
      previousPosition = currentPosition;
      currentPosition = "inWalls";
    }
  } else {
    if (currentPosition != "opening") {

      previousPosition = currentPosition;
      currentPosition = "opening";
    }

  }
}


void adjustRight() {
  leftServo.write(97); //4 speed slow
  rightServo.write(87); //6 speed slow

}

void adjustTurnRight() {
  leftServo.write(180);
  rightServo.write(180);
  delay(600);
}

void adjustLeft() {
  leftServo.write(99); //6 speed slow
  rightServo.write(89); //4 speed slow
}

void adjustTurnLeft() {
  leftServo.write(0);
  rightServo.write(0);
  delay(180);
}

void adjustToCircumstance() {
  if (previousPosition == "opening") {
    for ( uint32_t tStart = millis();  (millis() - tStart) < offset;  ) {
      moveBackwards();
    }
    Serial.println("Adjusted Backward");
  } else {
    for ( uint32_t tStart = millis();  (millis() - tStart) < offset;  ) {
      moveStraight();
    }
    Serial.println("Adjusted Forward");
  }
}




void stopMotors() {
  leftServo.write(93);
  rightServo.write(93);
}

void turnAround180() {
  mpu6050.update();
  while (mpu6050.getAngleZ() > (gyro180Val + gyroStartVal)) {
    mpu6050.update();
    Serial.print(gyro180Val + gyroStartVal);
    Serial.print("  ");
    Serial.println(mpu6050.getAngleZ());

    if (wallCloseRight()) {
      Serial.println("Did not complete turn");
      adjustTurnLeft();
      adjustToCircumstance();
    } else {
      leftServo.write(180);
      rightServo.write(180);
    }
  }
  Serial.println("Turning Right Done");

  gyroStartVal = gyro180Val + gyroStartVal;
}


boolean wallCloseRight() {
  return rightSensor.distanceCm() < 4.3;
}

boolean seeWallRight() {
  delay(100);
  //Serial.print(rightSensor.distanceCm());
  return rightSensor.distanceCm() < 14;
}

boolean wallCloseLeft() {

  return leftSensor.distanceCm() < 3.6;
}

boolean seeWallLeft() {
  delay(100);
  return leftSensor.distanceCm() < 12;

}

boolean wallCloseFront() {
  return frontSensor.distanceCm() < 5;
}

void turnAround90CW() {
  boolean wasInWalls = false;
  while (seeWallLeft() && seeWallRight()) {
    moveStraight();
    wasInWalls = true;
  }
  if (wasInWalls) {
    for ( int tStart = millis();  (millis() - tStart) < offset;  ) {
      moveStraight();
    }
  }
  Serial.println("Turning Right");
  updatePosition(); // not in walls
  mpu6050.update();
  while (mpu6050.getAngleZ() > (gyroRightVal + gyroStartVal)) {
    mpu6050.update();
    Serial.print(gyroRightVal + gyroStartVal);
    Serial.print("  ");
    Serial.println(mpu6050.getAngleZ());

    if (wallCloseRight()) {
      Serial.println("Did not complete turn");
      adjustTurnLeft();
      adjustToCircumstance();
    } else {
      leftServo.write(180);
      rightServo.write(180);
    }
  }
  Serial.println("Turning Right Done");

  gyroStartVal = gyroRightVal + gyroStartVal;
}

void turnAround90CCW() {
  boolean wasInWalls = false;
  while (seeWallLeft() && seeWallRight()) {
    moveStraight();
    wasInWalls = true;
  }
  if (wasInWalls) {
    for ( int tStart = millis();  (millis() - tStart) < offset;  ) {
      moveStraight();
    }
  }
  updatePosition(); // not in walls
  Serial.println("Turning Left");
  mpu6050.update();
  while (mpu6050.getAngleZ() < (gyroLeftVal + gyroStartVal)) {
    Serial.println(gyroLeftVal + gyroStartVal);
    Serial.println(mpu6050.getAngleZ());
    mpu6050.update();
    if (wallCloseLeft()) {
      adjustRight();
      adjustToCircumstance();
    } else {
      leftServo.write(0);
      rightServo.write(0);
    }
  }
  gyroStartVal = gyroLeftVal + gyroStartVal;
}



void moveStraight() {
  if (wallCloseFront()) {
    stopMotors();
  }
  else {
    Serial.println("Moving Forwards");
    if (wallCloseRight()) {
      Serial.print("stop right");
      //delay(1000);
      adjustRight();
      delay(100);
    }
    else if (wallCloseLeft() ) {
      Serial.print("stop left");
      //delay(1000);


      adjustLeft();
      delay(100);
    }
    leftServo.write(180);
    rightServo.write(0);
  }
   
}

void moveBackwards() {
  Serial.println("Moving Backwards");
  if (wallCloseRight()) {
    Serial.print("stop right");
    adjustRight();
    delay(100);
  }
  else if (wallCloseLeft() ) {
    Serial.print("stop left");
    adjustLeft();
    delay(100);
  }
  else {
    leftServo.write(0);
    rightServo.write(180);
  }

}

void loop() {



  
    if(digitalRead(upRPI) == HIGH ){

       Serial.print("Go UP");
        switch(directionState){
          case 0: 
                  moveStraight();
                  break;
          case 1: 
                  turnAround180();
                  directionState = 1;
                  break;
          case 2: 
                  turnAround90CW();
                  directionState = 2;
                  break;
          case 3: 
          
                  turnAround90CCW();
                  directionState = 3;
                  break;
          default: moveStraight();
                  break;
          }


      }else if(digitalRead(downRPI) ==HIGH){
        Serial.print("Go down");
              switch(directionState){
                case 0: 
                        turnAround180();
                        directionState = 0;
                        break;
                case 1: 
                        moveStraight();
                        
                        break;
                case 2: 
                        turnAround90CCW();
                        directionState = 2;
                        break;
                case 3: 
                        turnAround90CW();
                        directionState = 3;
                        break;
                default: moveStraight();
                        break;
                }


        }else if(digitalRead(leftRPI) == HIGH){
          Serial.print("Go left");
              switch(directionState){
                case 0: 
                        turnAround90CCW();
                        directionState = 0;
                        break;
                case 1: 
                        turnAround90CW();
                        directionState = 1;
                        break;
                case 2: 
                        moveStraight();
                    
                        break;
                case 3: 
                        turnAround180();
                        directionState = 3;
                        break;
                default: moveStraight();
                        break;
                }


          }else if(digitalRead(rightRPI) == HIGH){
            Serial.print("Go right");
              switch(directionState){
                case 0: 
                        turnAround90CW();
                        directionState = 0;
                        break;
                case 1: 
                        turnAround90CCW();
                        directionState = 1;
                        break;
                case 2: 
                        turnAround180();
                        directionState = 2;
                        break;
                case 3: 
                        moveStraight();
                        break;
                default: moveStraight();
                        break;
                }


          }else{
                stopMotors();
              }




}
