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
            print('creating subprocess')
            # process = subprocess.Popen("sh pacbotNoVis.sh", shell=True, stdout=subprocess.PIPE)
            process = subprocess.Popen(["sh", "pacbotNoVis.sh"], stdout=subprocess.PIPE)

            for processLine in process.stdout:
                print('PROCESS: ' + processLine)
                if processLine[:7] == 'score: ':
                    score = processLine[7:]
            print('subprocess created')
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


