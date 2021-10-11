import subprocess
import time

results = []

with open("test_weights.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        weights = line.split(' ')
        if len(weights) == 6:
            print(','.join(weights))
            with open("../botCode/weights.txt", "w") as f:
                f.write(' '.join(weights))
            score = 0

            pacbotNoVisToFile = subprocess.Popen(["sh", "pacbotNoVisToFile.sh"])

            time.sleep(5)

            pacbotNoVisToFile.terminate()

            with open("tests/currenttest/Pacman.txt", "r") as pacmantxt:
                pacmanLines = pacmantxt.readlines()
                for processLine in pacmanLines:
                    if processLine[:7] == 'score: ':
                        score = processLine[7:]

            # print('creating subprocesses')
            #
            # gameEngineServer = subprocess.Popen(["python3", "../gameEngine/server.py"])
            # botCodeServer = subprocess.Popen(["python3", "../botCode/server.py"])
            #
            # time.sleep(1)
            #
            # pacbotCommsModule = subprocess.Popen(["python3", "../botCode/pacbotCommsModule.py"])
            #
            # time.sleep(1)
            #
            # highLevelPacman = subprocess.Popen(["python3", "../botCode/highLevelPacman.py"], shell=True, stdout=subprocess.PIPE)
            #
            # time.sleep(1)
            #
            # gameEngine = subprocess.Popen(["python3", "../gameEngine/gameEngine.py", "<<", "p.txt"])
            #
            # print('processes created')
            #
            # time.sleep(10)
            #
            # print('sleep done')
            #
            # for processLineBinary in highLevelPacman.communicate():
            #     processLine = processLineBinary.decode('ascii')
            #     print(processLine)
            #     if processLine == 'Stop\n':
            #         highLevelPacman.terminate()
            #     elif processLine[:7] == 'score: ':
            #         score = processLine[7:]





            # process = subprocess.Popen("sh pacbotNoVis.sh", shell=True, stdout=subprocess.PIPE)
            # process = subprocess.Popen(["sh", "pacbotNoVis.sh"], stdout=subprocess.PIPE)
            #
            # for processLine in process.stdout:
            #     print('PROCESS: ' + processLine)
            #     if processLine[:7] == 'score: ':
            #         score = processLine[7:]
            # print('subprocess created')
            # try:
            #     outs, errs = process.communicate(timeout=5)
            #     for processLine in outs:
            #         print(processLine)
            #         if processLine == 'Stop\n':
            #             process.kill()
            #         elif processLine[:7] == 'score: ':
            #             score = processLine[7:]
            # except subprocess.TimeoutExpired:
            #     process.kill()
            print('subprocess complete: score: ' + str(score))
            # for processLineBinary in process.stdout:
            #     processLine = processLineBinary.decode('ascii')
            #     print(processLine)
            #     if processLine == 'Stop\n':
            #         process.terminate()
            #     elif processLine[:7] == 'score: ':
            #         score = processLine[7:]
            results.append(score)
        break  # only do 1 iteration for now

print(results)


