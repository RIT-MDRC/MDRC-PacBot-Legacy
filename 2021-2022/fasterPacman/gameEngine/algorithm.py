import asyncio
import os
import time

from gameEngine import GameEngine
import threading

ADDRESS = "localhost"
PORT = os.environ.get("BIND_PORT", 11297)

exitFlag = 0

WEIGHT_SET = {
    'FEAR': 10,
    'PELLET_WEIGHT': .65,
    'SUPER_PELLET_WEIGHT': .1,
    'GHOST_WEIGHT': .35,
    'FRIGHTENED_GHOST_WEIGHT': .105
}


class MyThread(threading.Thread):
    def __init__(self, threadID, name, scores, counter, print_stuff=False):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.scores = scores
        self.counter = counter
        self.print_stuff = print_stuff

    def run(self):
        if self.print_stuff:
            print("Starting " + self.name)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        game = GameEngine(ADDRESS, PORT, weight_set=WEIGHT_SET)
        game.run()
        if self.print_stuff:
            print(game.final_state)
        self.scores[self.counter] = game.final_state
        if self.print_stuff:
            print("Exiting " + self.name)
        return game.final_state


def main():
    start = time.time()

    threads = []
    scores = []
    numThreads = 1000
    notifyInterval = 10

    # Create new threads
    for i in range(1, numThreads+1):
        scores.append(None)
        threads.append(MyThread(i, "Thread-" + str(i), scores, i-1, False))

    # Start new Threads
    for i in range(numThreads):
        threads[i].start()
        if (i-1) % notifyInterval == 0:
            print('Starting thread ' + str(i-1) + '...')

    # Join new Threads
    for i in range(numThreads):
        threads[i].join()

    end = time.time()

    print('done in ' + str(end - start) + ' s')

    sum = 0
    for i in range(numThreads):
        sum += scores[i]['score']
        # print(str(scores[i]))
    print('average score: ' + str(sum/numThreads))


if __name__ == "__main__":
    main()
