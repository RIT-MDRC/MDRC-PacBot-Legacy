#ifndef _SENSOR_PAC
#define _SENSOR_PAC
class sensor{
    private:
        int GPIOREAD;
    public:
        void init_sensor(int GPIO);
        double sensor_read();
};
#endif