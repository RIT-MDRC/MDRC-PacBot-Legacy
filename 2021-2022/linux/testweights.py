import subprocess

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
            process = subprocess.Popen("sh pacbotNoVis.sh", shell=True, stdout=subprocess.PIPE)
            for processLine in process.stdout:
                print(processLine)
                if processLine == 'Stop':
                    process.kill()
                    break
                elif processLine[:7] == 'score: ':
                    score = processLine[7:]
            results.append(score)

print(results)


