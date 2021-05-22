import datetime
import typing


def get_dates_between_dates(start_date: datetime.date, end_date: datetime.date) -> typing.List[datetime.date]:
    assert start_date < end_date
    delta = end_date - start_date
    return [start_date + datetime.timedelta(days=i) for i in range(delta.days + 1)]
