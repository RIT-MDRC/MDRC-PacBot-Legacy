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

long randNumber;

MeUltrasonicSensor leftSensor(PORT_8);
MeUltrasonicSensor rightSensor(PORT_7);
MeUltrasonicSensor frontSensor(PORT_6);

double rightInput = 0;
double leftInput = 0;
double frontInput = 0;

/*
   RPI pin values
*/
int rightRPI = 4;
int leftRPI = 12;
int upRPI = 11;
int downRPI = 8;
int stopRPI = 3;

/*
    0 = up
    1 = down
    2 = left
    3 = right
*/
int directionState = -1;
int queueState = 0;

char currentPosition[8] = "inWalls";
char previousPosition[8] = "inWalls";

const char *robotStates[6] = {"turnfull", "turnright", "turnleft", "stop", "straight"};
char *currentState;
int counter = 0;

double gyroStartVal = 0.0;
//double gyroRightVal = -78.1;
double gyroRightVal = -39.1;
//double gyroLeftVal = 74.2;
double gyroLeftVal = 40.2;
double gyro180Val = -700.5;

boolean completedTurn = true;
boolean completed180 = true;

int servoStopValue = 93;
int leftFull = 180;
int rightFull = 0;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  leftServo.attach(9);
  rightServo.attach(10);
  mpu6050.begin();

  //mpu6050.setGyroOffsets( -3.85, -.65, .33);
  //mpu6050.setGyroOffsets(128, 24, -10);
  mpu6050.calcGyroOffsets(true);


  pinMode(upRPI, INPUT_PULLUP);
  pinMode(rightRPI, INPUT_PULLUP);
  pinMode(leftRPI, INPUT_PULLUP);
  pinMode(downRPI, INPUT_PULLUP);
  pinMode(stopRPI, INPUT_PULLUP);

  randomSeed(analogRead(2));

}


void updatePosition() {
  if (seeWallRight() && seeWallLeft()) {
    if (strcmp(currentPosition, "inWalls") != 0 ) {
      strcpy(previousPosition, currentPosition);
      strcpy(currentPosition, "inWalls");
    }
  } else {
    if (strcmp(currentPosition, "opening") != 0) {

      strcpy(previousPosition, currentPosition);
      strcpy(currentPosition, "opening");
    }

  }
}


void adjustRight() {
  leftServo.write(97); //9 speed slow
  rightServo.write(87); //5 speed slow

}

void adjustTurnRight() {
  leftServo.write(180);
  rightServo.write(180);
  delay(180);
}

void adjustLeft() {
  leftServo.write(99); //5 speed slow
  rightServo.write(89); //9 speed slow
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
  delay(50);
  return rightSensor.distanceCm() < 4.7 || (rightSensor.distanceCm() > 350);
}

boolean seeWallRight() {
  delay(50);
  Serial.print("rightsensor: ");
  Serial.print(rightSensor.distanceCm());
  Serial.print("          ");
  return rightSensor.distanceCm() < 14 || (rightSensor.distanceCm() > 350);
}

boolean wallCloseLeft() {
  delay(50);
  return leftSensor.distanceCm() < 4 || (leftSensor.distanceCm() > 350);
}

boolean seeWallLeft() {
  delay(50);
  Serial.print("leftsensor: ");
  Serial.print(leftSensor.distanceCm());
  Serial.print("          ");
  return leftSensor.distanceCm() < 12 || (leftSensor.distanceCm() > 350);

}

boolean wallCloseFront() {
  delay(50);
  Serial.print("frontsensor: ");
  Serial.print(frontSensor.distanceCm());
  Serial.print("          ");
  return (frontSensor.distanceCm() < 4.5) || (frontSensor.distanceCm() > 350) ;
}



