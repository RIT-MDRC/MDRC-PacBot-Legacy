
import websockets

ip = "ws://mdrcpi4.student.rit.edu:8765"

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