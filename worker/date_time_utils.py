from enum import Enum


class TimeUnit(Enum):
    SECOND = 1
    MINUTE = 60
    HOUR = 3600
    DAY = 86400
    WEEK = 604800


class SecondsPeriodBuilder:
    _seconds = 0

    def __init__(self, seconds=0):
        self._seconds = seconds

    def build(self):
        return self._seconds

    def add_minutes(self, minutes: int):
        return SecondsPeriodBuilder(self._seconds + minutes * TimeUnit.MINUTE.value)

    def add_hours(self, hours: int):
        return SecondsPeriodBuilder(self._seconds + hours * TimeUnit.HOUR.value)

    def add_days(self, days: int):
        return SecondsPeriodBuilder(self._seconds + days * TimeUnit.DAY.value)

    def add_weeks(self, weeks: int):
        return SecondsPeriodBuilder(self._seconds + weeks * TimeUnit.WEEK.value)
