import time
import serial, os

from definitions import *
from sensor import voltage_to_distance

SENSOR_GRID_DISTANCE_FROM_CENTER = 0.3
GRID_CELLS_PER_CM = 1 / 8.89


class PacbotArduinoManager:
    latest_message = None

    waiting_for_msg = True

    encoder_ticks_to_grid_units = 0.004571428571

    lines_read: list[IncomingArduinoMessage] = []
    lines_sent: list[OutgoingArduinoMessage] = []

    def __init__(self, port=os.environ.get('PI_SERIAL_PORT', '/dev/ttyUSB0'), baud_rate=115200):
        self.port = port
        self.baud_rate = baud_rate
        self.arduino = serial.Serial(self.port, self.baud_rate, timeout=1)
        self.arduino.flush()
        self.arduino.readline()
        self.arduino.readline()
        self.arduino.readline()

    def write_motors(self, left: int, right: int, forced: bool=False):
        if os.environ.get('DISABLE_MOTORS', 'f') == 't' or (self.waiting_for_msg and not forced):
            return
        self.waiting_for_msg = True
        #print('motors: ', left, right)

        motor_minimum_absolute_speed = 30
        motor_maximum_absolute_speed = 100

        # left and right are values between -1 and 1
        # modify them so that they fit the above constraints
        left_normalized = abs(left) * (
                motor_maximum_absolute_speed - motor_minimum_absolute_speed) + motor_minimum_absolute_speed
        left_normalized = min(255, 2 * left_normalized)
        if left < 0:
            left_normalized *= -1
        elif left == 0:
            left_normalized = 0
        right_normalized = abs(right) * (
                motor_maximum_absolute_speed - motor_minimum_absolute_speed) + motor_minimum_absolute_speed
        right_normalized = min(255, 2 * right_normalized)
        if right < 0:
            right_normalized *= -1
        elif right == 0:
            right_normalized = 0

        left_msg = OutgoingArduinoMessage('1', int(left_normalized))
        right_msg = OutgoingArduinoMessage('2', int(right_normalized))

        self.lines_sent.append(left_msg)
        self.lines_sent.append(right_msg)

        self.write(left_msg.format())
        self.write(right_msg.format())

        # when turning, only turn a little bit
        if right_normalized != 0 and left_normalized / right_normalized < 0:
            time.sleep(0.2)
            self.write_motors(0, 0, True)

    def write(self, data: str):
        #print('SEND', data)
        self.arduino.write(data.encode())

    def get_sensor_data(self) -> IncomingArduinoMessage:
        enc1_delta = 0
        enc2_delta = 0
        msg_received = False
        while self.arduino.in_waiting > 0:
            line = self.arduino.readline().decode('utf-8')

            msg = str_to_incoming_message(line)
            self.latest_message = msg
            self.waiting_for_msg = False
            msg_received = True
            self.lines_read.append(msg)

            enc1_delta += self.latest_message.encoder_values[0]
            enc2_delta += self.latest_message.encoder_values[1]
        if msg_received:
            self.latest_message.ir_sensor_values = tuple(
                voltage_to_distance(value) * GRID_CELLS_PER_CM for value in self.latest_message.ir_sensor_values
            )
            print(self.latest_message.ir_sensor_values)
            self.latest_message.encoder_values = (
                enc1_delta * self.encoder_ticks_to_grid_units,
                enc2_delta * self.encoder_ticks_to_grid_units
            )
        if self.latest_message is None:
            self.latest_message = str_to_incoming_message("0,0;0,0,0,0,0")
        return self.latest_message

    def get_debug_lines(self) -> tuple[list[IncomingArduinoMessage], list[OutgoingArduinoMessage]]:
        # clear lines_read and lines_sent and return them
        lines_read = self.lines_read
        lines_sent = self.lines_sent

        self.lines_read = []
        self.lines_sent = []

        return lines_read, lines_sent

    def close(self):
        self.arduino.close()
