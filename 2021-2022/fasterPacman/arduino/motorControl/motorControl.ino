// motor libraries
#include <Adafruit_MotorShield.h>
#include <Encoder.h>
#include <Wire.h>

#include "utility/Adafruit_MS_PWMServoDriver.h"

// uncomment for debugging information to be printed to serial
#define DEBUG

// motor setup
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *myMotor1 = AFMS.getMotor(1);
Adafruit_DCMotor *myMotor2 = AFMS.getMotor(2);
// Encoder setup
Encoder encoder1(2, 1);
Encoder encoder2(3, 4);

// Sensor averaging value
float movingAverages[5];

//Motor1 = Left, Motor2 = right
int motor1_targetVel; //target velocity for feedback control
int motor2_targetVel;

int motor1_inputVel; //value to send to motors
int motor2_inputVel;
//counters for amount of rising edges on pins 2 and 3 from encoders.
volatile unsigned long enc1_count = 0;
volatile unsigned long enc2_count = 0;
void setup() {
  // put your setup code here, to run once:
  // motor setup
  AFMS.begin();

  // flashing light setup
  pinMode(13, OUTPUT);

  // serial setup
  Serial.begin(115200);

  pinMode(2,INPUT_PULLUP);
  attachInterrupt(0, isr_enc1_count, RISING); //interrupt signal to pin 2

  pinMode(3,INPUT_PULLUP);
  attachInterrupt(0, isr_enc2_count, RISING); //interrupt signal to pin 2

  //read IR sensors initial value
  read_ir_init();
}

void loop() {
  
  /* UNCOMMENT TO TEST VELOCITY CONTROL (NOT WHEELS SEPARATELY), REQUIRES ENCODERS*/
  
  //read ir and adjust weigthed averages
  read_ir_update();

  //run velocity control on motors
  velocity_control();

  myMotor1->setSpeed(abs(motor1_inputVel));
  if(motor1_targetVel == 0)
  {
    myMotor1->run(RELEASE);
  } else if (motor1_targetVel < 0) {
    myMotor1->run(BACKWARD);
  } else {
    myMotor1->run(FORWARD);
  }

  myMotor2->setSpeed(abs(motor2_inputVel));
  if(motor2_targetVel == 0)
  {
    myMotor2->run(RELEASE);
  } else if (motor1_targetVel < 0) {
    myMotor2->run(BACKWARD);
  } else {
    myMotor2->run(FORWARD);
  }
  /*----COMMENT END */

  //prints of IR data
  #ifdef DEBUG
  for(int i = 0; i < 5; i++)
  {
    Serial.print("Sensor: ");
    Serial.print(i);
    Serial.print(": ");
    Serial.println(movingAverages[i]);
  }
  #endif
  //if command available in terminal
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    #ifdef DEBUG
    Serial.print("echo: ");
    Serial.print(data);
    Serial.print(";");
    #endif

    String motorNumberStr = data.substring(0, 1);
    String motorSpeedStr = data.substring(1, 5);

    int motorNumber = motorNumberStr.toInt();
    int motorSpeed = motorSpeedStr.toInt();

    #ifdef DEBUG
    Serial.print("   you want to turn motor: ");
    Serial.print(motorNumber);
    Serial.print(" at speed ");
    Serial.print(motorSpeed);
    Serial.print("\n");
    #endif
    
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
        motor1_targetVel = motorSpeed;
        if (motorSpeed < 0) {
          myMotor1->run(BACKWARD);
        } else {
          myMotor1->run(FORWARD);
        }
      } else if (motorNumber == 2) {
        motor2_targetVel = motorSpeed;
        if (motorSpeed < 0) {
          myMotor2->run(BACKWARD);
        } else {
          myMotor2->run(FORWARD);
        }
      }
    }
  }

  send_update_packet();

  // delay(10);
}

// send an update packet to the host over serial
// packet format:
//   [encoder1],[encoder2];[sensor1],[sensor2],[sensor3],[sensor4],[sensor5],
void send_update_packet() 
{
  Serial.print(enc1_count);
  Serial.print(",");
  Serial.print(enc2_count);
  Serial.print(";");
  for (int i = 0; i < 5; i++) {
    Serial.print(movingAverages[i]);
    if (i < 4)
      Serial.print(",");
  }
}

//increment counter everytime an edge occurs on pin 2 (Enc1)
void isr_enc1_count()
{
  enc1_count++;
}


//increment counter everytime an edge occurs on pin 3 (Enc2)
void isr_enc2_count()
{
  enc2_count++;
}

void read_ir_init()
{
  int sensorValue;
  static const uint8_t analog_pins[] = {A0,A1,A2,A3,A4};
  for(int i = 0; i < 5; i++)
  {
    sensorValue = analogRead(analog_pins[i]);
    movingAverages[i] =(float) sensorValue * (5.0 / 1023.0);
  }
}

void read_ir_update()
{
  int sensorValue;
  float new_voltage;
  static const uint8_t analog_pins[] = {A0,A1,A2,A3,A4};
  for(int i = 0; i < 5; i++)
  {
    sensorValue = analogRead(analog_pins[i]);
    new_voltage = sensorValue * (5.0 / 1023.0);
    // update the moving average
    // defaulting to a = .5
    movingAverages[i] = (1 - .5) * movingAverages[i] + .5 * new_voltage;
  }
}

//run both wheels forward
void straight(int vel)
{
  motor1_targetVel = vel;
  motor2_targetVel = vel;
}

//run left wheel backwards and right wheel forward
void turn_left(int vel)
{
  motor1_targetVel = -vel;
  motor2_targetVel = vel;
}

//run right wheel backwards and left wheel forward
void turn_right(int vel)
{
  motor1_targetVel = vel;
  motor2_targetVel = -vel;
}

void velocity_control()
{
  unsigned int motor1_ticks = enc1_count;
  unsigned int motor2_ticks = enc2_count;

  enc1_count = 0;
  enc2_count = 0;
  unsigned int rpm_convert = 1;
  float motor1_calcVel = (float) motor1_ticks / rpm_convert; //10ms ideally passes
  float motor2_calcVel = (float) motor2_ticks / rpm_convert; //10ms ideally passes, will need to  tune
  //Motor 1
  //if greater than target velocity, decrease input to the motor, else if less than target velocity, increase input to the motor
  if((motor1_calcVel > motor1_targetVel) | motor1_inputVel > 0)
  {
    motor1_inputVel --;
  } else if((motor1_ticks/rpm_convert < motor1_targetVel) | motor1_inputVel < 256)
  {
    motor1_inputVel ++;
  }

  //Motor 2
  //if greater than target velocity, decrease input to the motor, else if less than target velocity, increase input to the motor
  if((motor2_calcVel > motor2_targetVel) | motor2_inputVel > 0)
  {
    motor2_inputVel --;
  } else if((motor2_ticks/rpm_convert < motor2_targetVel) | motor2_inputVel < 256)
  {
    motor2_inputVel ++;
  }
}
