import socket

localIP = "0.0.0.0"
localPort = 20001
bufferSize = 1024
address = "129.21.135.196"
msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

# Listen for incoming datagrams
# while (True):
#     bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
#     message = bytesAddressPair[0]
#     address = bytesAddressPair[1]
#     clientMsg = "Message from Client:{}".format(message)
#     clientIP = "Client IP Address:{}".format(address)
#     print(clientMsg)
#     print(clientIP)

    # Sending a reply to client
    #UDPServerSocket.sendto(bytesToSend, address)


while(True):
    response = input("enter:")
    if response == "y":
        UDPServerSocket.sendto(str.encode("y"), (address, 20001))
    elif response == "n":
        UDPServerSocket.sendto(str.encode("n"), (address, 20001))
    elif response == "c":
        UDPServerSocket.sendto(str.encode("c"), (address, 20001))
        UDPServerSocket.settimeout(5)
        try:
            bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
            message = bytesAddressPair[0]
            #address = bytesAddressPair[1]
            print(message)
        except:
            print("it failed :(")