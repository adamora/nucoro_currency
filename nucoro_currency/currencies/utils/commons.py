import datetime
import random
import typing


def get_dates_between_dates(start_date: datetime.date, end_date: datetime.date) -> typing.List[datetime.date]:
    assert start_date < end_date
    delta = end_date - start_date
    return [start_date + datetime.timedelta(days=i) for i in range(delta.days + 1)]


def twr_formula(initial_rate, final_rate, amount, input=0, refund=0):
    initial_value = amount * initial_rate
    final_value = amount * final_rate
    return (final_value - initial_value + refund - input) / initial_value


def random_color():
    return f"#{''.join([random.choice('0123456789ABCDEF') for j in range(6)])}"
