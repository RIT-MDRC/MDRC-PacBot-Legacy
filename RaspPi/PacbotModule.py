"""
PacbotModule.py
holds all functionality relevant to the game rule's
Ethan Yaccarino-Mims
"""

import os
import robomodules
from messages import MsgType
from grid import grid


ADDRESS = os.environ.get("LOCAL_ADDRESS","localhost")
PORT = os.environ.get("LOCAL_PORT", 11295)


def FREQUENCY():
    return 10


class PacbotModule(robomodules.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = list().append(MsgType.PACMAN_COMMAND)








