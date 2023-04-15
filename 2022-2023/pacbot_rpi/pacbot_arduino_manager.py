import serial
import time

from definitions import *
from sensor import distance_to_voltage, voltage_to_distance


class PacbotArduinoManager:

    latest_message = None

    def __init__(self, port='/dev/ttyUSB0', baud_rate=9600):
        self.port = port
        self.baud_rate = baud_rate
        self.arduino = serial.Serial(self.port, self.baud_rate, timeout=1)
        self.arduino.flush()

    def write_motors(self, left: int, right: int):
        self.write(OutgoingArduinoMessage('1', left).format())
        self.write(OutgoingArduinoMessage('2', right).format())

    def write(self, data: str):
        self.arduino.write(data.encode())

    def get_sensor_data(self) -> IncomingArduinoMessage:
        while self.arduino.in_waiting > 0:
            self.latest_message = str_to_incoming_message(self.arduino.readline().decode('utf-8').rstrip())
        self.latest_message.ir_sensor_values = (
            voltage_to_distance(self.latest_message.ir_sensor_values[0]),
            voltage_to_distance(self.latest_message.ir_sensor_values[1]),
            voltage_to_distance(self.latest_message.ir_sensor_values[2]),
            voltage_to_distance(self.latest_message.ir_sensor_values[3]),
            voltage_to_distance(self.latest_message.ir_sensor_values[4])
        )
        self.latest_message.encoder_values = (
            # TODO
            self.latest_message.encoder_values[0] / 1000,
            self.latest_message.encoder_values[1] / 1000
        )
        return self.latest_message

    def close(self):
        self.arduino.close()