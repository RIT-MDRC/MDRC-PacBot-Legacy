import asyncio
import os
import time
import dlib
import math
import select
import termios

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
    def __init__(self, threadID, name, scores, counter, print_stuff=False, weight_set=WEIGHT_SET):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.scores = scores
        self.counter = counter
        self.print_stuff = print_stuff
        self.weight_set = weight_set

    def run(self):
        if self.print_stuff:
            print("Starting " + self.name)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        game = GameEngine(ADDRESS, PORT, weight_set=self.weight_set)
        game.run()
        if self.print_stuff:
            print(game.final_state)
        self.scores[self.counter] = game.final_state
        if self.print_stuff:
            print("Exiting " + self.name)
        return game.final_state


# ensure the Python version is 3.7+ so that dict keys are ordered
import sys
assert sys.version_info >= (3, 7)

def find_best_parameters():
    # set up the optimizer
    func_spec = dlib.function_spec(
        bound1=[lo for lo, hi, is_int in HYPERPARAM_RANGES.values()],
        bound2=[hi for lo, hi, is_int in HYPERPARAM_RANGES.values()],
        is_integer=[is_int for lo, hi, is_int in HYPERPARAM_RANGES.values()],
    )
    optimizer = dlib.global_function_search(
        functions=[func_spec],
        relative_noise_magnitude=0.001,
    )
    # if the optimizer expects that refining the current best solution won't result
    # in an improvement of at least this amount, then it will explore elsewhere
    optimizer.set_solver_epsilon(100) # in score units

    # main eval/solver loop
    best_score = -math.inf
    while True:
        next_eval_request = optimizer.get_next_x()
        print('Evaluating with parameters:')
        for name, value in zip(HYPERPARAM_RANGES.keys(), next_eval_request.x):
            print(f'  {name}: {value}')
        avg_score = test_hyperparams(*next_eval_request.x)
        next_eval_request.set(avg_score)

        if avg_score > best_score:
            best_score = avg_score
            print('New best score:', best_score)
            print(f'  Params: {list(next_eval_request.x)}')
            print()

        # check if stdin has input and stop if so
        if select.select([sys.stdin,],[],[],0.0)[0]:
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)  # flush stdin to prevent keypresses from going to the shell
            break
    best_hyperparams, best_score, func_idx = optimizer.get_best_function_eval()

    # print the best hyperparameters
    print()
    print('Best average score:', best_score)
    print('Parameters:')
    for name, value in zip(HYPERPARAM_RANGES.keys(), best_hyperparams):
        print(f'  {name}: {value}')
    print()

# hyperparam_name: (min_val, max_val, is_integer)
# names correspond to arguments of test_hyperparams
HYPERPARAM_RANGES = {
    'FEAR':                    (1, 15, False),
    'PELLET_WEIGHT':           (0.01, 1.0, False),
    'SUPER_PELLET_WEIGHT':     (0.01, 1.0, False),
    'GHOST_WEIGHT':            (0.01, 1.0, False),
    'FRIGHTENED_GHOST_WEIGHT': (0.01, 1.0, False),
}

def test_hyperparams(self, *args):
    """
    Evaluates the algorithm with the given hyperparameters. Returns the average score.
    """
    weight_set = dict(zip(HYPERPARAM_RANGES.keys(), args))

    start = time.time()

    threads = []
    scores = []
    numThreads = 1000
    notifyInterval = 10

    # Create new threads
    for i in range(1, numThreads+1):
        scores.append(None)
        threads.append(MyThread(i, "Thread-" + str(i), scores, i-1, False, weight_set=weight_set))

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
    avg_score = sum / numThreads
    print('average score: ' + str(avg_score))
    return avg_score


def main():
    find_best_parameters()


if __name__ == "__main__":
    main()
