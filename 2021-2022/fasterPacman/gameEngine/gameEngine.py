#!/usr/bin/env python3
import asyncio
import os, sys, logging
# import robomodules as rm
import time

import pygame

USING_VISUALIZER = False
NO_PRINT = True
RUN_ON_CLOCK = True

from messages import *
from pacbot.variables import game_frequency, ticks_per_update
from pacbot import StateConverter, GameState
from botCode.highLevelPacman import HighLevelPacman
from visualize import Visualize

ADDRESS = "localhost"
PORT = os.environ.get("BIND_PORT", 11297)

FREQUENCY_MULTIPLIER = 1
FREQUENCY = game_frequency * ticks_per_update * FREQUENCY_MULTIPLIER

WEIGHT_SET = {
    'FEAR': 10,
    'PELLET_WEIGHT': .65,
    'SUPER_PELLET_WEIGHT': .1,
    'GHOST_WEIGHT': .35,
    'FRIGHTENED_GHOST_WEIGHT': .105,
    'PROXIMITY_PELLET_MULTIPLIER': .1,
    'ANTI_CORNER_WEIGHT': .1
}
# WEIGHT_SET = dict(zip(WEIGHT_SET.keys(), [14.999761323524108, 0.6194892162712323, 0.011251072977281056, 0.40740361802529795, 0.6250905337589961]))
WEIGHT_SET = {'FEAR': 3.2543280421284333, 'PELLET_WEIGHT': 2.3070606203090285, 'SUPER_PELLET_WEIGHT': 13.27715231981747, 'GHOST_WEIGHT': 13.22475001399991, 'FRIGHTENED_GHOST_WEIGHT': 14.99999999830702, 'PROXIMITY_PELLET_MULTIPLIER': 11.57810588870234, 'ANTI_CORNER_WEIGHT': -14.968433445107918}

class GameEngine:
    def __init__(self, addr, port, weight_set=WEIGHT_SET, run_on_clock=None, using_visualizer=None):
        global WEIGHT_SET, USING_VISUALIZER, RUN_ON_CLOCK
        if run_on_clock is not None:
            RUN_ON_CLOCK = run_on_clock
        if using_visualizer is not None:
            USING_VISUALIZER = using_visualizer
        WEIGHT_SET = weight_set
        self.final_state = None
        self.latestPacbotInfo = None
        self.subscriptions = [MsgType.PACMAN_LOCATION]
        # super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        # self.loop.add_reader(sys.stdin, self.keypress)

        self.game = GameState()
        self.highLevelPacman = HighLevelPacman(addr=None, port=None, game=self, returnInfo=NO_PRINT,
                                               frequency_multiplier=FREQUENCY_MULTIPLIER, fear=WEIGHT_SET['FEAR'],
                                               pellet_weight=WEIGHT_SET['PELLET_WEIGHT'],
                                               super_pellet_weight=WEIGHT_SET['SUPER_PELLET_WEIGHT'],
                                               ghost_weight=WEIGHT_SET['GHOST_WEIGHT'],
                                               frightened_ghost_weight=WEIGHT_SET['FRIGHTENED_GHOST_WEIGHT'],
                                               proximity_pellet_multiplier=WEIGHT_SET['PROXIMITY_PELLET_MULTIPLIER'],
                                               anti_corner_weight=WEIGHT_SET['ANTI_CORNER_WEIGHT'],
                                               runOnClock=RUN_ON_CLOCK)
        if USING_VISUALIZER:
            self.visualize = Visualize(run_on_clock=run_on_clock)

        self.game.unpause()

        if RUN_ON_CLOCK:
            self.loop = asyncio.get_event_loop()
            self.loop.call_soon(self.tick)
        else:
            while self.game.play:
                # INCORRECT CALL TIMING, PACBOT MOVES WAY TOO FAST
                # update_pacbot_pos
                self.highLevelPacman.tick()
                # This will become asynchronous
                for i in range(8):
                    self.game.next_step()
                    if USING_VISUALIZER:
                        self.visualize.visualizer.msg_received(StateConverter.convert_game_state_to_full(self.game),
                                                               MsgType.FULL_STATE)
                self.highLevelPacman.msg_received(StateConverter.convert_game_state_to_light(self.game),
                                                  MsgType.LIGHT_STATE)
                # print('gameEngineTickMesg')
                # print('SAVE GAME STATE TO FILE')
                if USING_VISUALIZER:
                    pygame.time.wait(50)
        self.final_state = {'score':self.game.score}

    def _write_state(self):
        full_state = StateConverter.convert_game_state_to_full(self.game)
        self.write(full_state.SerializeToString(), MsgType.FULL_STATE)

        light_state = StateConverter.convert_game_state_to_light(self.game)
        self.write(light_state.SerializeToString(), MsgType.LIGHT_STATE)

    def msg_received(self, msg, msg_type):
        if msg_type == MsgType.PACMAN_LOCATION:
            self.game.pacbot.update((msg.x, msg.y))

    def tick(self):
        # print('GameEngine.tick()')
        # schedule the next tick in the event loop
        self.loop.call_later(1.0 / FREQUENCY, self.tick)

        # this function will get called in a loop with FREQUENCY frequency
        if self.game.play:
            # update_pacbot_pos
            # This will become asynchronous
            self.game.next_step()
            self.highLevelPacman.msg_received(StateConverter.convert_game_state_to_light(self.game), MsgType.LIGHT_STATE)
            # print('gameEngineTickMesg')
            if USING_VISUALIZER:
                self.visualize.visualizer.msg_received(StateConverter.convert_game_state_to_full(self.game), MsgType.FULL_STATE)
        # self._write_state()

    def run(self):
        if RUN_ON_CLOCK:
            self.loop.run_forever()

    def keypress(self):
        char = sys.stdin.read(1)
        # For some reason I couldn't quite get this to do what I wanted
        # Still it's a bit cleaner than otherwise
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")
        sys.stdout.flush()
        if char == "r":
            logging.info("Restarting...")
            self.game.restart()
            self._write_state()
        elif char == "p":
            if (self.game.play):
                logging.info('Game is paused')
                self.game.pause()
            else:
                logging.info('Game resumed')
                self.game.unpause()
        elif char == "q":
            logging.info("Quitting...")
            self.quit() 

    def receivePacbotInfo(self, pacbotInfo):
        # print('received info')
        # print(pacbotInfo)
        if not self.game.play:
            # print('I think we should stop the thing')
            self.highLevelPacman.quit()
            if USING_VISUALIZER:
                print('quitting pygame')
                pygame.quit()
                # self.visualize.visualizer.quit()
            self.loop.stop()
            self.final_state = {'score':self.game.score}

def main():
    global USING_VISUALIZER, NO_PRINT, RUN_ON_CLOCK
    # logger automatically adds timestamps
    # I wanted it to print each sequentially but it did not want to
    USING_VISUALIZER = '--vis' in sys.argv
    NO_PRINT = '--print' not in sys.argv
    RUN_ON_CLOCK = '--clock' in sys.argv

    logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s',
                        datefmt="%I:%M:%S %p")
    engine = GameEngine(ADDRESS, PORT)
    if not NO_PRINT:
        print('Game is paused.')
        print('Controls:')
        print('    r - restart')
        print('    p - (un)pause')
        print('    q - quit')

    if RUN_ON_CLOCK:
        engine.run()
    else:
        print(engine.game.score)


if __name__ == "__main__":
    main()
