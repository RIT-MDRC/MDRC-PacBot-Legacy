import serial
import time

from definitions import *
from sensor import distance_to_voltage, voltage_to_distance

SENSOR_GRID_DISTANCE_FROM_CENTER = 0.3;
GRID_CELLS_PER_CM = 1/8.89;

class PacbotArduinoManager:

    latest_message = None

    waiting_for_msg = True
    
    encoder_ticks_to_grid_units = 0.004571428571

    def __init__(self, port='/dev/ttyUSB0', baud_rate=115200):
        self.port = port
        self.baud_rate = baud_rate
        self.arduino = serial.Serial(self.port, self.baud_rate, timeout=1)
        self.arduino.flush()
        self.arduino.readline()
        self.arduino.readline()
        self.arduino.readline()

    def write_motors(self, left: int, right: int):
        if self.waiting_for_msg:
            return
        self.waiting_for_msg = True
        print('motors: ', left, right)
        self.write(OutgoingArduinoMessage('1', int(left / 5 * 100)).format())
        self.write(OutgoingArduinoMessage('2', int(right / 5 * 100)).format())

    def write(self, data: str):
        print('SEND', data)
        self.arduino.write(data.encode())

    def get_sensor_data(self) -> IncomingArduinoMessage:
        enc1_delta = 0
        enc2_delta = 0
        new_message = None
        while self.arduino.in_waiting > 0:
            line = self.arduino.readline().decode('utf-8')
            print('RECEIVED', self.arduino.in_waiting)
            self.waiting_for_msg = False
            #print(self.baud_rate)
            #print('line: ')
            #print(repr(line))
            #print('after line')
            self.latest_message = str_to_incoming_message(line)
            new_message = self.latest_message
            enc1_delta += self.latest_message.encoder_values[0]
            enc2_delta += self.latest_message.encoder_values[1]
        if new_message is not None:
            self.latest_message.ir_sensor_values = tuple(
                    voltage_to_distance(value) * GRID_CELLS_PER_CM for value in self.latest_message.ir_sensor_values
                )
            print(self.latest_message.ir_sensor_values)
            self.latest_message.encoder_values = (
                enc1_delta * self.encoder_ticks_to_grid_units,
                enc2_delta * self.encoder_ticks_to_grid_units
            )
        if self.latest_message is None:
            self.latest_message = str_to_incoming_message("0,0;2,2,2,2,2")
        return self.latest_message

    def close(self):
        self.arduino.close()
