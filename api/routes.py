from flask import Blueprint, request
from datetime import datetime
from zoneinfo import ZoneInfo
from googleapiclient.errors import HttpError

from api.sheets import _delete_sheet, _create_sheet_if_new, _create_tabs, _update_cells

api_routes = Blueprint('some_name', __name__)


@api_routes.get('/hello')
def home():
    now_str = datetime.now(ZoneInfo('US/Pacific')
                           ).isoformat(sep=' ', timespec='seconds')
    return {'message': f'Hello at this Pacific time: {now_str}'}


@api_routes.post('/test/create-sheet')
def create_and_update_sheet():
    """
    First half of testing function: create a new Google Sheet, add a tab, and add a value.
    The value will be added to the specified tab at the specified column, underneath a header.
    NOTE: won't create a new spreadsheet if an existing test one is still there.

    Request Args:
        tab_name: str, tab to add into new sheet
        new_value: str, value to put into sheet
        col: int, 1-indexed column number to add value to
    Returns:
        sheet_id: of newly created spreadsheet
        message: str
    """
    REQUIRED_ARGS = ['tab_name', 'new_value', 'col']
    req_body = request.get_json()
    for arg in REQUIRED_ARGS:
        if not req_body.get(arg, None):
            return f'Request needs field with non-empty value: {arg}', 400
    if type(req_body['col']) != int or req_body['col'] < 1 or req_body['col'] > 26:
        return f'Please give a column number in range [1, 26] for testing', 400

    err_str = ''
    # this folder already exists in the Google Drive
    TEST_FOLDER_ID = '1wbUcNoLzVHtfNpna7ydprA8KxCgPttPX'
    TEST_SHEET_NAME = 'API test sheet'
    sheet_id = ''
    try:
        sheet_id, is_new = _create_sheet_if_new(
            TEST_SHEET_NAME, parent_folder_id=TEST_FOLDER_ID)
        if not is_new:
            return {'sheet_id': sheet_id, 'message': 'Sheet exists already, no inserts done.'}
        _create_tabs(sheet_id, [req_body['tab_name']])
        _update_cells(sheet_id, req_body['tab_name'], 1, req_body['col'], [
            ['Test Value'], [req_body['new_value']]])
    except HttpError as error:
        err_str = f'HTTP error occurred: {error}'
    except Exception as error:
        err_str = f'A generic exception occurred: {repr(error)}'
    if err_str:
        return err_str, 500
    return {'sheet_id': sheet_id, 'message': 'Created new sheet and inserted given value.'}


@api_routes.post('/test/delete-sheet')
def delete_sheet():
    """Delete sheet given the sheet_id."""
    req_body = request.get_json()
    sheet_to_delete = req_body.get('sheet_id')
    if not sheet_to_delete:
        return 'Request needs non-empty field `sheet_id`', 400
    try:
        _delete_sheet(sheet_to_delete)
    except HttpError as error:
        err_str = (
            f'Unknown sheet_id provided: {error}'
            if error.status_code == 404
            else f'HTTP error occurred: {error}'
        )
        return err_str, 400
    return f'Deleted sheet {sheet_to_delete}'
