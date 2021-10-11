import subprocess
import time

results = []

with open("test_weights.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
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

            time.sleep(5)
            print('Process terminated. Retrieving data...')

            with open("tests/currenttest/Pacman.txt", "r") as pacmantxt:
                pacmanLines = pacmantxt.readlines()
                for processLine in pacmanLines:
                    if processLine[:7] == 'score: ':
                        score = str(int(processLine[7:]))

            print('Iteration complete: score: ' + str(score))
            results.append(score)

print(results)

with open("test_weights_results.txt", "w") as f:
    f.write('\n'.join(results))


