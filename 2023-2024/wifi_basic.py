# SPDX-FileCopyrightText: 2022 Liz Clark for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import os
import ipaddress
import wifi
import time
import socketpool
import microcontroller

print()
print("Connecting to WiFi")

#  connect to your SSID
wifi.radio.connect("The Province", "8884pavlov")
#wifi.radio.stop_station()
time.sleep(5)
#wifi.radio.start_ap(ssid='TEST', password='ABCDEFGH')

print("Connected to WiFi")

pool = socketpool.SocketPool(wifi.radio)

#  prints MAC address to REPL
print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])

#  prints IP address to REPL
print("My IP address is", wifi.radio.ipv4_address)

#  pings Google
#ipv4 = ipaddress.ip_address("8.8.4.4")
#print("Ping google.com: %f ms" % (wifi.radio.ping(ipv4)*1000))
