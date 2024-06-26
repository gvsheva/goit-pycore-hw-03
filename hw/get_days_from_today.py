from datetime import datetime


def get_days_from_today(v: str, _today: datetime = datetime.now()):
    """Get the number of days from today to the given date.

    >>> get_days_from_today("2021-01-01", datetime(2021, 1, 1))
    0
    >>> get_days_from_today("2021-01-01", datetime(2021, 1, 2))
    1
    >>> get_days_from_today("2021-01-01", datetime(2020, 12, 31))
    -1
    >>> get_days_from_today("2021-01-01", datetime(2021, 1, 3))
    2
    >>> get_days_from_today("2021-01-01", datetime(2020, 12, 30))
    -2
    >>> get_days_from_today("2021-10-09", datetime(2021, 5, 5))
    -157
    >>> get_days_from_today("xxxxx")
    Traceback (most recent call last):
        ...
    ValueError: Invalid date format
    >>> get_days_from_today(123)
    Traceback (most recent call last):
        ...
    ValueError: Invalid input type
    """
    match v:
        case datetime():
            date = v
        case str():
            try:
                date = datetime.strptime(v, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Invalid date format")
        case _:
            raise ValueError("Invalid input type")
    return (_today - date).days


if __name__ == "__main__":
    import argparse
    import sys
    ap = argparse.ArgumentParser()
    ap.add_argument("date", help="Date in format YYYY-MM-DD")
    args = ap.parse_args()
    try:
        print(get_days_from_today(args.date))
    except ValueError as e:
        print(e, file=sys.stderr)
