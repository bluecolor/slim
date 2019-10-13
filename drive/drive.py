from __future__ import print_function
import math
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class Drive():
    def __init__(self, *args, **kwargs):
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        self.SPREADSHEET_ID = '17U8YorOXw-6AsBFHOtqyaTigAeAg-v_ANJ5JNWw5TYI'
        self.RANGE_NAME = 'A1:F8'
        self.__auth()
        self.sheets = []
        super().__init__(*args, **kwargs)

    def __auth(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token: creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        self.service = build('sheets', 'v4', credentials=creds)
        self.sheet = self.service.spreadsheets()


    def _read_meta(self):
        print("Reading sheet metadata ...")
        sheet_metadata = self.service.spreadsheets().get(spreadsheetId=self.SPREADSHEET_ID).execute()
        properties = sheet_metadata.get('sheets')
        self.sheets = [{'sheet_id': i['properties']['sheetId'], 'day': i['properties']['title']} for i in properties]
        print("Got sheet metadata.")

    def read(self):
        self._read_meta()
        document = []
        for s in self.sheets:
            result = self.sheet.values().get(
                spreadsheetId=self.SPREADSHEET_ID, range=f'{s["day"]}!{self.RANGE_NAME}').execute()
            values = result.get('values', [])
            if not values:
                print(f'No data found. for {s["day"]}')
            else:
                data = []
                for row in values[1:]:
                    record = {
                        'plan': row[0],
                        'preriod': row[1],
                        'start': row[2],
                        'end': row[3],
                        'status': row[4],
                        'duration': math.floor(int(row[5])/60),
                    }
                    data.append(record)

                sheet = {
                    'meta': s,
                    'data': data
                }
                document.append(sheet)

        return document


document = Drive().read()


def find_max_day():
    days = []
    for sheet in document:
        days.append(sheet['meta']['day'])
    return max(days)


