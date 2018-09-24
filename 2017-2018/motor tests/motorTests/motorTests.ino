

#include "Pinout.h"
#include "motors.h"


int motorSpeed = 0;



void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  delay(1000);  

  //starts the indication LED
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  
  InitMotors();

  delay(1000);
}

void loop() {
  // put your main code here, to run repeatedly:
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
      case 'u':
        motorSpeed += 10;
        break;
      case 'd':
        motorSpeed -= 10;
        break;
    }
  }
  driveLeft(motorSpeed);
  driveRight(motorSpeed);
    
} 
