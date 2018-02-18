



void strafe(int pwmValue){
  Motor1(pwmValue);
  Motor2(pwmValue);
  Motor3((int)(-0.5*pwmValue));
}


void climb(int pwmValue){
  Motor1(pwmValue);
  Motor2(-pwmValue);
  Motor3(0)
}
