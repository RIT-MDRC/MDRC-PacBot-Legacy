import subprocess

with open("test_weights.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        weights = line.split(' ')
        print(','.join(weights))
        subprocess.call(["sh", "pacbotNoVisToFile.sh"])

