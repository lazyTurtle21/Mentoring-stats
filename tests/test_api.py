import unittest

import sys  # for correct import
import json

sys.path.append('../')
from sources.api import app


class TestAPIServer(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.url = '/api/v1'
        self.assertEqual(app.debug, False)
        self.required_cols = {'surname', 'hours', 'from', 'to'}
        self.OK = 200
        self.NOT_FOUND = 404
        self.INCORRECT_DATE = 422

    def test_initial_page(self):
        response = self.app.get(self.url + '/', follow_redirects=True)
        self.assertEqual(response.status_code, self.OK)
        returned = json.loads(response.data)
        self.assertEqual(type(returned), list)
        if returned:
            for item in returned:
                self.assertEqual(self.required_cols, set(item.keys()))

    def test_one_mentor(self):
        response = self.app.get(self.url + '/?surname=mentor1', follow_redirects=True)
        self.assertIn(response.status_code, [self.OK, self.NOT_FOUND])
        if response.status_code != self.NOT_FOUND:
            returned = json.loads(response.data)
            self.assertEqual(type(returned), dict)
            if returned:
                self.assertEqual(self.required_cols, set(returned.keys()))

    def test_incorrect_dates(self):
        response = self.app.get(self.url + '/?date_from=12345')
        self.assertEqual(response.status_code, self.INCORRECT_DATE)

        response = self.app.get(self.url + '/?date_from=hihello&date_to=2044-11-02')
        self.assertEqual(response.status_code, self.INCORRECT_DATE)

        response = self.app.get(self.url + '/?date_from=11-02-2016&date_to=11-02-2019')
        self.assertEqual(response.status_code, self.INCORRECT_DATE)

        response = self.app.get(self.url + '/?date_from=2019-01-02&date_to=2018-07-08')
        self.assertEqual(response.status_code, self.INCORRECT_DATE)

    def test_correct_dates(self):
        response = self.app.get(self.url + '/?date_from=2019-01-02&date_to=2019-07-08&surname=mentor1')
        self.assertIn(response.status_code, [self.OK, self.NOT_FOUND])

        response = self.app.get(self.url + '/?date_from=2019-01-02&date_to=2019-07-08')
        self.assertIn(response.status_code, [self.OK, self.NOT_FOUND])

        response = self.app.get(self.url + '/?date_from=2019-01-02')
        self.assertIn(response.status_code, [self.OK, self.NOT_FOUND])

        response = self.app.get(self.url + '/?date_to=2019-01-02')
        self.assertIn(response.status_code, [self.OK, self.NOT_FOUND])


if __name__ == "__main__":
    unittest.main()
