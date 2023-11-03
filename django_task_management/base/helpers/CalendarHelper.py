from abc import abstractmethod
from typing import List
import calendar

from datetime import date, timedelta


class CalendarHelper:
    @abstractmethod
    def get_last_day_of_month(year: int, month:int) -> date:
        """
        Get the last day of the month given the
            year and the month
        :param year: int of year
        :param month: int of month
        :return date of the last day
        """
        last_day = calendar.monthrange(year, month)[1]
        return date(year, month, last_day)
    
    @abstractmethod
    def get_next_month(current_date: date) -> str:
        """
        Get the next month iso given current date

        :param current_date: datetime date object
        :return string next month in iso format
        """
        next_month = (current_date.replace(year=current_date.year + 1, month=1, day=1)).isoformat() \
            if current_date.month == 12 else (current_date.replace(month=current_date.month + 1, day=1)).isoformat()
        return next_month

    @abstractmethod
    def get_previous_month(current_date: date) -> str:
        """
        Get the previous month iso given current date

        :param current_date: datetime date object
        :return string prev month in iso format
        """
        prev_month = (current_date.replace(year=current_date.year - 1, month=12, day=1)).isoformat() \
            if current_date.month == 1 else (current_date.replace(month=current_date.month - 1, day=1)).isoformat()
        return prev_month

    @abstractmethod
    def populate_calendar_days_for_month(current_date: date) -> List[date]:
        """
        Create a list of dates of days for
            current month.
        :param current_date: current date
            datetime object
        :return list of dates of days for current month
        """
        last_day_of_month = CalendarHelper.get_last_day_of_month(current_date.year, current_date.month)
        first_day_of_month = date(current_date.year, current_date.month, 1)
        calendar_days: List[date] = []
        day = first_day_of_month
        while day <= last_day_of_month:
            calendar_days.append(day)
            day += timedelta(days=1)
        return calendar_days
