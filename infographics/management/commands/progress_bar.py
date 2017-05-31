import sys


def show_progress(current, total, bars=25):
    percentage = (current / total) * 100
    sys.stdout.write("\r")
    percents_per_bar = (100 / bars)
    number_of_bars = int(percentage / percents_per_bar)
    sys.stdout.write("[%-{}s] %d%%".format(bars) % ('=' * number_of_bars, int(percentage)))
