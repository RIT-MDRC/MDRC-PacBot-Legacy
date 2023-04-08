import serial
import time

from definitions import *


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
        return self.latest_message

    def close(self):
        self.arduino.close()