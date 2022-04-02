from argparse import ArgumentParser

import websockets

# get command-line arguments
parser = ArgumentParser()
parser.add_argument('ip', help='The ip to use', default='ws://mdrcpi4.student.rit.edu:8765')
args = parser.parse_args()

ip = args.ip

print("forward, backward, left, or right")

with websockets.connect(ip) as websocket:
    while True:
        direction = input()
        if direction == "forward":
            websocket.send("forward")
        elif direction == "backward":
            websocket.send("backward")
        elif direction == "left":
            websocket.send("left")
        elif direction == "right":
            websocket.send("right")
        elif direction == "stop":
            websocket.send("stop")
        else:
            print("invalid input")