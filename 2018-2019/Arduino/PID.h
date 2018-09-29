/**
 * PID.h
 * Ethan Yaccrino-Mims
 * PID controllers for MDRC pacbot
 */



//constants for the min and max sum of all prior errors
#define MIN_INTEGRATED_ERROR -50
#define MAX_INTEGRATED_ERROR 50

//distance out of bounds indicator
#define DISTANCE_OUT_OF_BOUNDS -1

//max distance sensor value
#define MAX_DISTANCE 500

//min distance sensor value
#define MIN_DISTANCE 120

//lane keeping constants
double LP = 3;
double LI = 1;
double LD = 0.5;

//heading hold constants
double HP = 5;
double HI = 0;
double HD = 0.5;

//the error on the last function call
double lastLaneError = 0;
double lastHeadingError = 0;

//the constraned sum of all prior errors
double integratedLaneError = 0;
double integratedHeadingError = 0;


//initializes working values to zero
void InitPID(void)
{
	lastLaneError = 0;
	lastHeadingError = 0;
	integratedLaneError = 0;
	integratedHeadingError = 0;  
}


/**
 * PID control structure for lane keeping
 *
 * @param left the distance to the left wall scaled by some constant k
 * @param right the distance to the right wall scaled by some constant k
 * @return the output of the laneKeep PID controller
 */
int laneKeepPID(double left, double right)
{
	double error = right - left;
	double out;

	out = LP * error;
	integratedLaneError += LI * error;
	integratedLaneError = constrain(integratedLaneError, MIN_INTEGRATED_ERROR,
		MAX_INTEGRATED_ERROR);
	out += integratedLaneError;
	out += LD * (error - lastLaneError);
	lastLaneError = error;

	return ((int)constrain(out, -255, 255));
}


/**
 * PID control structure for the heading
 *
 * @param current the current 
 * @return the output of the heading PID controller
 */
int headingPID(double current, double target)
{

	double error = target - current;
	double out;

	out = HP * error;
	integratedHeadingError += HI * error;
	integratedHeadingError = constrain(integratedHeadingError, MIN_INTEGRATED_ERROR,
		MAX_INTEGRATED_ERROR);
	out += integratedHeadingError;
	out += HD * (error - lastHeadingError);
	lastHeadingError = error;

	return ((int)constrain(out, -255, 255));
}



/**
 * 
 * 
 * 
 * 
 */
 int FilterSensor(int value)
 {
  if((MIN_DISTANCE < value && value < MAX_DISTANCE))
  {
    return value;
  }
  
  return DISTANCE_OUT_OF_BOUNDS;
 }
















 
