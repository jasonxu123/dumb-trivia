# will need this for Vercel
# from dotenv import load_dotenv
# import os
from typing import List, Tuple, Any
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# from online docs
GOOGLE_SPREADSHEET_FILE_TYPE = 'application/vnd.google-apps.spreadsheet'

CREDS_FILE = '/Users/jasonxu/dumb-trivia/account1-dumb-trivia-321.json'

SA_HOME_FOLDER = '1LjGx6741JfmmyqhZ4RLonT7HWmvuzTmY'
TEST_SHEET_ID = '1yqd34HMjq4oHJfQK2X6JXu1LPSU7UPPEiNKYEjxaQl4'
NEW_TAB_NAMES = ['tab 1', 'Programmatic Tab']
TEST_VALUES = [
    ['Answer 1', 98.76, '1/1/2023'],
    ['Answer 2', 'chicken\n| bird', '$101.85'],
    ['Answer 3', 5, 'false'],
    ['Answer 4', '"quotes here"', True],
    ['Answer 5', 'test@gmail.com', 'https://www.google.com'],
]

all_creds = service_account.Credentials.from_service_account_file(
    CREDS_FILE,
    scopes=['https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive']
)
sheets_service = build('sheets', 'v4', credentials=all_creds)
drive_service = build('drive', 'v3', credentials=all_creds)


def create_folder(folder_name):
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
    }
    folder = drive_service.files().create(body=file_metadata, fields='id').execute()
    print(f'Folder ID: {folder["id"]}')
    return folder['id']


def share_folder(fileId, email):
    """NOTE: sharing the root Drive, like `fileId='root'` or using the root Drive ID, is not allowed."""
    new_permission = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': email,
    }
    response = drive_service.permissions().create(
        fileId=fileId,
        body=new_permission,
        sendNotificationEmail=True,
    ).execute()
    print(f"Permission ID: {response.get('id')}")


def get_drive_permissions():
    info = drive_service.about().get(fields='*').execute()
    print(info['user'])
    # about = drive_service.files().get(fileId='root').execute()
    # root_drive_id = about['id']
    # print(root_drive_id)
    # response = drive_service.permissions().list(
    #     fileId='0AOcO1nBFMDM3Uk9PVA').execute()
    # print(response['permissions'])


def find_sheets(query: str):
    response = drive_service.files().list(q=query, fields='files(id)').execute()
    file_ids = [obj['id'] for obj in response['files']]
    print(file_ids)
    return file_ids


def read_sheet(sheet_id: str, tab_name=NEW_TAB_NAMES[0], cell_range='A1:Z1000'):
    response = sheets_service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range=f'{tab_name}!{cell_range}',
    ).execute()
    values = response.get('values', [])
    if not values:
        print('No data found.')
    else:
        for row in values:
            print(row)


def create_sheet_if_new(title: str, parent_folder_id=SA_HOME_FOLDER) -> Tuple[str, bool]:
    """
    Creates a new Google Spreadsheet (i.e. an entirely new file). If a sheet exists in the same
    location with the same name, just return that instead.

    Args:
        title: Title of the Google Sheet
        parent_folder_id: Optional ID of parent folder to put new sheet under.
            If not given, will be in home folder of service account.
    Returns:
        Tuple of (Unique spreadsheet ID of newly created sheet, if sheet was newly created)
    """
    existing_query = f'''
        name = \'{title}\' and
        mimeType = \'{GOOGLE_SPREADSHEET_FILE_TYPE}\' and
        \'{parent_folder_id}\' in parents
    '''
    results = drive_service.files().list(
        q=existing_query, fields='files(id)').execute()
    if len(results['files']):
        return results['files'][0]['id'], False

    # use Drive API to be able to specify file parent
    new_spreadsheet_fields = {
        'mimeType': GOOGLE_SPREADSHEET_FILE_TYPE,
        'parents': [parent_folder_id],
        'name': title,
    }
    response = drive_service.files().create(
        body=new_spreadsheet_fields, fields='id').execute()
    return response['id'], True


def create_tabs(sheet_id: str, tab_names: List[str]):
    """Adds new tabs to an existing Google Sheet (officially, this is what a "sheet" is.)"""
    make_tab_body = {
        'requests': [
            {
                'addSheet': {
                    'properties': {
                        'title': tab_name,
                    }
                }
            }
            for tab_name in tab_names
        ]
    }
    sheets_service.spreadsheets().batchUpdate(
        spreadsheetId=sheet_id,
        body=make_tab_body,
    ).execute()
    return tab_names


def number_to_letter_col(col: int) -> str:
    """Just turn a 1-indexed number into base 26 letter format, e.g. 27 -> AA, 677 -> AAA"""
    letter_col = ''
    while col:
        col -= 1
        next_letter = chr(col % 26 + ord('A'))
        letter_col = letter_col + next_letter
        col = col // 26
    return letter_col


def update_cells(sheet_id: str, tab_name: str, start_row: int, start_col: int, values: List[List[Any]]):
    # TODO: `values` will need to be created based on answer sheet format,
    # i.e. to know where answer to each question should go in sheet.
    """
    Updates cells in a particular row and column section of a Google Sheet.

    Args:
        sheet_id: Spreadsheet to update
        tab_name: Tab to update in spreadsheet, used as part of range
        start_row: 1-indexed number of top row to update
        start_col: 1-indexed number of left-most column to update
        values: 2D array of values to put into sheet
    """
    if not len(values) or not len(values[0]):
        return
    start_letter_col = number_to_letter_col(start_col)
    end_letter_col = number_to_letter_col(start_col + len(values[0]))
    range_to_update = f'{tab_name}!{start_letter_col}{start_row}:{end_letter_col}{start_row + len(values)}'
    print(range_to_update)
    result = sheets_service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=range_to_update,
        valueInputOption='RAW',
        body={'values': values},
    ).execute()
    print(f'{result["updatedCells"]} cells updated.')


def delete_sheet(sheet_id: str):
    """DANGEROUS."""
    drive_service.files().delete(fileId=sheet_id).execute()


def test_sequence():
    try:
        # new_id, new_sheet = create_sheet_if_new('another sheet')
        # print(new_id, new_sheet)
        # create_tabs(new_id, NEW_TAB_NAMES)
        update_cells(TEST_SHEET_ID, NEW_TAB_NAMES[0], 10, 5, TEST_VALUES)
        read_sheet(TEST_SHEET_ID)

        # delete_sheet(new_id)

    except HttpError as error:
        print(f"HTTP error occurred: {error}")
    except Exception as error:
        print(f"A generic exception occurred: {repr(error)}")


test_sequence()
