import sys


def show_progress(percentage, bars=25):
    sys.stdout.write("\r")
    percents_per_bar = (100 / bars)
    number_of_bars = int(percentage / percents_per_bar)
    sys.stdout.write("[%-{}s] %d%%".format(bars) % ('=' * number_of_bars, int(percentage)))
