import subprocess
import sys
import time
from datetime import datetime

results = 0
ports = [11295, 12295]

with open("test_weights.txt", "r") as f:
    lines = f.readlines()
    processes = {}
    if len(lines) > 1000:
        print('Only up to 1000 tests at a time are supported!')
    else:
        for line in lines:
            weights = line.split(' ')
            if len(weights) == 6:
                with open("../botCode/weights.txt", "w") as f:
                    f.write(' '.join(weights))

                processes[str(ports[0])] = subprocess.Popen(["sh", "pacbotNoVisToFileV2.sh", str(ports[0]), str(ports[1])])
                print('Process #' + str(len(processes.keys())) + ' initialized.')

                ports[0] += 1
                ports[1] += 1
                time.sleep(3)

    print('All processes initialized.')
    time.sleep(5)

    completedProcesses = {}
    while len(processes) > 0:
        for process in processes:
            if process not in completedProcesses:
                consecutiveStopCount = 0
                with open("tests/currenttest_"+process+"/Pacman.txt", "r") as pacmantxt:
                    pacmantxtlines = pacmantxt.readlines()[1:]
                for pacmantxtline in pacmantxtlines:
                    if pacmantxtline == 'Stop\n':
                        consecutiveStopCount += 1
                    else:
                        consecutiveStopCount = 0
                if consecutiveStopCount >= 10:
                    processes[process].terminate()
                    completedProcesses[process] = processes[process]
        print(str(len(completedProcesses)*100/len(processes))+"% complete")
        time.sleep(10)

    print('Collecting scores...')

    scores = []
    for process in completedProcesses:
        score = 0
        with open("tests/currenttest_"+process+"/Pacman.txt", "r") as pacmantxt:
            pacmanLines = pacmantxt.readlines()
            for processLine in pacmanLines:
                if processLine[:7] == 'score: ':
                    score = str(int(processLine[7:]))
                    
        scores.append(score)

    print('Writing scores...')

    with open("test_weights_results.txt", "a") as f:
        f.write('\n'.join(scores))

    print('Finished.')
