import subprocess
import sys
import time
from datetime import datetime

results = 0

print('waiting for ports to close...')
time.sleep(10)

with open("test_weights.txt", "r") as f:
    lines = f.readlines()
    if int(sys.argv[1]) < len(lines):
        line = lines[int(sys.argv[1])]
        weights = line.split(' ')
        if len(weights) == 6:

            print('Weight Set ' + sys.argv[1] + ': ' + ', '.join(weights))
            with open("../botCode/weights.txt", "w") as f:
                f.write(' '.join(weights))
            score = 0

            print('Initializing process...')
            pacbotNoVisToFile = subprocess.Popen(["sh", "pacbotNoVisToFile.sh"])
            print('Process initialized.')

            time.sleep(5)
            consecutiveStopCount = 0
            while consecutiveStopCount < 10: # pacman sometimes stops midgame for a second
                with open("tests/currenttest/Pacman.txt", "r") as pacmantxt:
                    pacmantxtlines = pacmantxt.readlines()[1:]
                for pacmantxtline in pacmantxtlines:
                    if pacmantxtline == 'Stop\n':
                        consecutiveStopCount += 1
                    else:
                        consecutiveStopCount = 0
                print('[' + str(datetime.now().strftime("%H:%M:%S")) + '] Pacman is still going!')
                time.sleep(10)

            print('Terminating process...')
            pacbotNoVisToFile.terminate()

            time.sleep(3)
            print('Process terminated. Retrieving data...')

            with open("tests/currenttest/Pacman.txt", "r") as pacmantxt:
                pacmanLines = pacmantxt.readlines()
                for processLine in pacmanLines:
                    if processLine[:7] == 'score: ':
                        score = str(int(processLine[7:]))

            print('Iteration complete: score: ' + str(score))
            result = score

print('Score: '+result)

with open("test_weights_results.txt", "a") as f:
    f.write('\n'+result)

print('Starting new process... goodbye...')
subprocess.Popen(['nohup', 'lxterminal', '-e', 'python3', 'testweights.py', str(int(sys.argv[1])+1)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

