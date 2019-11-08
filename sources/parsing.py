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
    """Set correct date range
    If date_to is None, set to current date
    If date_from is None, set to date_to - 1 year
    :param date_from: string in format YYYY-MM-DD
    :param date_to: string in format YYYY-MM-DD
    :return: datetime.datetime object if date_to and date_from are correct; otherwise - None, None
    """
    date_to = parse_date(date_to) if date_to is not None else datetime.datetime.utcnow()  # if not specified, set to current date
    if date_to is None:
        return None, None
    date_from = parse_date(date_from) if date_from is not None else date_to - relativedelta(years=1)
    if not all([date_to, date_from]) or (date_to < date_from):
        return None, None
    return date_from, date_to


def parse_events(events, surname=None):
    """
    :param events: list of dictionaries that has keys 'summary' and 'start'
    :param surname: mentor's surname
    :return: list of statistics
    """
    def parse_one_mentor(m_events, last_name):
        first_event, last_event = parse_date(m_events[0]['start']), parse_date(m_events[-1]['start'])
        return {'surname': last_name, 'hours': len(m_events) / 2,
                'from': first_event.strftime('%Y-%m-%d'),
                'to': last_event.strftime('%Y-%m-%d')}

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
