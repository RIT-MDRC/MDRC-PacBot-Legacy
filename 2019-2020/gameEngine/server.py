#!/usr/bin/env python3

import robomodules
import os
from messages import MsgType

ADDRESS = "129.21.92.150"
PORT = os.environ.get("BIND_PORT", 11297)

def main():
    server = robomodules.Server(ADDRESS, PORT, MsgType)
    server.run()

if __name__ == "__main__":
    main()
