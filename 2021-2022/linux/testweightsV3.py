from __future__ import print_function

import subprocess
import math
import os.path
import random
import sys
import time
import socket

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


class TestWeights:
    def __init__(self):
        # If modifying these scopes, delete the file token.json.
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

        # The ID of the spreadsheet.
        self.SPREADSHEET_ID = '1QDQBckl58-aCvUn4bPmHVkHH8CDi7GZy8oOo-0AxJU4'

        self.weight_sets = []
        self.last_cached = 0.0
        self.max_processes = 1

        self.sheet = None

        self.initGoogle()
        self.getFromGoogle()

        self.processes = {}
        self.ports = [11295, 15295]

        print('Initializing processes...')

        while len(self.processes) < self.max_processes:
            print('Process ' + str(len(self.processes)) + ' of ' + str(self.max_processes))
            self.initProcess(self.weight_sets[random.randint(0, len(self.weight_sets))])

        print('Checking for results...')
        while len(self.processes) > 0:
            print('...')
            self.finishProcesses()
            # if time.time() > self.last_cached + 30:
            #     self.getFromGoogle()
            time.sleep(10)

        if self.max_processes == 0:
            sys.exit(1)
        else:
            sys.exit(0)

    def initGoogle(self):
        credentials = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            credentials = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                credentials = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(credentials.to_json())

        service = build('sheets', 'v4', credentials=credentials)
        self.sheet = service.spreadsheets()

    def getFromGoogle(self):
        self.last_cached = time.time()
        values = self.getRange('Dashboard!A:B')
        self.max_processes = min(int(values[3][0]), int(values[5][0]))
        self.weight_sets = [v[1] for v in values[1:] if len(values) >= 2]

    def getRange(self, my_range):
        while 1:
            try:
                # Call the Sheets API
                result = self.sheet.values().get(spreadsheetId=self.SPREADSHEET_ID, range=my_range).execute()
                return result.get('values', [])
            except:
                print('Failed to get range ' + my_range + '. This is likely a Google error, possibly related to rate '
                                                          'limiting. There might also be a problem with your internet '
                                                          'connection. Sleeping for 10 seconds and trying again.')
                time.sleep(10)

    def initProcess(self, weights):
        with open("../botCode/weights.txt", "w") as f:
            f.write(' '.join(weights))
        self.ports[0] += 1
        self.ports[1] += 1
        # print('6) new ports found and saved')
        self.processes[str(self.ports[0])] = [weights,
                                              subprocess.Popen(["sh", "pacbotNoVisToFileV3.sh", str(self.ports[0])],
                                                               stdout=subprocess.DEVNULL),
                                              subprocess.Popen(
                                                  ["python3", "-u", "../gameEngine/server.py", str(self.ports[0]),
                                                   str(self.ports[1])])
                                              ]
        time.sleep(10)
        self.processes[str(self.ports[0])].append(subprocess.Popen(
            ["python3", "-u", "../botCode/server.py", str(self.ports[0]),
             str(self.ports[1])], stdout=subprocess.DEVNULL))
        self.processes[str(self.ports[0])].append(subprocess.Popen(
            ["python3", "-u", "../botCode/pacbotCommsModule.py", str(self.ports[0]),
             str(self.ports[1])], stdout=subprocess.DEVNULL))
        self.processes[str(self.ports[0])].append(subprocess.Popen(
            ["python3", "-u", "botCode/highLevelPacman.py",
             str(self.ports[0]),
             str(self.ports[1]), ">", "linux/tests/currenttest_$1/Pacman.txt"], cwd="../", stdout=subprocess.DEVNULL))
        self.processes[str(self.ports[0])].append(subprocess.Popen(
            ["python3", "-u", "../gameEngine/gameEngine.py",
             str(self.ports[0]),
             str(self.ports[1]), "<<", "../linux/p.txt"], stdout=subprocess.DEVNULL))

    def finishProcesses(self):
        completedProcesses = {}
        for process in self.processes:
            consecutiveStopCount = -1
            try:
                with open("tests/currenttest_" + process + "/Pacman.txt", "r") as pacmantxt:
                    pacmantxtlines = pacmantxt.readlines()[1:]
                for pacmantxtline in pacmantxtlines:
                    if pacmantxtline == 'Stop\n':
                        if consecutiveStopCount >= 0:
                            consecutiveStopCount += 1
                    else:
                        consecutiveStopCount = 0
                if consecutiveStopCount >= 10:
                    for i in range(1, len(self.processes[process]) - 1):
                        self.processes[process][i].kill()
                        self.processes[process][i].wait()
                    completedProcesses[process] = self.processes[process]
            except:
                # game hasn't started yet
                print('Not found: ' + "tests/currenttest_" + process + "/Pacman.txt")
                pass
        print('9) submitting scores...')
        for process in completedProcesses:
            while 1:
                try:
                    score = 0
                    with open("tests/currenttest_" + process + "/Pacman.txt", "r") as pacmantxt:
                        pacmanLines = pacmantxt.readlines()
                        for processLine in pacmanLines:
                            if processLine[:7] == 'score: ':
                                score = str(int(processLine[7:]))
                    break
                except:
                    print(
                        'Error reading ' + "tests/currenttest_" + process + "/Pacman.txt" + "; trying again in 5 seconds")
                    time.sleep(5)

            # submit score to google sheets
            while 1:
                try:
                    result = self.sheet.values().append(spreadsheetId=self.SPREADSHEET_ID, range="Results",
                                                        valueInputOption="USER_ENTERED", body=(
                            {'majorDimension': 'ROWS', 'values': [completedProcesses[process][0] + [score]]})).execute()
                    self.processes.pop(process)
                    break
                except:
                    print('Error submitting results, trying again in 10 seconds.')
                    time.sleep(10)


def main():
    x = TestWeights()


if __name__ == '__main__':
    main()
