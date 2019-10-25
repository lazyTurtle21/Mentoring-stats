from flask import Blueprint, request, jsonify, Flask, abort
from sources.calendar_api import get_all_events, get_calendars_list, set_up_api_service
from sources.parsing import parse_date_range, parse_events

api = Blueprint('api', __name__)
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
calendar_service = set_up_api_service(scopes=SCOPES, pickle_token_path='../token.pickle')


@api.route('/', methods=["GET"])
def get():
    surname = request.args.get('surname')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')

    calendar_list = get_calendars_list(calendar_service)  # for testing
    test_calendar_id = list(filter(lambda calender: calender['summary'] == 'test', calendar_list))
    test_calendar_id = test_calendar_id[0]['id'] if test_calendar_id else 'primary'

    d_from, d_to = parse_date_range(date_from=date_from, date_to=date_to)
    if d_from is None or d_to is None:
        abort(422, f'"{date_from if not d_from else date_to}" is not a correct value for date.')

    all_events = get_all_events(calendar_service, calendar_id=test_calendar_id,
                                date_from=d_from.isoformat() + 'Z', date_to=d_to.isoformat() + 'Z')

    return jsonify(parse_events(all_events, surname))


if __name__ == '__main__':
    app = Flask(__name__)
    app.register_blueprint(api, url_prefix='/api/v1')
    app.run(debug=True)
