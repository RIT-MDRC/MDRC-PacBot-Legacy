#include <MPU6050.h>
#include <Servo.h>
#include <Wire.h>
#include <string.h>


MPU6050 mpu;


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

double gyroStartVal;
double gyroTurnedVal;
double gyro180Val;

boolean completedTurn = true;
boolean completed180 = true;



void setup() {
  Serial.begin(9600);

  leftServo.attach(A0);
  rightServo.attach(A1);
  
    // Initialize MPU6050
  Serial.println("Initialize MPU6050");
  while(!mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G))
  {   Serial.println("Could not find a valid MPU6050 sensor, check wiring!");
    delay(500);
  }

   // If you want, you can set gyroscope offsets
  // mpu.setGyroOffsetX(155);
  // mpu.setGyroOffsetY(15);
  // mpu.setGyroOffsetZ(15);
  
  // Calibrate gyroscope. The calibration must be at rest.
  // If you don't want calibrate, comment this line.
  mpu.calibrateGyro();

  // Set threshold sensivty. Default 3.
  // If you don't want use threshold, comment this line or set 0.
  mpu.setThreshold(3);

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
  
  
  }

boolean wallFront(){
  }

void turnAround90CW() {
  while(mpu.readNormalizeGyro().XAxis < gyroTurnedVal){
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
  while(mpu.readNormalizeGyro().XAxis < gyroTurnedVal){
        if(wallLeft()){
          completedTurn = false;
          break;}
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
  
  Serial.print(analogRead(rightSensor));
  Serial.print(" ");
  Serial.println(analogRead(leftSensor));


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
            
  int readRight = analogRead(rightSensor);
  int readLeft = analogRead(leftSensor);
  int readFront = analogRead(frontSensor);

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
