import wifi
import socketpool
import ipaddress
import time
#from secrets import secrets


# edit host and port to match server
HOST = "192.168.4.17"
PORT = 5000
TIMEOUT = 5
INTERVAL = 5
MAXBUF = 6


print("Connecting to wifi")
wifi.radio.connect("TEST", "ABCDEFGH")
pool = socketpool.SocketPool(wifi.radio)

print("Self IP", wifi.radio.ipv4_address)
server_ipv4 = ipaddress.ip_address(pool.getaddrinfo(HOST, PORT)[0][4][0])
print("Server ping", server_ipv4, wifi.radio.ping(server_ipv4), "ms")

buf = bytearray(MAXBUF)
#while True:
#print("Create TCP Client Socket")
#s = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
#s.settimeout(TIMEOUT)

#print("Connecting")
#s.connect((HOST, PORT))

#size = s.send(b'Hello, world')
#print("Sent", size, "bytes")

#size = s.recv_into(buf)
#print('Received', size, "bytes", buf[:size])

print("Create UDP Client socket")
s = pool.socket(pool.AF_INET, pool.SOCK_DGRAM)
s.settimeout(TIMEOUT)

size = s.sendto(b"Hello, world", (HOST, PORT))
print("Sent", size, "bytes")

size, addr = s.recvfrom_into(buf)
print("Received", buf[:size], size, "bytes from", addr)

while True:
    size = s.sendto(b"Hello, world", (HOST, PORT))
    size, addr = s.recvfrom_into(buf)
#size = s.sendto(b"Hello, world", (HOST, PORT))
#size, addr = s.recvfrom_into(buf)
#size = s.sendto(b"Hello, world", (HOST, PORT))
#size, addr = s.recvfrom_into(buf)
#while True:
#    s.send(b'000000')
#    size = s.recv_into(buf)
#    s.send(b'000000')
#    size = s.recv_into(buf)
#    s.send(b'000000')
#    size = s.recv_into(buf)

s.close()

time.sleep(INTERVAL)
