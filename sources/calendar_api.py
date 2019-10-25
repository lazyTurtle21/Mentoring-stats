import os.path
import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def set_up_api_service(scopes=None, pickle_token_path='token.pickle', json_creds_path='credentials.json'):
    creds = None
    # Pickle token stores the user's access and refresh tokens
    if os.path.exists(pickle_token_path):
        with open(pickle_token_path, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(json_creds_path, scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(pickle_token_path, 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)


def get_calendars_list(service, page_token=None):
    calendars = []
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        calendars += calendar_list['items']
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break
    return calendars


def get_all_events(service, calendar_id='primary', date_from=None, date_to=None, order_by='startTime'):
    all_events = []
    page_token = None
    while True:
        events = service.events().list(calendarId=calendar_id, pageToken=page_token,
                                       singleEvents=True, orderBy=order_by,
                                       timeMin=date_from, timeMax=date_to).execute()
        all_events += events['items']
        page_token = events.get('nextPageToken')
        if not page_token:
            break
    return all_events
