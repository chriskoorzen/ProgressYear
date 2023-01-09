from datetime import datetime
from calendar import isleap


class ProgressYear:

    @staticmethod
    def _total_days(year):
        return 365 + isleap(year)

    @staticmethod
    def _total_hours(year):
        return ProgressYear._total_days(year) * 24

    @staticmethod
    def _total_minutes(year):
        return ProgressYear._total_hours(year) * 60

    @staticmethod
    def _get_diff(date: datetime):
        date = date.replace(tzinfo=None)
        this_year = date.year
        year_start = datetime(this_year, 1, 1)
        diff = date - year_start
        return diff, this_year

    @classmethod
    def get_day_resolution(cls, date: datetime = datetime.now()):
        diff, this_year = cls._get_diff(date)
        days = diff.days
        return days / cls._total_days(this_year)

    @classmethod
    def get_hour_resolution(cls, date: datetime = datetime.now()):
        diff, this_year = cls._get_diff(date)
        hours = diff.seconds // 3600
        return (hours / cls._total_hours(this_year)) + cls.get_day_resolution(date)

    @classmethod
    def get_minute_resolution(cls, date: datetime = datetime.now()):
        diff, this_year = cls._get_diff(date)
        minutes = (diff.seconds % 3600) // 60
        return (minutes / cls._total_minutes(this_year)) + cls.get_hour_resolution(date)


if __name__ == "__main__":
    print(ProgressYear.get_day_resolution())
    print(ProgressYear.get_hour_resolution())
    print(ProgressYear.get_minute_resolution())

