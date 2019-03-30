#include <PID_v1.h>
#include <Servo.h> 
#include <Wire.h>
#include <PID_AutoTune_v0.h>



/**
 * Servo Motors
 */
Servo leftServo;
Servo rightServo;

/*
 * Sensor values
 */

//PIN VALUES FOR SENSORS
int rightSensor = A0;
int leftSensor = A1;
int frontSensor = A2;

double rightInput;
double leftInput;
double frontInput;

/*
 * RPI values
 */
int rightRPI = 20;
int leftRPI = 18;
int upRPI = 16;
int downRPI = 14;

int directionState = 0;

//Define Variables we'll be connecting to
double leftSetpoint, rightSetpoint = 180;
double leftOutput = 93; 
double rightOutput = 93;

double kpL=2,kiL=0.5,kdL=2;
double kpR=2,kiR=0.5,kdR=2;

//Specify the links and initial tuning parameters
PID leftPID(&leftInput, &rightOutput, &leftSetpoint, kpL,kiL,kdL, DIRECT);
PID rightPID(&rightInput, &leftOutput, &rightSetpoint, kpR,kiR,kdR, DIRECT);
PID_ATune leftATune(&leftInput, &leftOutput);
PID_ATune rightATune(&rightInput, &rightOutput);

byte ATuneModeRememberL=2;
byte ATuneModeRememberR=2;

boolean tuningRight = true;
boolean tuningLeft = true;

void setup() {
  Serial.begin(9600);
  
  leftServo.attach(9);
  rightServo.attach(10);
  //Setup the pid 
  leftPID.SetMode(AUTOMATIC);
  rightPID.SetMode(AUTOMATIC);
    if(tuningLeft)
  {
    tuningLeft=false;
    changeAutoTune(leftATune, leftPID, tuningLeft);
    tuningLeft=true;
  }
  if(tuningRight){
    tuningRight=false;
    changeAutoTune(rightATune, rightPID, tuningRight);
    tuningRight=true;
    }
  
}

void loop() {
  //Serial.print(analogRead(rightSensor));
  //Serial.print(" ");
  //Serial.println(analogRead(leftSensor));
  if(tuningLeft)
  {
    Serial.println("Tuning Left");
    byte valLeft = (leftATune.Runtime());
    Serial.println(valLeft);
    if (valLeft!=0)
    {
      Serial.println("RunTime done");
      tuningLeft = false;
    }
   if(!tuningLeft)
    {
   //we're done, set the tuning parameters
    kpL = leftATune.GetKp();
    kiL = leftATune.GetKi();
    kdL = leftATune.GetKd();
    leftPID.SetTunings(kpL,kiL,kdL);
          Serial.println("Setting new tunes done");
    }
  }else{
          Serial.println("Computing PID");
      leftPID.Compute();
    }
    if(tuningRight)
  {
    byte valRight = (rightATune.Runtime());
    if (valRight!=0)
    {
      Serial.println("Tuning done");
      tuningRight = false;
    }
   if(!tuningRight)
    {
   //we're done, set the tuning parameters
    kpR = rightATune.GetKp();
    kiR = rightATune.GetKi();
    kdR = rightATune.GetKd();
    rightPID.SetTunings(kpR,kiR,kdR);
    }
  }else{
      rightPID.Compute();
    }
          Serial.println(leftOutput);
    Serial.println(rightOutput);
  //leftServo.write(leftOutput);
  //rightServo.write(183-rightOutput);

}



void changeAutoTune(PID_ATune Atune, PID pid, boolean tuning)
{
 if(!tuning)
  {
    ATune.SetNoiseBand(aTuneNoise);
    ATune.SetOutputStep(aTuneStep);
    ATune.SetLookbackSec((int)aTuneLookBack);
    AutoTuneHelper(true, pid);
    tuning = true;
  }
  else
  { //cancel autotune
    ATune.Cancel();
    tuning = false;
    AutoTuneHelper(false);
  }
}

void AutoTuneHelper(boolean start, PID pid, byte ATuneModeRemember)
{
  if(start)
    ATuneModeRemember = pid.GetMode();
  else
    pid.SetMode(ATuneModeRemember);
}
