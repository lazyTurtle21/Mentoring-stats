import unittest

from datetime import datetime
from dateutil.relativedelta import relativedelta

import sys   # for correct import
sys.path.append('../')

from sources.parsing import parse_date


class TestParseDate(unittest.TestCase):
    def test_not_string_format(self):
        self.assertIsNone(parse_date(4))
        self.assertIsNone(parse_date(4.5))
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


if __name__ == '__main__':
    unittest.main()
