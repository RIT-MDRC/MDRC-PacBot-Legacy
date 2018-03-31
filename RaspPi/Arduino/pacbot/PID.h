/**
 *PID.h
 *Ethan Yaccrino-Mims
 *PID controllers for MDRC pacbot
 */



//constants for the min and max sum of all prior errors
#define MIN_INTEGRATED_ERROR -50
#define MAX_INTEGRATED_ERROR 50

//lane keeping constants
#define LP 3;
#define LI 1;
#define LD 0.5;

//heading hold constants
#define HP 5;
#define HI 0;
#define HD 0.5;

//the error on the last function call
double lastLaneError = 0;
double lastHeadingError = 0;

//the constraned sum of all prior errors
double integratedLaneError = 0;
double integratedHeadingError = 0;


//initializes working values to zero
void initPID(void)
{
	lastLaneError = 0
	lastHeadingError = 0;
	integratedLaneError
	integratedHeadingError = 0;  
}


/**
 *PID control structure for lane keeping
 *
 *@param left the distance to the left wall scaled by some constant k
 *@param right the distance to the right wall scaled by some constant k
 *@return the output of the PID controller
 */
int laneKeepPID(double left, double right)
{
	double error = right - left;
	double out;

	out = KP * error;
	integratedError += KI * error;
	integratedError = constrain(integratedError, MIN_INTEGRATED_ERROR,
		MAX_INTEGRATED_ERROR);
	out += integratedError;
	out += KD * (error - lastError);
	lastError = error;

	return ((int)constrain(out, -255, 255));
}


/**
 * PID control structure for the heading
 *
 *@param current the current 
 *
 *
 */
int headingPID(double current, double target)
{

	double error = target - current;
	double out;

	out = HP * error;
	integratedError += HI * error;
	integratedError = constrain(integratedError, MIN_INTEGRATED_ERROR,
		MAX_INTEGRATED_ERROR);
	out += integratedError;
	out += HD * (error - lastError);
	lastError = error;

	return ((int)constrain(out, -255, 255));
}












