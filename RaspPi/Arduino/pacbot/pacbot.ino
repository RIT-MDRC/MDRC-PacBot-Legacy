#include "Pinout.h"
#include "sensors.h"
#include "motors.h"
#include "PID.h"



#define STD_LOOP_TIME 5000
#define LOOP_TIME_SECONDS STD_LOOP_TIME/1000000 
#define GYRO_OFFSET 0


int wantedAngle = 0; //0:right, 90:up, 180:left, 270:down
int angle = 0; //stores the current angle based off of starting angle
int right = 0; //which side is left
int left = 0; //which side is right

boolean waitingDirection = true;
boolean stopKey = true;

int motor1;
int motor2;
int motor3;


uint32_t lastLoopTime = STD_LOOP_TIME;
uint32_t lastLoopUsefulTime = STD_LOOP_TIME;
uint32_t loopStartTime = 0;



void setup() 
{
  // put your setup code here, to run once:
  Serial.begin(115200);
  delay(1000);  
  Serial.println("Starting...");

  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  initMotors();
  initSensors();
  initPID();
  
  delay(1000);
    

}

void loop() 
{
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


  char msg[80];
  char cmd;

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
  updateSensors();
  angle += (getGyroRate() + gyroOffset) * LoopTimeSeconds
  
  //between walls

  lastLoopUsefulTime = micros() - loopStartTime;
  if(lastLoopUsefulTime < STD_LOOP_TIME)
  delayMicroseconds(STD_LOOP_TIME - lastLoopUsefulTime);
  loopStartTime = micros();
}
