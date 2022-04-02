import asyncio
from argparse import ArgumentParser

import websockets

# get command-line arguments
parser = ArgumentParser()
parser.add_argument('ip', help='The ip to use', default='ws://mdrcpi4.student.rit.edu:8765')
args = parser.parse_args()

ip = args.ip

print("forward, backward, left, right, stop, or quit")

async def main():

    websocket = await websockets.connect(ip)

    while True:
        direction = input()
        if direction == "forward" or direction == "f":
            await websocket.send("forward")
            print(await websocket.recv())
        elif direction == "backward" or direction == "b":
            await websocket.send("backward")
            print(await websocket.recv())
        elif direction == "left" or direction == "l":
            await websocket.send("left")
            print(await websocket.recv())
        elif direction == "right" or direction == "r":
            await websocket.send("right")
            print(await websocket.recv())
        elif direction == "stop" or direction == "s":
            await websocket.send("stop")
            print(await websocket.recv())
        elif direction == "quit" or direction == "q":
            break
        else:
            print("invalid input")

    await websocket.close()

asyncio.run(main())