# will need this for Vercel
# from dotenv import load_dotenv
# import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

CREDS_FILE = '/Users/jasonxu/dumb-trivia/account1-dumb-trivia-321.json'

SHEET_ID = '1ztMpzzPl4X3FnumcfUHIPwMmsNEIU8XQZFqxRQelRAo'
TAB_NAME = 'answers_0'

loaded_creds = service_account.Credentials.from_service_account_file(
    CREDS_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets'])

service = build('sheets', 'v4', credentials=loaded_creds)


def get_sheet_id() -> str:
    pass


def read_sheet(sheet_id=SHEET_ID, tab_name=TAB_NAME, cell_range='A1:Z1000'):
    response = service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range=f'{tab_name}!{cell_range}'
    ).execute()
    values = response.get('values', [])
    if not values:
        print('No data found.')
    else:
        for row in values:
            print(row)


def update_cell():
    pass


def update_sheet():
    pass


def create_tab():
    pass


read_sheet()
