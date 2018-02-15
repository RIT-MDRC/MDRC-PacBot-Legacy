
#define MIN_INTEGRATED_ERROR = -50;
#define MAX_INTEGRATED_ERROR = 50;

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


int updatePID(double left, double right)
{
   
}












