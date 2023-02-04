'''
simple PID controller class
'''
import math

class PID_controller:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.integral = 0
        self.previous_error = 0

    def update(self, error, dt):
        self.integral += error * dt
        derivative = (error - self.previous_error) / dt
        self.previous_error = error
        return self.Kp * error + self.Ki * self.integral + self.Kd * derivative

    def reset(self):
        self.integral = 0
        self.previous_error = 0
        
    def set_Kp(self, Kp):
        self.Kp = Kp

    def set_Ki(self, Ki):
        self.Ki = Ki
        
    def set_Kd(self, Kd):
        self.Kd = Kd