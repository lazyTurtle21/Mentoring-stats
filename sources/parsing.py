import datetime
from dateutil.relativedelta import relativedelta
from collections import defaultdict


def parse_date(date):
    """
    Check if date is correct. If not, return None, otherwise convert it to datetime object.
    :param date: string in format YYYY-MM-DD
    :return: datetime.datetime object
    """
    if type(date) != str:
        return None
    if 'T' in date:  # if time is specified
        date = date[0:date.find('T')]
    date_list = date.split('-')
    if len(date_list) != 3:
        return None

    try:
        date_list = [int(el) for el in date_list]
        parsed_date = datetime.datetime(date_list[0], date_list[1], date_list[2])
    except ValueError:  # if at least one element in the list cannot be converted to integer or out of range
        return None

    return parsed_date


def parse_date_range(date_from=None, date_to=None):
    """Set correct date range"""
    date_to = parse_date(date_to) if date_to else datetime.datetime.utcnow()  # if not specified, set to current date
    if date_to is None:
        return date_from, date_to
    date_from = parse_date(date_from) if date_from else date_to - relativedelta(years=1)
    if all([date_to, date_from]) and date_to < date_from:
        return None, None
    return date_from, date_to


def parse_events(events, surname=None):
    def parse_one_mentor(m_events, last_name):
        first_event, last_event = parse_date(m_events[0]['start']), parse_date(m_events[-1]['start'])
        return {'surname': last_name, 'hours': len(m_events) / 2,
                'from': f'{first_event.year}-{first_event.month}-{first_event.day}',
                'to': f'{last_event.year}-{last_event.month}-{last_event.day}'}

    start = "Mentoring: "
    start_length = len(start)
    filter_function = lambda e: e['summary'].startswith(start + (surname + '-' if surname else ''))
    events = [
        {
            'summary': event['summary'],
            'start': event['start'].get('dateTime', event['start'].get('date'))
        }
        for event in events if filter_function(event)
    ]
    if not events:
        return {}
    if surname:
        return parse_one_mentor(events, surname)

    events_by_surname = defaultdict(lambda: [])
    for event in events:
        name = event['summary'][start_length: event['summary'].find('-')]
        events_by_surname[name] += [event]

    parsed_events = [parse_one_mentor(events_by_surname[key], key) for key in events_by_surname]
    return parsed_events
