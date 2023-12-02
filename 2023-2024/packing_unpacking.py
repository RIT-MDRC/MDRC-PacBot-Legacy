import os
import ipaddress
import wifi
import time
import socketpool
import microcontroller
import struct

print("check")


def packing(ack, battery, accel, distance, encoders):
    if len(distance) != 8 or len(encoders) != 3:
        print("bad length for packing")
    # define the format string for struct.pack
    format_str = 'Hhh' + 'H' * 8 + 'h' * 3
    # create a tuple containing all the values to pack
    values = (ack, battery, accel) + tuple(distance) + tuple(encoders)
    # pack the data
    packed_data = struct.pack(format_str, *values)
    return packed_data


numbers = [1, 100, 100, 100]
while True:
    message_type = numbers[0]

    if message_type == 1:
        # motors
        if len(numbers) != 7:
            print("numbers is not 7")
        motor1 = struct.unpack("h", numbers[1:3])
        motor2 = struct.unpack("h", numbers[3:5])
        motor3 = struct.unpack("h", numbers[5:7])
        print("motor command recieved", motor1, motor2, motor3)
    elif message_type == 2:
        if len(numbers) != 3:
            print("numbers is not 3")
        ack = struct.unpack("H", numbers[1:3])
        sleep = struct.unpack("B", numbers[3])
        print("ack and sleep:", ack, sleep)
    elif message_type == 3:
        if len(numbers) != 5:
            print("numbers is not 5")
        ack = struct.unpack("H", numbers[1:3])
        accel_offset = struct.unpack("h", numbers[3:5])
        print("ack and accel_offset:", ack, accel_offset)
    elif message_type == 4:
        if len(numbers) != 7:
            print("numbers is not 7")
        ack = struct.unpack("H", numbers[1:3])
        sensor = struct.unpack("B", numbers[3:4])
        offset = struct.unpack("h", numbers[4:6])
        print("ack and sensor and offset:", ack, sensor, offset)
    else:
        print("bad message")
        print("message_type:", message_type)

