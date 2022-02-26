import asyncio
import os
import time
import dlib
import math
import select
# import termios
import numpy as np
from tqdm import tqdm

PRINT_ALL = False
USE_CLOCK = False
USING_VISUALIZER = False

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
    'FRIGHTENED_GHOST_WEIGHT': .105,
    'PROXIMITY_PELLET_MULTIPLIER': .1,
    'ANTI_CORNER_WEIGHT': .1
}


class MyThread(threading.Thread):
    def __init__(self, threadID, name, scores, counter, print_stuff=False, weight_set=WEIGHT_SET, run_on_clock=USE_CLOCK):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.scores = scores
        self.counter = counter
        self.print_stuff = print_stuff
        self.weight_set = weight_set
        self.run_on_clock = run_on_clock

    def run(self):
        if self.print_stuff:
            print("Starting " + self.name)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        game = GameEngine(ADDRESS, PORT, weight_set=self.weight_set, run_on_clock=self.run_on_clock, using_visualizer=USING_VISUALIZER)
        if self.run_on_clock:
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
        initial_function_evals=[[]],
        relative_noise_magnitude=0.001,
    )
    # if the optimizer expects that refining the current best solution won't result
    # in an improvement of at least this amount, then it will explore elsewhere
    optimizer.set_solver_epsilon(100) # in score units

    # main eval/solver loop
    best_score = -math.inf
    while True:
        next_eval_request = optimizer.get_next_x()
        if PRINT_ALL:
            print('Evaluating with parameters:')
            print(list(next_eval_request.x))
            print(list(next_eval_request.x))
            print(list(next_eval_request.x))
            for name, value in zip(HYPERPARAM_RANGES.keys(), next_eval_request.x):
                print(f'  {name}: {value}')
        avg_score = test_hyperparams(*next_eval_request.x)
        next_eval_request.set(avg_score)

        if avg_score > best_score:
            best_score = avg_score
            print('New best score:', best_score)
            print(f'  Params: {dict(zip(HYPERPARAM_RANGES.keys(), next_eval_request.x))}')
            print()

        # check if stdin has input and stop if so
        # if select.select([sys.stdin,],[],[],0.0)[0]:
        #     # termios.tcflush(sys.stdin, termios.TCIOFLUSH)  # flush stdin to prevent keypresses from going to the shell
        #     break
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
    'FEAR':                    (0, 15, False),
    'PELLET_WEIGHT':           (-15.0, 15.0, False),
    'SUPER_PELLET_WEIGHT':     (-15.0, 15.0, False),
    'GHOST_WEIGHT':            (-15.0, 15.0, False),
    'FRIGHTENED_GHOST_WEIGHT': (-15.0, 15.0, False),
    'PROXIMITY_PELLET_MULTIPLIER': (-15.0, 15.0, False),
    'ANTI_CORNER_WEIGHT': (-15.0, 15.0, False)
}

def test_hyperparams(*args):
    """
    Evaluates the algorithm with the given hyperparameters. Returns the average score.
    """
    weight_set = dict(zip(HYPERPARAM_RANGES.keys(), args))
    if PRINT_ALL:
        print(weight_set)

    start = time.time()

    if USE_CLOCK:
        threads = []
        scores = []
        numThreads = 1
        notifyInterval = 100

        # Create new threads
        for i in range(1, numThreads+1):
            scores.append(None)
            threads.append(MyThread(i, "Thread-" + str(i), scores, i-1, print_stuff=False, weight_set=weight_set, run_on_clock=USE_CLOCK))

        # Start new Threads
        for i in range(numThreads):
            threads[i].start()
            if PRINT_ALL and i % notifyInterval == 0:
                print('Starting thread ' + str(i) + '...')

        # Join new Threads
        for i in range(numThreads):
            threads[i].join()

        end = time.time()
        if PRINT_ALL:
            print('done in ' + str(end - start) + ' s')

        sum = 0
        for i in range(numThreads):
            # print(scores[i])
            sum += scores[i]['score']
            if scores[i]['score'] > 11000 and PRINT_ALL:
                print('super score: ' + str(weight_set))
            # print(str(scores[i]))
        avg_score = sum / numThreads
        if PRINT_ALL:
            print('average score: ' + str(avg_score))
        return avg_score
    else:

        results = []
        numGamesFinished = 0
        totalNumGames = 70
        for i in range(totalNumGames):
            game = GameEngine(ADDRESS, PORT, weight_set=weight_set, run_on_clock=USE_CLOCK,
                            using_visualizer=USING_VISUALIZER)
            if PRINT_ALL:
                print(game.final_state)
            results.append(game.final_state['score'])
            if True:
                numGamesFinished += 1

        all_results.append(results)
        with open('data.npy', 'wb') as f:
            np.save(f, all_results)

        mean_score = np.mean(results)
        print(f'average score: {mean_score}')
        print(f'number of games finished: {numGamesFinished} / {totalNumGames}')
        return mean_score

all_results = []


def get_data():
    all_results = []
    
    for fear in tqdm(np.linspace(0, 15, num=25)):
        weight_set = WEIGHT_SET
        weight_set['FEAR'] = fear
        
        results = []
        for i in range(50):
            game = GameEngine(ADDRESS, PORT, weight_set=weight_set, run_on_clock=USE_CLOCK,
                            using_visualizer=USING_VISUALIZER)
            if PRINT_ALL:
                print(game.final_state)
            results.append(game.final_state['score'])

        all_results.append((fear, results))
        with open('data.npy', 'wb') as f:
            np.save(f, all_results)

def main():
    find_best_parameters()
    # get_data()


if __name__ == "__main__":
    main()
