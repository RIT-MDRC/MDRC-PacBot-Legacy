from argparse import ArgumentParser

import serial
import time

import asyncio
import websockets

# get command-line arguments
parser = ArgumentParser()
parser.add_argument('serialPort', help='The serial port to use', default='/dev/ttyACM0')
args = parser.parse_args()

useSerial = False
serialPort = args.serialPort
serialBaud = 9600


def motorMove(direction):
    if direction == "forward":
        serialPort.write(b'1155\n2155\n')
        print(serialPort.readline())
        print(serialPort.readline())
    elif direction == "backward":
        serialPort.write(b'1-155\n2-155\n')
        print(serialPort.readline())
        print(serialPort.readline())
    elif direction == "left":
        serialPort.write(b'1-155\n2155\n')
        print(serialPort.readline())
        print(serialPort.readline())
        time.sleep(0.5)
        serialPort.write(b'1155\n2155\n')
        print(serialPort.readline())
        print(serialPort.readline())
    elif direction == "right":
        serialPort.write(b'1155\n2-155\n')
        print(serialPort.readline())
        print(serialPort.readline())
        time.sleep(0.5)
        serialPort.write(b'1155\n2155\n')
        print(serialPort.readline())
        print(serialPort.readline())
    elif direction == "stop":
        serialPort.write(b'1000\n2000\n')
        print(serialPort.readline())
        print(serialPort.readline())


serialPort = serial.Serial(serialPort, serialBaud, timeout=1)


async def hello(websocket, path):
    while True:
        direction = await websocket.recv()
        print(f"< {direction}")
        motorMove(direction)

        greeting = "You said {}!".format(direction)
        await websocket.send(greeting)

start_server = websockets.serve(hello, port=8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