void turnAround90CCW() {
  //  boolean wasInWalls = false;
  //  while (seeWallLeft() && seeWallRight()) {
  //    moveStraight();
  //    wasInWalls = true;
  //  }
  //  if (wasInWalls) {
  //    for ( int tStart = millis();  (millis() - tStart) < offset;  ) {
  //      moveStraight();
  //    }
  //  }
  updatePosition(); // not in walls
  mpu6050.update();
  while (mpu6050.getAngleZ() < (gyroLeftVal + gyroStartVal)) {
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
  //delay(500);
}



void moveStraight() {
  //  if (wallCloseFront()) {
  //    stopMotors();
  //  }
  //  else {
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
  //}

}

void tester() {
  //Moving straight until it hits a intersection
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
  stopMotors();
  //delay(500);
  //WHAT HAPPENS AT THE INTERSECTION **REMEMBER TO COMMENT OUT THE TURNS
  //Test moving straight
  //Test all the bad conditions where it will hit a wall and other stuff
  turnAround90CW();


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

void turnAround90CW() {
  //  boolean wasInWalls = false;
  //  while (seeWallLeft() && seeWallRight()) {
  //    moveStraight();
  //    wasInWalls = true;
  //  }
  //  if (wasInWalls) {
  //    for ( int tStart = millis();  (millis() - tStart) < offset;  ) {
  //      moveStraight();
  //    }
  //  }
  updatePosition(); // not in walls
  mpu6050.update();
  while (mpu6050.getAngleZ() > (gyroRightVal + gyroStartVal)) {
    mpu6050.update();
    if (wallCloseRight()) {
      adjustTurnLeft();
      adjustToCircumstance();
    } else {
      leftServo.write(180);
      rightServo.write(180);
    }
  }

  gyroStartVal = gyroRightVal + gyroStartVal;
}


void backup() {
  //  //Moving straight until it hits a intersection
  //  boolean wasInWalls = false;
  //  while (seeWallLeft() && seeWallRight()) {
  //    moveStraight();
  //    wasInWalls = true;
  //  }
  //  if (wasInWalls) {
  //    //    for ( int tStart = millis();  (millis() - tStart) < offset;  ) {
  //    //      moveStraight();
  //    //    }
  //    int starttime = millis();
  //    int endtime = starttime;
  //    while ((endtime - starttime) <= 450) // do this loop for up to 1000mS
  //    {
  //      moveStraight();
  //      endtime = millis();
  //    }
  //    stopMotors();
  //  }
  // stopMotors();
  //delay(500);
  //WHAT HAPPENS AT THE INTERSECTION
  //
  if (!seeWallLeft() && seeWallRight()) {
    //turnAround90CCW();
    adjustTurnLeft();
    //      moveStraight();
    //      delay(700);
    int starttime = millis();
    int endtime = starttime;
    while ((endtime - starttime) <= 700) // do this loop for up to 1000mS
    {
      moveStraight();
      endtime = millis();
    }
    stopMotors();
  }
  else if (!seeWallRight() && seeWallLeft()) {
    //turnAround90CW();
    adjustTurnRight();
    //      moveStraight();
    //      delay(700);
    int starttime = millis();
    int endtime = starttime;
    while ((endtime - starttime) <= 700) // do this loop for up to 1000mS
    {
      moveStraight();
      endtime = millis();
    }
    stopMotors();
  }
  else if (!seeWallLeft() && !seeWallRight()) {
    randNumber = random(2);
    if (randNumber == 0) {
      //turnAround90CCW();
      adjustTurnLeft();
      //        moveStraight();
      //        delay(700);
      int starttime = millis();
      int endtime = starttime;
      while ((endtime - starttime) <= 700) // do this loop for up to 1000mS
      {
        moveStraight();
        endtime = millis();
      }
      stopMotors();
    }
    else {
      //turnAround90CW();
      adjustTurnRight();
      //        moveStraight();
      //        delay(700);
      int starttime = millis();
      int endtime = starttime;
      while ((endtime - starttime) <= 700) // do this loop for up to 1000mS
      {
        moveStraight();
        endtime = millis();
      }
      stopMotors();
    }
    // }
  } else {
    //Moving straight until it hits a intersection
    boolean wasInWalls = false;
    while (seeWallLeft() && seeWallRight()) {
      moveStraight();
      wasInWalls = true;
    }
    if (wasInWalls) {
      //    for ( int tStart = millis();  (millis() - tStart) < offset;  ) {
      //      moveStraight();
      //    }
      int starttime = millis();
      int endtime = starttime;
      while ((endtime - starttime) <= 450) // do this loop for up to 1000mS
      {
        moveStraight();
        endtime = millis();
      }
      stopMotors();
    }
    //  stopMotors();
  }
  //  else {
  //    if (!seeWallRight()) {
  //      //turnAround90CW();
  //      adjustTurnRight();
  //      //        moveStraight();
  //      //        delay(700);
  //            int starttime = millis();
  //      int endtime = starttime;
  //      while ((endtime - starttime) <= 700) // do this loop for up to 1000mS
  //      {
  //        moveStraight();
  //        endtime = millis();
  //      }
  //    } else {
  //      //turnAround90CCW();
  //      adjustTurnLeft();
  //      //        moveStraight();
  //      //        delay(700);
  //      int starttime = millis();
  //      int endtime = starttime;
  //      while ((endtime - starttime) <= 700) // do this loop for up to 1000mS
  //      {
  //        moveStraight();
  //        endtime = millis();
  //      }
  //    }
  //  }

}

void getSensorValues() {
  seeWallLeft();
  seeWallRight();
  wallCloseFront();
  Serial.println("");
}

void loop() {
  //PIzeroOperations();
  backup();
  //PIzeroOperationsTwo();
  //turnAround90CW();
  //getSensorValues();
}
