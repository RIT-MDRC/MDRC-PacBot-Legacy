import serial
import time

import asyncio
import websockets

useSerial = False
serialPort = "/dev/ttyACM0"
serialBaud = 9600


def motorMove(direction):
    if direction == "forward":
        serialPort.write(b'0155\n1155\n')
    elif direction == "backward":
        serialPort.write(b'0-155\n1-155\n')
    elif direction == "left":
        serialPort.write(b'0155\n0-155\n')
        time.sleep(0.5)
        serialPort.write(b'0155\n1155\n')
    elif direction == "right":
        serialPort.write(b'0-155\n0155\n')
        time.sleep(0.5)
        serialPort.write(b'0155\n1155\n')
    elif direction == "stop":
        serialPort.write(b'0000\n0000\n')


serialPort = serial.Serial(serialPort, serialBaud, timeout=1)


async def hello(websocket, path):
    direction = await websocket.recv()
    print(f"< {direction}")
    motorMove(direction)

    greeting = "You said {}!".format(direction)
    await websocket.send(greeting)

start_server = websockets.serve(hello, port=8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()