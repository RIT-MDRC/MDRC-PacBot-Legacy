#ifndef _MOTOR_PAC
#define _MOTOR_PAC
    #include "encoders.h"

    class Motor{
        private:
            int MOTORNUM;
            int GPIOPWM;
            int GPIOPHASE;
            encoder my_encoder;
        public:
            int init_encoder();

            int set_phase();

            int send_pwm();
    };

#endif