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
                        score = str(int(processLine[7:]))

            print('subprocess complete: score: ' + str(score))
            results.append(score)

print(results)


