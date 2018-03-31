/**
 * sensors.h
 * Ethan Yaccarino-Mims
 * functions for getting all sensor values
 */
#include <Wire.h>
#include "I2Cdev.h"
#include "MPU6050.h"

//the gyro object
MPU6050 accelgyro;

//the output values from updating the sensors
int16_t ax, ay, az;
int16_t gx, gy, gz;


/**
 * initializes values and objects
 */
void initSensors()
{
	//start connection
	Wire.begin(); 

	//starts accelGyro object
	accelgyro.initialize(); 

	// sample rate to 8KHz/40
	accelgyro.setRate(8); 

}


/**
 * updates the sensor values
 */
void updateSensors()
{
  accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
}


/**
 * calculates the gyro's current rotational velocity on the z axis 
 * in degrees/second
 * 
 * @return the rate of rotating on the z axis in degrees/second
 */
double getGyroRate()
{
  return ((double)gz / 131.064);
}


/**
 * gets a measurement of the distance to the left wall
 */
//TODO



/**
 * gets a measurement of the distance to the right wall
 */
//TODO



/**
 * gets a measurement of the distance to the wall infront of the pacman
 */
//TODO

