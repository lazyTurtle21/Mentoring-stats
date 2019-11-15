from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow


def set_up_api_service(scopes=None, json_creds_path='credentials.json'):
    flow = InstalledAppFlow.from_client_secrets_file(json_creds_path, scopes)
    creds = flow.run_local_server(port=0)
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
