from __future__ import print_function

import subprocess
import math
import os.path
import random
import time
import socket

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1QDQBckl58-aCvUn4bPmHVkHH8CDi7GZy8oOo-0AxJU4'

spreadsheetInfo = {
    'last_cached': 0.0,
    'status': 'run',
    'max_processes': 1,
    'weight_sets': [[''], []]
}

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    # appending to sheet test
    # sheet = service.spreadsheets()
    # result = sheet.values().append(spreadsheetId=SPREADSHEET_ID, range="Results", valueInputOption="USER_ENTERED", body=({'majorDimension': 'ROWS', 'values': [[1,2,3,4,5,6]+[2]]})).execute()

    def getRange(myRange):
        while 1:
            try:
                # Call the Sheets API
                result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=myRange).execute()
                return result.get('values', [])
            except:
                print('Failed to get range ' + myRange + '. This is likely a Google error, possibly related to rate limiting. There might also be a problem with your internet connection. Sleeping for 10 seconds and trying again.')
                time.sleep(10)

    processes = {}
    results = 0
    ports = [11295, 15295]

    while 1:
        print('1) processes length: ' + str(len(processes.keys())))

        if time.time() > spreadsheetInfo['last_cached'] + 30:
            spreadsheetInfo['last_cached'] = time.time()
            values = getRange('Dashboard!A:B')
            # spreadsheetInfo['status'] = getRange('Dashboard!A2:A2')
            # spreadsheetInfo['max_processes'] = getRange('Dashboard!A4:A4')
            # spreadsheetInfo['weight_sets'] = getRange('Dashboard!B:B')
            spreadsheetInfo['status'] = values[1][0]
            spreadsheetInfo['max_processes'] = values[3][0]
            spreadsheetInfo['weight_sets'] = [v[1] for v in values if len(values) >= 2]

        print('2) data acquired')

        if spreadsheetInfo['status'] == 'stop':
            print('The dashboard has indicated that I should stop. Goodbye!')
            break
        elif spreadsheetInfo['status'] == 'run':
            if len(processes.keys()) >= int(spreadsheetInfo['max_processes']):
                print('3) Maximum number of processes (' + str(spreadsheetInfo['max_processes']) + ') already running.')
            else:
                print('3) Starting new weight set...')
                values = spreadsheetInfo['weight_sets']
                if not values:
                    print('No data found.')
                else:
                    rowNum = math.floor(random.random()*(len(values)-1)) + 1
                    weights = values[rowNum].split(' ')
                    if len(weights) == 6:
                        print('5) Testing weight set: ' + ', '.join(weights))

                        while 1:
                            try:
                                with open("../botCode/weights.txt", "w") as f:
                                    f.write(' '.join(weights))
                                break
                            except:
                                print('Error opening bot/weights.txt file. Sleeping for 5 seconds then trying again.')
                                time.sleep(5)

                        while 1:
                            try:
                                processes[str(ports[0])] = [weights, subprocess.Popen(["sh", "pacbotNoVisToFileV2.sh", str(ports[0]), str(ports[1])], stdout=subprocess.DEVNULL)]
                                break
                            except:
                                print('Error opening process. Sleeping for 5 seconds then trying again.')
                                time.sleep(5)
                        print('6) Process initializing... locating new sockets')
    
                        ports[0] += 1
                        ports[1] += 1

                        while 1:
                            try:
                                # find new ports for next time around
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
                                    result1 = sock2.connect_ex(('127.0.0.1', ports[1]))
                                sock.close()
                                sock1.close()
                                break
                            except:
                                print('Socket port connecting failed. Incrementing ports and trying again in 5 seconds.')
                                ports[0] += 1
                                ports[1] += 1
                                time.sleep(5)

                        print('7) new ports found and saved')
                    else:
                        print('Invalid weight set: ' + str(weights[0]))
        elif spreadsheetInfo['status'] == 'pause':
            print('Paused...')
        else:
            print('Invalid instruction "' + str(spreadsheetInfo['status']) + '" should be either "run" or "stop"')

        print('8) checking for results and terminating completed processes...')
        # check for results
        completedProcesses = {}
        for process in processes:
            consecutiveStopCount = -1
            try:
                with open("tests/currenttest_"+process+"/Pacman.txt", "r") as pacmantxt:
                    pacmantxtlines = pacmantxt.readlines()[1:]
                for pacmantxtline in pacmantxtlines:
                    if pacmantxtline == 'Stop\n':
                        if consecutiveStopCount >= 0:
                            consecutiveStopCount += 1
                    else:
                        consecutiveStopCount = 0
                if consecutiveStopCount >= 10:
                    processes[process][1].kill()
                    completedProcesses[process] = processes[process]
            except:
                # game hasn't started yet
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
                    print('Error reading ' + "tests/currenttest_" + process + "/Pacman.txt" + "; trying again in 5 seconds")
                    time.sleep(5)

            # submit score to google sheets
            while 1:
                try:
                    sheet = service.spreadsheets()
                    result = sheet.values().append(spreadsheetId=SPREADSHEET_ID, range="Results",
                                                   valueInputOption="USER_ENTERED", body=(
                        {'majorDimension': 'ROWS', 'values': [completedProcesses[process][0] + [score]]})).execute()
                    processes.pop(process)
                    break
                except:
                    print('Error submitting results, trying again in 10 seconds.')
                    time.sleep(10)

        print('10) done')
        time.sleep(1)

if __name__ == '__main__':
    main()