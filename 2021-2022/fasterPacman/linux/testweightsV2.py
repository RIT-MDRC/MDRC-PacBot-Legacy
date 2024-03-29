import subprocess
import sys
import time
from datetime import datetime
import socket

results = 0
ports = [11295, 15295]

with open("test_weights.txt", "r") as f:
    lines = f.readlines()
    processes = {}
    if len(lines) > 1000:
        print('Only up to 1000 tests at a time are supported!')
    else:
        for line in lines:
            weights = line.split(' ')
            if len(weights) == 6:
                with open("../gameEngine/botCode/weights.txt", "w") as f:
                    f.write(' '.join(weights))

                processes[str(ports[0])] = subprocess.Popen(["sh", "pacbotNoVisToFileV2.sh", str(ports[0]), str(ports[1])], stdout=subprocess.DEVNULL)
                print('Process ' + str(len(processes.keys())) + '/' + str(len(lines)) + ' initialized.')

                ports[0] += 1
                ports[1] += 1

                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex(('127.0.0.1', ports[0]))
                result1 = sock.connect_ex(('127.0.0.1', ports[1]))
                if result != 0 or result1 != 0:
                    sock.close()
                    sock1.close()
                    ports[0] += 1
                    ports[1] += 1
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    result = sock.connect_ex(('127.0.0.1', ports[0]))
                    result1 = sock.connect_ex(('127.0.0.1', ports[1]))
                sock.close()
                sock1.close()

                time.sleep(0.5)

    print('All processes initialized. Waiting for files to be created.')
    time.sleep(15)
    print('Assuming files are created. Waiting for results.')

    completedProcesses = {}
    while len(processes) > len(completedProcesses):
        for process in processes:
            if process not in completedProcesses:
                consecutiveStopCount = -1
                with open("tests/currenttest_"+process+"/Pacman.txt", "r") as pacmantxt:
                    pacmantxtlines = pacmantxt.readlines()[1:]
                for pacmantxtline in pacmantxtlines:
                    if pacmantxtline == 'Stop\n':
                        if consecutiveStopCount >= 0:
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
