from calendar_api import get_all_events, get_calendars_list, set_up_api_service
import argparse


SCOPES = ['https://www.googleapis.com/auth/calendar']


def create_event(event_data, service, calendar_id):
    try:
        service.events().insert(calendarId=calendar_id, body=event_data).execute()
    except Exception as e:
        print('Error happened:', e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--initial', '-i', type=str,
                        help='Name of the calendar to get the events from.', required=True)
    parser.add_argument('--to', '-t', type=str,
                        help='Name of the calendar to write the events to.', required=True)
    args = parser.parse_args()

    service = set_up_api_service(scopes=SCOPES, json_creds_path='../credentials.json')
    calendar_list = get_calendars_list(service)

    from_events_calendar = list(filter(lambda calender: calender['summary'] == args.initial, calendar_list))
    to_events_calendar = list(filter(lambda calender: calender['summary'] == args.to, calendar_list))

    if not from_events_calendar or not to_events_calendar:
        raise Exception('No such calendar: ' + args.initial if not from_events_calendar else args.to)

    events = get_all_events(calendar_id=from_events_calendar[0]['id'], service=service)

    mentoring_events = list(filter(lambda e: e.get('summary', '').startswith('Mentoring:'), events))

    for event in mentoring_events:
        create_event(event, service, to_events_calendar[0]['id'])

    print('Events were created successfully.')
