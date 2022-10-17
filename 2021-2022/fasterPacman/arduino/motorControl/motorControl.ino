// motor libraries
#include <Adafruit_MotorShield.h>
#include <Encoder.h>
#include <Wire.h>

#include "utility/Adafruit_MS_PWMServoDriver.h"

// motor setup
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *myMotor1 = AFMS.getMotor(1);
Adafruit_DCMotor *myMotor2 = AFMS.getMotor(2);
// Encoder setup
Encoder encoder1(2, 1);
Encoder encoder2(3, 4);

// Sensor averaging value
float movingAverageA1;

void setup() {
  // put your setup code here, to run once:
  // motor setup
  AFMS.begin();
  myMotor1->setSpeed(255);

  // flashing light setup
  pinMode(13, OUTPUT);

  // read the input on analog pin 0:
  int sensorValue = analogRead(A0);
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  movingAverageA1 = sensorValue * (5.0 / 1023.0);

  // serial setup
  Serial.begin(9600);
}

void loop() {
  // read in the 2 encoders
  long readEncoder1 = encoder1.read();
  long readEncoder2 = encoder2.read();

  // print out the encoder values
  Serial.print("encoder1 = ");
  Serial.print(readEncoder1);
  Serial.print(", encoder2 = ");
  Serial.print(readEncoder2);

  // read the input on analog pin 0:
  int sensorValue = analogRead(A0);
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  float voltage = sensorValue * (5.0 / 1023.0);

  // update the moving average
  // defaulting to a = .5
  movingAverageA1 = (1 - .5) * movingAverageA1 + .5 * voltage;

  // print out the moving average
  Serial.print(", sensor voltage = ");
  Serial.print(voltage);
  Serial.print("\n");

  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    Serial.print("echo: ");
    Serial.print(data);
    Serial.print(";");

    String motorNumberStr = data.substring(0, 1);
    String motorSpeedStr = data.substring(1, 5);

    int motorNumber = motorNumberStr.toInt();
    int motorSpeed = motorSpeedStr.toInt();

    Serial.print("   you want to turn motor: ");
    Serial.print(motorNumber);
    Serial.print(" at speed ");
    Serial.print(motorSpeed);
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
