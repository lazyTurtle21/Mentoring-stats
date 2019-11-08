import unittest

from dateutil.relativedelta import relativedelta
from datetime import datetime

import sys  # for correct import

sys.path.append('../')
from sources.parsing import parse_date_range, parse_date, parse_events


class TestParseDate(unittest.TestCase):
    def test_not_string_format(self):
        self.assertIsNone(parse_date(4))
        self.assertIsNone(parse_date([]))
        self.assertIsNone(parse_date({}))

    def test_invalid_string(self):
        self.assertIsNone(parse_date('11-10-2016'))
        self.assertIsNone(parse_date('11-2016'))
        self.assertIsNone(parse_date('2016'))
        self.assertIsNone(parse_date('hi'))

    def test_valid_string(self):
        now = datetime.today()
        self.assertEqual(parse_date(now.strftime('%Y-%m-%d')), datetime(now.year, now.month, now.day))

        year_ago = now - relativedelta(years=1)
        self.assertEqual(parse_date(year_ago.strftime('%Y-%m-%d')),
                         datetime(year_ago.year, year_ago.month, year_ago.day))

        leap_year = datetime(2012, 2, 29)
        self.assertEqual(parse_date(leap_year.strftime('%Y-%m-%d')),
                         datetime(leap_year.year, leap_year.month, leap_year.day))

        year_from_now = now + relativedelta(years=1)
        self.assertEqual(parse_date(year_from_now.strftime('%Y-%m-%d')),
                         datetime(year_from_now.year, year_from_now.month, year_from_now.day))

        self.assertEqual(parse_date(year_from_now.isoformat()),
                         datetime(year_from_now.year, year_from_now.month, year_from_now.day))


class TestParseDateRange(unittest.TestCase):
    def setUp(self) -> None:
        self.default_return = (None, None)

    def test_not_string_format(self):
        self.assertEqual(parse_date_range(4), self.default_return)
        self.assertEqual(parse_date_range([], {}), self.default_return)

    def test_invalid_string(self):
        self.assertEqual(parse_date_range('а', 'b'), self.default_return)
        self.assertEqual(parse_date_range('2019-10-09', 'hi'), self.default_return)

    def test_valid_string(self):
        now = datetime.today()
        now_y_m_d = now.strftime('%Y-%m-%d')
        year_ago_y_m_d = (now - relativedelta(years=1)).strftime('%Y-%m-%d')
        leap_year = datetime(2012, 2, 29)
        leap_y_m_d = leap_year.strftime('%Y-%m-%d')

        returned = parse_date_range(date_to=now_y_m_d)
        self.assertEqual(len(returned), 2)
        self.assertListEqual([returned[0].strftime('%Y-%m-%d'), returned[1].strftime('%Y-%m-%d')],
                             [year_ago_y_m_d, now_y_m_d])

        returned = parse_date_range(date_to=now_y_m_d, date_from=leap_y_m_d)
        self.assertEqual(len(returned), 2)
        self.assertListEqual([returned[0].strftime('%Y-%m-%d'), returned[1].strftime('%Y-%m-%d')],
                             [leap_y_m_d, now_y_m_d])


class TestParseEvents(unittest.TestCase):
    def test_valid_events(self):
        now = datetime.today()
        now_y_m_d = now.strftime('%Y-%m-%d')

        events = [{'summary': 'Mentoring: mentor1-mentee', 'start': {'date': now_y_m_d}},
                  {'summary': 'Mentoring: mentor2-mentee', 'start': {'date': now_y_m_d}},
                  {'summary': 'Mentoring: mentor1-mentee', 'start': {'dateTime': now.isoformat()}}]
        returned_stats = parse_events(events)
        self.assertEqual(returned_stats, [
                        {'surname': 'mentor1',
                         "from": now_y_m_d,
                         "hours": 1.0,
                         "to": now_y_m_d},
                        {'surname': 'mentor2',
                         "from": now_y_m_d,
                         "hours": 0.5,
                         "to": now_y_m_d}
        ])

        returned_stats = parse_events(events, surname='mentor2')
        self.assertEqual(returned_stats,
                         {'surname': 'mentor2',
                          "from": now_y_m_d,
                          "hours": 0.5,
                          "to": now_y_m_d}
                         )

        returned_stats = parse_events([{'summary': 'not_mentoring event', 'start': {'date': now_y_m_d}}])
        self.assertEqual(returned_stats, {})

    def test_not_valid_events(self):
        returned_stats = parse_events([])
        self.assertEqual(returned_stats, {})

        returned_stats = parse_events({})
        self.assertEqual(returned_stats, {})

        returned_stats = parse_events('')
        self.assertEqual(returned_stats, {})


if __name__ == '__main__':
    unittest.main()
