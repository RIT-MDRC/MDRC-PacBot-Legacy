
#define MIN_INTEGRATED_ERROR -50
#define MAX_INTEGRATED_ERROR 50

double kp;
double ki;
double kd;

double lastError = 0;
double integratedError = 0;


void initPID(void)
{
	lastError = 0;
	integratedError = 0;  
}


int laneKeepPID(double left, double right)
{
	double error = right - left;
	double out;

	out = kp * error;
	integratedError += ki * error;
	integratedError = constrain(integratedError, MIN_INTEGRATED_ERROR,
		MAX_INTEGRATED_ERROR);
	out += integratedError;
	out += kd * (error - lastError);
	lastError = error;

	return ((int)constrain(out, -255, 255));
}


int headingPID(double current)
{

	double error = -current;
	double out;

	out = kp * error;
	integratedError += ki * error;
	integratedError = constrain(integratedError, MIN_INTEGRATED_ERROR,
		MAX_INTEGRATED_ERROR);
	out += integratedError;
	out += kd * (error - lastError);
	lastError = error;

	return ((int)constrain(out, -255, 255));
}












