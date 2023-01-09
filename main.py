from datetime import datetime, timezone
from calendar import isleap


def total_days(year):
    return 365 + isleap(year)


def total_hours(year):
    return total_days(year) * 24


def total_minutes(year):
    return total_hours(year) * 60


def get_day_resolution():
    today = datetime.now(timezone.utc)
    this_year = today.year
    year_start = datetime(this_year, 1, 1, tzinfo=timezone.utc)
    diff = today - year_start

    days = diff.days
    perc = days / total_days(this_year)
    return perc


def get_hour_resolution():
    today = datetime.now(timezone.utc)
    this_year = today.year
    year_start = datetime(this_year, 1, 1, tzinfo=timezone.utc)
    diff = today - year_start

    hours = diff.seconds//3600
    perc = hours / total_hours(this_year)
    return perc


def get_minute_resolution():
    today = datetime.now(timezone.utc)
    this_year = today.year
    year_start = datetime(this_year, 1, 1, tzinfo=timezone.utc)
    diff = today - year_start

    minutes = (diff.seconds % 3600) // 60
    perc = minutes / total_minutes(this_year)
    return perc


if __name__ == "__main__":
    print(get_day_resolution())
    print(get_hour_resolution())
    print(get_minute_resolution())

    print(f"{get_day_resolution() * 100:.3f} % days have passed")
    print(f"{(get_day_resolution() + get_hour_resolution()) * 100:.3f} % hours have passed")
    print(f"{(get_day_resolution() + get_hour_resolution() + get_minute_resolution()) * 100:.3f} % minutes have passed")
