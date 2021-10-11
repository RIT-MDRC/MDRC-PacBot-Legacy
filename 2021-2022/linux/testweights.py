import subprocess

with open("test_weights.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        weights = line.split(' ')
        print(','.join(weights))
        with open("../botCode/weights.txt", "w") as f:
            f.write(' '.join(weights))
        process = subprocess.Popen("sh pacbotNoVisToFile.sh", shell=True, stdout=subprocess.PIPE)

