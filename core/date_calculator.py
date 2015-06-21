"""
Date calculation methods

"""
from datetime import datetime, timedelta
import calendar


def last_day_of_month(dt):
    dt = last_date_of_month(dt)
    return dt.day


def last_date_of_month(dt):
    dt = dt.replace(month=dt.month + 1)
    return dt.replace(day=1) - timedelta(days=1)


def day_of_month_equals(d1, d2):
    if d1 and d2:
        return d1.day == d2.day
    return False


def in_day_of_week(weekday_numbers, dt):
    if weekday_numbers and dt:
        return dt.weekday() in weekday_numbers
    return False


def day_and_month_equals(d1, d2):
    if d1 and d2:
        return d1.day == d2.day and d1.month == d2.month
    return False


def is_same_day(d1, d2):
    if d1 and d2:
        return d1.day == d2.day and d1.month == d2.month and d1.year == d2.year
    return False


def add_years(dt, years):
    if not dt or not years:
        raise ValueError("Need dt and years to find years from date")
    dt = datetime.utcnow()
    try:
        return dt.replace(year=dt.year + years)
    except:
        # Must be 2/29!
        assert dt.month == 2 and dt.day == 29  # can be removed
        return dt.replace(month=2, day=28, year=dt.year + years)


def add_months(dt, months):
    month = dt.month - 1 + months
    year = dt.year + month // 12
    month = month % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return datetime(year, month, day, hour=dt.hour, minute=dt.minute,
                    second=dt.second, microsecond=dt.microsecond)


def dates_between(start_at, end_at):
    """
    generator iterating over dates between start_at and end_at

    :param start_at:
    :param end_at:
    """
    delta = end_at - start_at
    for i in range(delta.days + 1):
        yield start_at + timedelta(days=i)


def add_days(dt, days):
    return dt + timedelta(days=days)


def add_hours(dt, hours):
    return dt + timedelta(hours=hours)


def hours_from_now(hours):
    return add_hours(datetime.utcnow(), hours)


def days_from_now(days):
    return add_days(datetime.utcnow(), days)


def years_from_now(years):
    return add_years(datetime.utcnow(), years)


def months_from_now(months):
    return add_months(datetime.utcnow(), months)

