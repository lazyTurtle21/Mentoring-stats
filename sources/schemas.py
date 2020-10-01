import marshmallow as ma
import datetime
from parsing import parse_date_range


class MentoringStatsArgs(ma.Schema):
    surname = ma.fields.String(description="Mentor's surname. If not specified, return statistic for all mentors.")
    date_from = ma.fields.String(description='Start date in format YYYY-MM-DD. If not specified, set to current date.',
                                 missing=parse_date_range()[0].strftime('%Y-%m-%d'))
    date_to = ma.fields.String(description='Finish date in format YYYY-MM-DD. '
                                           'If not specified, set to date_from - 1 year.',
                               missing=datetime.datetime.today().strftime('%Y-%m-%d'))


class MentoringStatsResponse(ma.Schema):
    surname = ma.fields.String(description="Mentor's surname")
    date_to = ma.fields.String(description='Finish date')
    date_from = ma.fields.String(description='Start date')
    hours = ma.fields.Float(description='Total hours spent on mentoring')
