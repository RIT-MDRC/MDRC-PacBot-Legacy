// motor libraries
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

// motor setup
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
Adafruit_DCMotor *myMotor1 = AFMS.getMotor(1);
Adafruit_DCMotor *myMotor2 = AFMS.getMotor(2);


void setup() {
  // put your setup code here, to run once:
  // motor setup
  AFMS.begin();
  myMotor1->setSpeed(255);

  // flashing light setup
  pinMode(13, OUTPUT);

  // serial setup
  Serial.begin(9600);
}

void loop() {

  // read the input on analog pin 0:
  int sensorValue = analogRead(A0);
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  float voltage = sensorValue * (5.0 / 1023.0);

  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    Serial.print("echo: ");
    Serial.print(data);
    Serial.print(";");

    String motorNumberStr = data.substring(0, 1);
    String motorSpeedStr = data.substring(1, 5);

    int motorNumber = motorNumberStr.toInt();
    int motorSpeed = motorSpeedStr.toInt();

    // read the input on analog pin 0:
    int sensorValue = analogRead(A0);
    // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
    float voltage = sensorValue * (5.0 / 1023.0);

    Serial.print("   you want to turn motor: ");
    Serial.print(motorNumber);
    Serial.print(" at speed ");
    Serial.print(motorSpeed);
    Serial.print("; voltage = ");
    Serial.print(voltage);
    Serial.print("\n");
    
    if (motorSpeed == 0) {
      digitalWrite(13, LOW);
      if (motorNumber == 1) {
        myMotor1->run(RELEASE);
      } else if (motorNumber == 2) {
        myMotor2->run(RELEASE);
      }
    } else {
      digitalWrite(13, HIGH);
      if (motorNumber == 1) {
        myMotor1->setSpeed(abs(motorSpeed));
        if (motorSpeed < 0) {
          myMotor1->run(BACKWARD);
        } else {
          myMotor1->run(FORWARD);
        }
      } else if (motorNumber == 2) {
        myMotor2->setSpeed(abs(motorSpeed));
        if (motorSpeed < 0) {
          myMotor2->run(BACKWARD);
        } else {
          myMotor2->run(FORWARD);
        }
      }
    }
    
  }
}
