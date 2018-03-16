
#include <Wire.h>
#include "I2Cdev.h"
#include "MPU6050.h"


MPU6050 accelgyro;


int16_t ax, ay, az;
int16_t gx, gy, gz;


void updateSensors()
{
  accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
}


double getGyroRate()
{
  return ((double)gz / 131.064);
}

