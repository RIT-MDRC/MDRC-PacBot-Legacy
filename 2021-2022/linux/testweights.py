import subprocess
import sys
import time

results = []

print('waiting...')
time.sleep(5)

with open("test_weights.txt", "r") as f:
    lines = f.readlines()
    if int(sys.argv[0]) < len(lines):
        line = lines[int(sys.argv[0])]
        weights = line.split(' ')
        if len(weights) == 6:

            print('Weights: ' + ', '.join(weights))
            with open("../botCode/weights.txt", "w") as f:
                f.write(' '.join(weights))
            score = 0

            print('Initializing process...')
            pacbotNoVisToFile = subprocess.Popen(["sh", "pacbotNoVisToFile.sh"])
            print('Process initialized.')

            time.sleep(5)

            print('Terminating process...')
            pacbotNoVisToFile.terminate()

            time.sleep(10)
            print('Process terminated. Retrieving data...')

            with open("tests/currenttest/Pacman.txt", "r") as pacmantxt:
                pacmanLines = pacmantxt.readlines()
                for processLine in pacmanLines:
                    if processLine[:7] == 'score: ':
                        score = str(int(processLine[7:]))

            print('Iteration complete: score: ' + str(score))
            results.append(score)

print(results)

with open("test_weights_results.txt", "a") as f:
    f.write('\n'+results[0])



