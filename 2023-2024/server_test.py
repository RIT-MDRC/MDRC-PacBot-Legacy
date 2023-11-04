from time import monotonic
import board
import microcontroller
import socketpool
import os
import wifi
import digitalio
from adafruit_httpserver import Server, Request, Response, Websocket, GET
import time
import microcontroller
#  connect to your SSID
try:
    wifi.radio.connect("TEST", "ABCDEFGH")
    print("connected!")
except:
    print('error connecting')
    time.sleep(10)
    microcontroller.reset()
#wifi.radio.stop_station()
#wifi.radio.start_ap(ssid='TEST', password='ABCDEFGH')

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, debug=True)

websocket: Websocket = None
next_message_time = monotonic()

HTML_TEMPLATE = """

<html lang="en">
    <head>
        <title>Websocket Client</title>
    </head>
    <body>
        <script>;
            const colorPicker = document.querySelector('input[type="color"]');
            let ws = new WebSocket('ws://' + location.host + '/connect-websocket');
            ws.onopen = () => console.log('WebSocket connection opened');
            ws.onclose = () => console.log('WebSocket connection closed');
            colorPicker.oninput = debounce(() => ws.send(colorPicker.value), 200);
            function debounce(callback, delay = 1000) {
                let timeout
                return (...args) => {
                    clearTimeout(timeout)
                    timeout = setTimeout(() => {
                    callback(...args)
                  }, delay)
                }
            }
        </script>
    </body>
</html>

"""

@server.route("/client", GET)
def client(request: Request):
    print("check")
    return Response(request, '{"code": "ok"}', content_type="json")

@server.route("/connect-websocket", GET)
def connect_client(request: Request):
    global websocket  # pylint: disable=global-statement
    if websocket is not None:
        websocket.close()  # Close any existing connection
    websocket = Websocket(request)
    return websocket

print(wifi.radio.ipv4_address)
server.start(str(wifi.radio.ipv4_address))
led = digitalio.DigitalInOut(board.GP18)
led.direction = digitalio.Direction.OUTPUT
while True:
    #print("poll" + str(monotonic()))
    server.poll()
    # Check for incoming messages from client
    if websocket is not None:
        while True:
            #print(monotonic())
            if (data := websocket.receive(False)) is not None:
                print("-------")
                websocket.send_message("hello\n")
    # Send a message every second
    #if websocket is not None and next_message_time < monotonic():
    #    websocket.send_message(str(led.value))
    #    next_message_time = monotonic() + 1
