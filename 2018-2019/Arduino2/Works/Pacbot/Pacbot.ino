#include <Servo.h> 
#include <Wire.h>
#include <MPU6050.h>
#include <MPU6050.h>
#define period 10000


//NEED https://github.com/jarzebski/Arduino-MPU6050 installed

/**
 * Servo Motors
 */
Servo myservo;
Servo myservo2;


/**
 * Gyroscope/Accelerometer
 */
MPU6050 mpu;

/*
 * Sensor values
 */
const int numReadings = 70;

int readingsRight[numReadings];      // the readings from the analog input - RIGHT
int readingsLeft[numReadings];      // the readings from the analog input - LEFT
int readingsFront[numReadings];      // the readings from the analog input -FRONT
int readIndexR = 0;               // the index of the current reading - R
int readIndexL = 0;               // the index of the current reading - L
int readIndexF = 0;               // the index of the current reading - F
int totalR = 0;                  // the running total - R
int averageR = 0;                // the average - R
int totalL = 0;                  // the running total -L
int averageL = 0;                // the average - l
int totalF = 0;                  // the running total - F
int averageF = 0;                // the average - F

//PIN VALUES FOR SENSORS
int rightSensor = A0;
int leftSensor = A1;
int frontSensor = A2;


int rightRPI = 20
int leftRPI = 18
int upRPI = 16
int downRPI = 14 

int directionState = 0;

void setup() {
  Serial.begin(9600);

  // Initializes the Gyro
  Serial.println("Initialize MPU6050");
  while(!mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G))
  {
    Serial.println("Could not find a valid MPU6050 sensor, check wiring!");
    delay(500);
  }
  mpu.calibrateGyro();
  mpu.setThreshold(3);

  // Initializes arrays for sensor readings to normalize
  
   for (int thisReading = 0; thisReading < numReadings; thisReading++) {
    readingsRight[thisReading] = 0;
  }
  for (int thisReading = 0; thisReading < numReadings; thisReading++) {
    readingsLeft[thisReading] = 0;
  }
  for (int thisReading = 0; thisReading < numReadings; thisReading++) {
    readingsFront[thisReading] = 0;
  }


  delay(2000);

}

void loop() {
  if(gyroTilt> 0){
      //left servo increase
    }else if (gyroTilt <0) {
      //right servo increases    
      }

   if !inRangeRight(){
      //right servo increases
    }else if (!inRangeLeft(){
      
      //left servo increases
      }

   //add up increase

   
}

/*
void tempShow()
{
    float temp = mpu.readTemperature();
    Serial.print(" Temp = ");
    Serial.print(temp);
    Serial.println(" *C");
    delay(400);
}
*/


int gyroTilt()
{
  //lcd.setCursor(0,0);
  Vector rawGyro = mpu.readRawGyro();
  Vector normGyro = mpu.readNormalizeGyro();
  Serial.print(" Xnorm = ");
  Serial.print(normGyro.XAxis);
  Serial.print(" Ynorm = ");
  Serial.print(normGyro.YAxis);
  Serial.print(" Znorm = ");
  Serial.println(normGyro.ZAxis);
  return rawGyro.XAxis;
  delay(200);
}

void accelShow()
{

  Vector rawAccel = mpu.readRawAccel();
  Vector normAccel = mpu.readNormalizeAccel();

  Serial.print(" Xnorm = ");
  Serial.print(normAccel.XAxis);
  Serial.print(" Ynorm = ");
  Serial.print(normAccel.YAxis);
  Serial.print(" Znorm = ");
  Serial.println(normAccel.ZAxis);
  delay(200);
}

/**
 * Function to return if the robot's right side is in good range
 */

boolean inRangeRight(){
    // subtract the last reading:
  totalR = totalR - readingsRight[readIndexR];
  // read from the sensor:
  readingsRight[readIndexR] = analogRead(rightSensor);
  // add the reading to the total:
  totalR = totalR + readingsRight[readIndexR];
  // advance to the next position in the array:
  readIndexR = readIndexR + 1;

  // if we're at the end of the array...
  if (readIndexR >= numReadings) {
    // ...wrap around to the beginning:
    readIndexR = 0;
  }

  // calculate the average:
  averageR = totalR / numReadings;
  // send it to the computer as ASCII digits
  if(averageR < 435){  //Is it in the range of NOT being too far from the wall or too close
      return true;
    }else {return false;}
  
  }

/**
 * Function to return if the robot's left side is in good range
 */


boolean inRangeLeft(){
    // subtract the last reading:
  totalL = totalL - readingsLeft[readIndexL];
  // read from the sensor:
  readingsLeft[readIndexL] = analogRead(leftSensor);
  // add the reading to the total:
  totalL = totalL + readingsLeft[readIndexL];
  // advance to the next position in the array:
  readIndexL = readIndexL + 1;

  // if we're at the end of the array...
  if (readIndexL >= numReadings) {
    // ...wrap around to the beginning:
    readIndexL = 0;
  }

  // calculate the average:
  averageL = totalL / numReadings;
  // send it to the computer as ASCII digits
  if(averageL < 201 || averageL > 231){
      return false;
    }else {return true;}
  
  }


/**  
 *   Returns if the robot has a wall in front of it
 */
boolean inRangeFront(){
    // subtract the last reading:
  totalF = totalF - readingsFront[readIndexF];
  // read from the sensor:
  readingsFront[readIndexF] = analogRead(frontSensor);
  // add the reading to the total:
  totalF = totalF + readingsFront[readIndexF];
  // advance to the next position in the array:
  readIndexF = readIndexF + 1;

  // if we're at the end of the array...
  if (readIndexF >= numReadings) {
    // ...wrap around to the beginning:
    readIndexF = 0;
  }

  // calculate the average:
  averageF = totalF / numReadings;
  // send it to the computer as ASCII digits
  if(averageF < 0 || averageF > 0){
      return true;
    }else {return false;}
  
  }
