import wifi
import socketpool
import ipaddress
import time
import board
import digitalio

led = digitalio.DigitalInOut(board.GP18)
led.direction = digitalio.Direction.OUTPUT
# from secrets import secrets


# edit host and port to match server
HOST = "129.21.83.96"
PORT = 20001
TIMEOUT = 10000
INTERVAL = 5
MAXBUF = 6

print("Connecting to wifi")
wifi.radio.connect("RIT-WiFi", "")
pool = socketpool.SocketPool(wifi.radio)

print("Self IP", wifi.radio.ipv4_address)
HOST = str(wifi.radio.ipv4_address)
server_ipv4 = ipaddress.ip_address(pool.getaddrinfo(HOST, PORT)[0][4][0])
print("Server ping", server_ipv4, wifi.radio.ping(server_ipv4), "ms")

buf = bytearray(MAXBUF)

print("Create UDP Client socket")
s = pool.socket(pool.AF_INET, pool.SOCK_DGRAM)
# s.settimeout(TIMEOUT)
s.bind((HOST, PORT))

while True:
    print("check")
    size, addr = s.recvfrom_into(buf)
    print("received")
    temp = buf.decode("utf-8")
    temp = temp.rstrip("\x00")
    print(repr(temp))
    print(len(temp))
    print(buf)
    if temp == "y":
        print("yes")
        led.value = True
    elif temp == "n":
        print("no")
        led.value = False
    elif temp == "c":
        if led.value:
            print("check light on")
            s.sendto(b"light on", addr)
        else:
            print("check check light off")
            s.sendto(b"light off", addr)

s.close()

time.sleep(INTERVAL)
