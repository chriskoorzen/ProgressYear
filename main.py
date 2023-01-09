from datetime import datetime
from calendar import isleap

import time
import sched
import threading


class ProgressYear:
    """Class that shows the percentage past of the given date in the year. By default calculates today's percentage.
    A custom datetime object may be passed for calculation.

    No instantiation is necessary to use the class methods - call directly from class.
    """
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
    def get_day_resolution(cls, date: datetime = None):
        if date is None:
            date = datetime.now()
        diff, this_year = cls._get_diff(date)
        days = diff.days
        return days / cls._total_days(this_year)

    @classmethod
    def get_hour_resolution(cls, date: datetime = None):
        if date is None:
            date = datetime.now()
        diff, this_year = cls._get_diff(date)
        hours = diff.seconds // 3600
        return (hours / cls._total_hours(this_year)) + cls.get_day_resolution(date)

    @classmethod
    def get_minute_resolution(cls, date: datetime = None):
        if date is None:
            date = datetime.now()
        diff, this_year = cls._get_diff(date)
        minutes = (diff.seconds % 3600) // 60
        return (minutes / cls._total_minutes(this_year)) + cls.get_hour_resolution(date)


class ProgressYearServer:
    """A variation of the ProgressYear class (but not a subclass) that stores its calculation as a variable. Meant to
    save processing power if expecting lots of queries to the function as a long-running server process. Only returns
    the current time passed as a percentage. This class must create an instance to function properly.

    The class spawns a non-blocking separate thread for updating values, and the user can call its public methods
    at any time to retrieve values. Attempting to call its internal update function will enter an endless blocking
    loop."""

    def __init__(self, update_interval=60):
        # Initialize variables
        self.day_progress = ProgressYear.get_day_resolution()
        self.hour_progress = ProgressYear.get_hour_resolution()
        self.minute_progress = ProgressYear.get_minute_resolution()

        # Create a new scheduler and schedule the _update function every "interval" seconds
        self._scheduler = sched.scheduler(time.time, time.sleep)
        self._scheduler.enter(update_interval, 1, self._update, argument=(update_interval,))

        # Run the scheduler in a separate thread
        self._thread = threading.Thread(target=self._scheduler.run)
        self._thread.daemon = True
        self._thread.start()

    def _update(self, interval):
        # This will run indefinitely within a separate thread.
        while True:
            self.day_progress = ProgressYear.get_day_resolution()
            self.hour_progress = ProgressYear.get_hour_resolution()
            self.minute_progress = ProgressYear.get_minute_resolution()
            time.sleep(interval)

    def get_day_resolution(self):
        return self.day_progress

    def get_hour_resolution(self):
        return self.hour_progress

    def get_minute_resolution(self):
        return self.minute_progress


# Testing
if __name__ == "__main__":
    # print(ProgressYear.get_day_resolution())
    # print(ProgressYear.get_hour_resolution())
    # print(ProgressYear.get_minute_resolution())
    k = ProgressYearServer()
    # static = datetime.now()
    while True:
        print(f"Server class: {k.get_minute_resolution()*100}")
        print(f"Static class: {ProgressYear.get_minute_resolution()*100}")
        print(" --- --- --- ")
        time.sleep(30)
