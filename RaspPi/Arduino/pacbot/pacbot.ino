/**
 * pacbot.ino
 * Ethan Yaccarino-Mims
 * the main arduino program for MDRC pacbot
 */

#include "Pinout.h"
#include "sensors.h"
#include "motors.h"
#include "PID.h"

//loop time in micro seconds
#define STD_LOOP_TIME 5000

//loop time in seconds
#define LOOP_TIME_SECONDS STD_LOOP_TIME/1000000 

//the offset for the gyro value
#define GYRO_OFFSET 0

//the wanted angle
int wantedAngle = 0; //0:right, 90:up, 180:left, 270:down

//the actual angle
int angle = 0; //stores the current angle based off of starting angle

//an arbitrary measurement of the distance to the left wall
int left = 0;

//an arbitrary measurement of the distance to the right wall
int right = 0; 

//is the pacman waiting for a command?
boolean waitingDirection = true;

//if the pacman has been stopped by the game
boolean stopKey = true;

//the values to output to the motors
int leftMotor;
int rightMotor;

//variables relevant to the control structure for the loop timing 
uint32_t lastLoopTime = STD_LOOP_TIME;
uint32_t lastLoopUsefulTime = STD_LOOP_TIME;
uint32_t loopStartTime = 0;


/**
 * initializes all needed values and objects
 */
void setup() 
{
  //starts the serial port at a baud rate of 115200
  Serial.begin(115200);

  delay(1000);  

  //starts the indication LED
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  //initializes all data in the .h files
  initMotors();
  initSensors();
  initPID();
  
  delay(1000);
}


/**
 * the main loop
 */
void loop() 
{
  //used to stop the pacman
  while(stopKey)
  {
    char chPC;
    Serial.println("Stopped");
    if (Serial.available())  
    {
      chPC = Serial.read();  //Sets inch to char on serial port
      switch(chPC)
      {
        case'G':
        case'g':
          stopKey = false;
      }
    }
  }

  //the message buffer
  char msg[80];

  //the char from the serial port
  char cmd;

  //toggle LED
  digitalWrite(LED_PIN, HIGH);

  if(Serial.available())
  {
    cmd = Serial.read();
    switch(cmd)
    {
      case'j':
        polar = 90;
        waitingDirection = false;
        break;
      case'h':
        polar = 180;
        waitingDirection = false;
        break;
      case'k':
        polar = 270;
        waitingDirection = false;
        break;
      case'l':
        polar = 0;
        waitingDirection = false;
        break;
      case's':
        stopKey = true;
        waitingDirection = true;
    }

     
  }
  //update sensors
  updateSensors();

  //get new angle
  angle += (getGyroRate() + gyroOffset) * LoopTimeSeconds;

  //TODO


  //loop timing control structure
  lastLoopUsefulTime = micros() - loopStartTime;
  if(lastLoopUsefulTime < STD_LOOP_TIME)
  delayMicroseconds(STD_LOOP_TIME - lastLoopUsefulTime);
  loopStartTime = micros();
}
