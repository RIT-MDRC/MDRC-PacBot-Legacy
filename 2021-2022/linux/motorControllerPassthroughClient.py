import asyncio
from argparse import ArgumentParser

import websockets

# get command-line arguments
parser = ArgumentParser()
parser.add_argument('ip', help='The ip to use', default='ws://mdrcpi4.student.rit.edu:8765')
args = parser.parse_args()

ip = args.ip

print("forward, backward, left, right, or stop")

async def main():

    websocket = await websockets.connect(ip)

    while True:
        direction = input()
        if direction == "forward":
            await websocket.send("forward")
            print(await websocket.recv())
        elif direction == "backward":
            await websocket.send("backward")
            print(await websocket.recv())
        elif direction == "left":
            await websocket.send("left")
            print(await websocket.recv())
        elif direction == "right":
            await websocket.send("right")
            print(await websocket.recv())
        elif direction == "stop":
            await websocket.send("stop")
            print(await websocket.recv())
        else:
            print("invalid input")

asyncio.run(main())