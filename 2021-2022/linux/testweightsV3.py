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
    result = sheet.values().append(spreadsheetId=SPREADSHEET_ID, range="Results", valueInputOption="USER_ENTERED", body=({'majorDimension': 'ROWS', 'values': [[1,2,3,4,5,6]+[2]]})).execute()

    def getRange(myRange):
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=myRange).execute()
        return result.get('values', [])

    processes = {}
    results = 0
    ports = [11295, 15295]

    while 1:
        values = getRange('Dashboard!A2:A2')
        if values[0][0].lower() == 'stop':
            print('The dashboard has indicated that I should stop. Goodbye!')
            break
        elif values[0][0].lower() == 'run':
            values = getRange('Dashboard!A4:A4')
            if len(processes.keys()) >= int(values[0][0]):
                print('Maximum number of processes (' + str(values[0][0]) + ') already running.')
            else:
                values = getRange('Dashboard!B:B')
                if not values:
                    print('No data found.')
                else:
                    rowNum = math.floor(random.random()*(len(values)-1)) + 1
                    weights = values[rowNum][0].split(' ')
                    if len(weights) == 6:
                        print('Testing weight set: ' + ', '.join(weights))
    
                        with open("../botCode/weights.txt", "w") as f:
                            f.write(' '.join(weights))
    
                        processes[str(ports[0])] = [weights, subprocess.Popen(["sh", "pacbotNoVisToFileV2.sh", str(ports[0]), str(ports[1])], stdout=subprocess.DEVNULL)]
                        print('Process initialized.')
    
                        ports[0] += 1
                        ports[1] += 1
    
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
                    else:
                        print('Invalid weight set: ' + str(weights[0]))
        elif values[0][0].lower() == 'pause':
            print('Paused...')
        else:
            print('Invalid instruction "' + str(values[0][0]) + '" should be either "run" or "stop"')

        # check for results
        completedProcesses = []
        for process in processes:
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
                processes[process][1].terminate()
                completedProcesses.append(process)
        for process in completedProcesses:
            score = 0
            with open("tests/currenttest_" + process + "/Pacman.txt", "r") as pacmantxt:
                pacmanLines = pacmantxt.readlines()
                for processLine in pacmanLines:
                    if processLine[:7] == 'score: ':
                        score = str(int(processLine[7:]))

            # submit score to google sheets
            sheet = service.spreadsheets()
            result = sheet.values().append(spreadsheetId=SPREADSHEET_ID, range="Results",
                                           valueInputOption="USER_ENTERED", body=(
                {'majorDimension': 'ROWS', 'values': [completedProcesses[process][0] + [score]]})).execute()
            processes.pop(process)

if __name__ == '__main__':
    main()