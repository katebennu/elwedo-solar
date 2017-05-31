from datetime import datetime

import unittest

from .range import hourly, daily, Range


def pseudo_now():
    return datetime(year=2016, month=11, day=24, hour=7, minute=16)


class RangeTests(unittest.TestCase):

    def test_hourly(self):
        self.assertEqual([
            Range(start=datetime(2016, 11, 24, 2, 0), end=datetime(2016, 11, 24, 3, 0)),
            Range(start=datetime(2016, 11, 24, 3, 0), end=datetime(2016, 11, 24, 4, 0)),
            Range(start=datetime(2016, 11, 24, 4, 0), end=datetime(2016, 11, 24, 5, 0)),
            Range(start=datetime(2016, 11, 24, 5, 0), end=datetime(2016, 11, 24, 6, 0)),
            Range(start=datetime(2016, 11, 24, 6, 0), end=datetime(2016, 11, 24, 7, 0))
        ], list(hourly(5, pseudo_now())))

    def test_daily(self):
        self.assertEqual([
            Range(start=datetime(2016, 11, 19, 0, 0), end=datetime(2016, 11, 20, 0, 0)),
            Range(start=datetime(2016, 11, 20, 0, 0), end=datetime(2016, 11, 21, 0, 0)),
            Range(start=datetime(2016, 11, 21, 0, 0), end=datetime(2016, 11, 22, 0, 0)),
            Range(start=datetime(2016, 11, 22, 0, 0), end=datetime(2016, 11, 23, 0, 0)),
            Range(start=datetime(2016, 11, 23, 0, 0), end=datetime(2016, 11, 24, 0, 0))
        ], list(daily(5, pseudo_now())))
