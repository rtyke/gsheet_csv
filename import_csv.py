from __future__ import print_function
import pickle
import sys
import os.path
import csv

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from config import SPREADSHEET_ID, SHEET_NAME


def auth():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    return service


def get_sheet_id_by_name(service, sheet_name=SHEET_NAME):
    sheet_metadata = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    sheets = sheet_metadata.get('sheets', '')
    for sheet in sheets:
        if sheet['properties']['title'] == sheet_name:
            return sheet['properties']['sheetId']
    return None


def write_row(service, row_number, row):
    sheet_id = get_sheet_id_by_name(service)
    grid_coordinate = {
        'sheetId': sheet_id,
        'rowIndex': row_number,
        'columnIndex': 0,
    }
    change_this = {'requests': [{'pasteData': {
        'coordinate': grid_coordinate,
        'data': row,
        'type': 'PASTE_NORMAL',
        'delimiter': ','
    }}]}

    result = service.spreadsheets().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body=change_this,

    ).execute()
    return result


def yield_csv_row(csv_path, write_first_row=False):
    with open(csv_path) as fo:
        csv_reader = csv.reader(fo)
        for i, row in enumerate(csv_reader):
            if i == 0 and not write_first_row:
                continue
            else:
                yield ', '.join(row)


def get_first_blank_row_coordinate(service):
    first_column_range = "{}!A:A".format(SHEET_NAME)
    first_column_values = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=first_column_range,
    ).execute().get('values', [])
    return len(first_column_values)


def if_import_first_row():
    if len(sys.argv) > 2 and sys.argv[2] == 'first':
        return True
    else:
        return False


def main():
    service = auth()
    row_number = get_first_blank_row_coordinate(service)
    for row in yield_csv_row(
            csv_path=sys.argv[1], write_first_row=if_import_first_row()):
        write_row(service, row_number, row)
        row_number += 1


if __name__ == '__main__':
    main()


