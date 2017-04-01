import datetime

import pytz

from collections import namedtuple

Range = namedtuple("Range", ("start", "end"))


def get_ranges(step, number_of_steps, end_limit_function):
    """
    :param step: timedelta specifying partitioning for the
    :param number_of_steps: number of steps to go backward in time
    :param end_limit_function: function generating returning the end date for the range sequence

    :return: a generator over date Ranges
    """
    start = end_limit_function() - (step * number_of_steps)

    cursor = pytz.UTC.localize(start)
    for i in range(number_of_steps):
        previous_cursor = cursor
        cursor += step
        yield Range(previous_cursor, cursor)


def hourly(number_of_hours, end_limit_function=None):
    """
    Generate ranges of full hours up until now. I.e. current hour is excluded from the set since it is incomplete.

    :param number_of_hours: see number_of_steps in get_ranges
    :param end_limit_function: see get_ranges
    :return: see get_ranges
    """
    end_limit_function = end_limit_function or datetime.datetime.now

    def _get_closest_full_hour():
        now = end_limit_function()
        return datetime.datetime(day=now.day, month=now.month, year=now.year, hour=now.hour)

    return get_ranges(datetime.timedelta(hours=1), number_of_hours, _get_closest_full_hour)


def daily(number_of_days, end_limit_function=None):
    """
    Generate ranges of full days up until today. I.e. current day is excluded from the set since it is incomplete.

    :param number_of_days: see number_of_steps in get_ranges
    :param end_limit_function: see get_ranges
    :return: see get_ranges
    """
    end_limit_function = end_limit_function or datetime.datetime.now

    def _get_closest_full_day():
        now = end_limit_function()
        return datetime.datetime(day=now.day, month=now.month, year=now.year)

    return get_ranges(datetime.timedelta(days=1), number_of_days, _get_closest_full_day)
