/**
 * pacbot.ino
 * Ethan Yaccarino-Mims
 * the main arduino program for MDRC pacbot
 */

#include "Pinout.h"
#include "sensors.h"
#include "motors.h"
#include "PID.h"
#include <QueueList.h>

//loop time in micro seconds
#define STD_LOOP_TIME 5000

//loop time in seconds
#define LOOP_TIME_SECONDS STD_LOOP_TIME/1000000 

//the offset for the gyro value
#define GYRO_OFFSET 0

#define MOTOR_OFFSET_WEIGHT 1

//the queue of commands
QueueList <int> queue

//the wanted angle
int wantedAngle = 0; //0:right, 90:up, 180:left, 270:down

//the actual angle
int angle = 0; //stores the current angle based off of starting angle

//an arbitrary measurement of the distance to the left wall
int leftDistance = 0;

//an arbitrary measurement of the distance to the right wall
int rightDistance = 0; 

//an arbitrary measurement of the distance to the wall infront
int frontDistance = 0;

//the front distance reading on the last loop
int lastFrontDistance = 0;

int runMotors = false;

int nextTurn = 0;

//the next turn
int queue.push(0;

//is the pacman waiting for a command?
boolean waitingDirection = true;

//if the pacman has been stopped by the game
boolean stopKey = true;


boolean openingPresent = false;


boolean turning = false;

//the values to output to the motors
int leftSpeed = 0;
int rightSpeed = 0;

int motorOffset = 0;

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
  Serial.begin(9600);

  delay(1000);  

  //starts the indication LED
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  //initializes all data in the .h files
  InitMotors();
  InitSensors();
  InitPID();
  
  delay(1000);
}


/**
 * the main loop
 */
void loop() 
{
  //used to stop the pacman
  if(stopKey)
  {
    Serial.println("Stopped");
    while(stopKey)
    {
      char chPC;
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
      case '1':
        queue.push(1);
        break;
      case '!':
        queue.push(-1);
        break;
      case '2':
        queue.push(2);
        break;
      case '@':
        queue.push(-2);
        break;
      case '3'
        queue.push(3);
        break;
      case '#':
        queue.push(-3);
        break;
      case '4':
        queue.push(4);
        break;
      case '$':
        queue.push(-4);
        break;
      case '5':
        queue.push(5);
        break;
      case '%':
        queue.push(-5);
        break;
      case '6':
        queue.push(6);
        break;
      case '^':
        queue.push(-6);
        break;
      case '7':
        queue.push(7);
        break;
      case '&':
        queue.push(-7);
      case '0':
        queue.push(180);
        break;
      case 's':
        stopKey = true;
        waitingDirection = true;
        break;
    }
  }
  //update sensors
  updateSensors();
  
   //TODO
  
  leftDistance = FilterSensor(analogRead(LEFT_IR));
  rightDistance = FilterSensor(analogRead(RIGHT_IR));

  angle += (getGyroRate() + GYRO_OFFSET) * LOOP_TIME_SECONDS;
  motorOffset = headingPID(angle, wantedAngle);

  if(!queue.isEmpty || !waitingDirection)
  {
    if(waitingDirection)
    {
      nextTurn = queue.pop();
      waitingDirection = false;
      lastLeft = leftDistance;
      lastRight = rightDistance;
      moving = true;
    }
    else if(turning)
      {
        if(abs(wantedAngle - angle) < 2)
        {
          turning = false;
          waitingDirection = true;
        }
      }
    else if(moving)
      {
        runMotors = true;
        if(180 == nextTurn)
        {
          turning = true;
          wantedAngle = angle + 180;
        }
        else
        {
          if(!containsWall(leftDistance, lastLeft) || !containsWall(rightDistance, lastRight))
          {
            if(-1 == nextTurn) //turn left
            {
              turning = true;
              moving = false;
              wantedAngle -= 90;
              runMotors = false;
            }
            else if(1 == nextTurn)
            {
              turning = true;
              moving = false;
              wantedAngle += 90;
              runMotors = false
            }
            else if(!openingPresent)
            {
              if(nextTurn >= 0)
              {
                nextTurn -= 1;  
              }
              else
              {
                nextTurn += 1;
              }
            }
          }
          else if(!containsWall(rightDistance, lastRight)
          {
            
          }
          else
          {
            motorOffset += laneKeepPID(leftDistance, rightDistance); 
          }
      }
  }
  else
  {
      
  }
  
  //get new angle
  

 
  lastLeft = leftDistance;
  lastRight = rightDistance;
  motorOffset += laneKeepPID(leftDistance, rightDistance);
  

  Serial.print(frontDistance);
  Serial.print("    ");
  Serial.print(leftDistance); 
  Serial.print("    ");
  Serial.print(rightDistance);
  Serial.println("");

  lastFrontDistance = frontDistance;

  //loop timing control structure
  lastLoopUsefulTime = micros() - loopStartTime;
  if(lastLoopUsefulTime < STD_LOOP_TIME)
  delayMicroseconds(STD_LOOP_TIME - lastLoopUsefulTime);
  loopStartTime = micros();
}
