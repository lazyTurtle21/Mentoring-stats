from flask import request, jsonify, Flask, abort
from sources.calendar_api import get_all_events, get_calendars_list, set_up_api_service
from sources.parsing import parse_events
from flask_rest_api import Api, Blueprint, abort
from sources.schemas import *

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

app = Flask('API')

if 'CREDS' not in app.config.keys():
    app.config['CREDS'] = '../credentials.json'

app.config['OPENAPI_VERSION'] = '3.0.2'
app.config['OPENAPI_URL_PREFIX'] = '/docs'
app.config['OPENAPI_SWAGGER_UI_VERSION'] = '3.3.0'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger_ui'
app.config['OPENAPI_REDOC_PATH'] = '/redoc_ui'

api = Api(app)
blp = Blueprint('api', 'api', url_prefix='/api/v1',
                description='Mentoring statistics')


@blp.route('/', methods=["GET"])
@blp.arguments(MentoringStatsArgs, location='query')
@blp.response(MentoringStatsResponse(many=True), description="Return statistics if such mentor is found.",
              example={
                  "from": "2019-7-16",
                  "hours": 1.0,
                  "surname": "mentor",
                  "to": "2019-10-20"
              })
@blp.response(code=422, description="Invalid date format.")
@blp.response(code=404, description="Mentor not found.")
def get(_):
    """Get mentoring statistics

    Return statistics for mentor(s) in the specified date range
    """
    surname = request.args.get('surname')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')

    if 'CALENDAR_SERVICE' not in app.config.keys():
        app.config['CALENDAR_SERVICE'] = set_up_api_service(scopes=SCOPES, json_creds_path=app.config['CREDS'])

    calendar_list = get_calendars_list(app.config['CALENDAR_SERVICE'])  # for testing
    test_calendar_id = list(filter(lambda calender: calender['summary'] == 'test', calendar_list))
    test_calendar_id = test_calendar_id[0]['id'] if test_calendar_id else 'primary'

    d_from, d_to = parse_date_range(date_from=date_from, date_to=date_to)
    if not all([d_from, d_to]):
        abort(422, f'"{date_from if not d_from else date_to}" is not a correct value for date.')

    all_events = get_all_events(app.config['CALENDAR_SERVICE'], calendar_id=test_calendar_id,
                                date_from=d_from.isoformat() + 'Z', date_to=d_to.isoformat() + 'Z')

    parsed_events = parse_events(all_events, surname)
    if parsed_events:
        return jsonify(parsed_events)
    else:
        abort(404, "Mentor not found.")


api.register_blueprint(blp)

if __name__ == '__main__':
    app.run(debug=True)
