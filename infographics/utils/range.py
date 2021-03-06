import datetime

import pytz

from collections import namedtuple

Range = namedtuple("Range", ("start", "end"))


def get_ranges(step, number_of_steps, end_limit):
    """
    :param step: timedelta specifying partitioning for the
    :param number_of_steps: number of steps to go backward in time
    :param end_limit: the end date for the range sequence

    :return: a generator over date Ranges
    """
    start = end_limit - (step * number_of_steps)

    cursor = pytz.UTC.localize(start)
    for i in range(number_of_steps):
        previous_cursor = cursor
        cursor += step
        yield Range(previous_cursor, cursor)


def hourly(number_of_hours, end_limit):
    """
    Generate ranges of full hours up until now. I.e. current hour is excluded from the set since it is incomplete.

    :param number_of_hours: see number_of_steps in get_ranges
    :param end_limit: see get_ranges
    :return: see get_ranges
    """
    end_limit = datetime.datetime(
        day=end_limit.day, month=end_limit.month, year=end_limit.year, hour=end_limit.hour) - datetime.timedelta(hours=1)
    return get_ranges(datetime.timedelta(hours=1), number_of_hours, end_limit)
