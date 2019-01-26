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

#define USED -1

//the values to output to the motors
int leftSpeed = 0;
int rightSpeed = 0;

bool openLeft = false;
bool openRight = false;
bool reverse = false;

int motorOffset = 0;

bool stopped = true;
bool turning = false;

char cmd;

//initial: East, counterClockwise: Positive.
int newHeading = 0;
int rhc = 0; //relativeHeadingChange
int wantedHeading = 0;
int currentHeading = 0;



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


void loop() 
{
    if(stopped) {Serial.println("Stopped")}
    while(stopped)
    {
        if (Serial.available())  
        {
            cmd = Serial.read();  //Sets inch to char on serial port
            switch(cmd)
            {
                case'G':
                case'g':
                    stopped = false;
                    break;
            }
        }
    }

    char msg[80]

    digitalWrite(LED_PIN, HIGH);

    if(Serial.available())
    {
        cmd = Serial.read();
        switch(cmd)
        {
            case 'E':
                newHeading = 0;
                break;
            case 'W':
                newHeading = 180;
                break;
            case 'N':
                newHeading = 90;
                break;
            case 'S':
                newHeading = 270;
                break;
            case 'P';
                stopped = true;
                break;        
        }

        if(newHeading != USED)
        {
            
        }
        //compare chars instead of angle
    }

    updateSensors();

    //record left sensor; open -> openLeft = true
    //record right sensor; open -> openRight = true

    currentHeading += (getGyroRate() * GYRO_OFFSET) * LOOP_TIME_SECONDS;
    motorOffset = headingPID(currentHeading, wantedHeading);

    if((newHeading = wantedHeading + 90 && openRight) ||
        (newHeading = wantedHeading - 90 && openLeft))
    {
        wantedHeading = newHeading;
        newHeading = USED;
        while(abs(wantedHeading - currentHeading) < 5) //less than 5 degrees offset
        {
            turnBot(turningPID(wantedHeading, currentHeading));
        }
        
    }


}