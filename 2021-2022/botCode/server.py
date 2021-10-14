#!/usr/bin/env python3
import sys

import robomodules
import os
from messages import MsgType

ADDRESS = os.environ.get("LOCAL_ADDRESS","localhost")
if len(sys.argv) == 1:
    PORT = os.environ.get("BIND_PORT", 11295)
else:
    PORT = os.environ.get("BIND_PORT", int(sys.argv[2]))

def main():
    server = robomodules.Server(ADDRESS, PORT, MsgType)
    server.run()

if __name__ == "__main__":
    main()
