import serial
import time

from definitions import *
from sensor import distance_to_voltage, voltage_to_distance

SENSOR_GRID_DISTANCE_FROM_SENSOR = 0.3;
GRID_CELLS_PER_CM = 1/8.89;

class PacbotArduinoManager:

    latest_message = None
    
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
        print('motors: ', left, right)
        self.write(OutgoingArduinoMessage('1', left / 5 * 100).format())
        self.write(OutgoingArduinoMessage('2', right / 5 * 100).format())

    def write(self, data: str):
        self.arduino.write(data.encode())

    def get_sensor_data(self) -> IncomingArduinoMessage:
        enc1_delta = 0
        enc2_delta = 0
        while self.arduino.in_waiting > 0:
            line = self.arduino.readline().decode('utf-8')
            #print(self.baud_rate)
            #print('line: ')
            #print(repr(line))
            #print('after line')
            self.latest_message = str_to_incoming_message(line)
            enc1_delta += self.latest_message.encoder_values[0]
            enc2_delta += self.latest_message.encoder_values[1]
            
        self.latest_message.ir_sensor_values = (
            voltage_to_distance(self.latest_message.ir_sensor_values[0] * GRID_CELLS_PER_CM - SENSOR_GRID_DISTANCE_FROM_SENSOR),
            voltage_to_distance(self.latest_message.ir_sensor_values[1] * GRID_CELLS_PER_CM - SENSOR_GRID_DISTANCE_FROM_SENSOR),
            voltage_to_distance(self.latest_message.ir_sensor_values[2] * GRID_CELLS_PER_CM - SENSOR_GRID_DISTANCE_FROM_SENSOR),
            voltage_to_distance(self.latest_message.ir_sensor_values[3] * GRID_CELLS_PER_CM - SENSOR_GRID_DISTANCE_FROM_SENSOR),
            voltage_to_distance(self.latest_message.ir_sensor_values[4 * GRID_CELLS_PER_CM - SENSOR_GRID_DISTANCE_FROM_SENSOR])
        )
        print(self.latest_message.ir_sensor_values)
        self.latest_message.encoder_values = (
            enc1_delta * self.encoder_ticks_to_grid_units,
            enc2_delta * self.encoder_ticks_to_grid_units
        )
        return self.latest_message

    def close(self):
        self.arduino.close()
