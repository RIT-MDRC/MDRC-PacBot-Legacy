# @author Michael Elia
# @date 2023-04-06

import os
import robomodules as rm
import argparse as ap

from Pacbot.src.gameEngine.messages import *


class AutoRobo:
    """
    This class facilitates running and communication with the services provided by the HarvardURC_Pacbot repo.

    It uses robomodules, a custom library for communicating with the Harvard Robotics Club's server.
    """
    def __init__(self):
        pass


class AutoRobotClient(rm.ProtoModule):
    """
    This class acts as a client to the AutoRobo class.
    """
    pass


if __name__ == "__main__":
    # Parse arguments
    parser = ap.ArgumentParser()

    autoRobo = AutoRobo()
