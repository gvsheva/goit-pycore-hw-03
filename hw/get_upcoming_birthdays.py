from datetime import date, datetime, timedelta
from typing import Hashable, Iterable


def _get_congratulation_date(birthdate: date, _current_year: int):
    """Get the next birthday date for the given birthdate.
    >>> _get_congratulation_date(date(1985, 1, 23), 2024)
    datetime.date(2024, 1, 23)
    >>> _get_congratulation_date(date(1985, 6, 29), 2024)
    datetime.date(2024, 7, 1)
    >>> _get_congratulation_date(date(1985, 6, 30), 2024)
    datetime.date(2024, 7, 1)
    """
    birthday = date(_current_year, birthdate.month, birthdate.day)
    weekday = birthday.weekday()
    if 0 <= weekday < 5:
        return birthday
    return date(_current_year, birthdate.month, birthday.day) + timedelta(days=(7 - weekday))


def _get_upcoming_birthdays(
        users: Iterable[dict[str, str]],
        _days: int = 7,
        _current_date: date = date.today(),
):
    for user in users:
        match user:
            case {"name": name, "birthday": birthday}:
                try:
                    birthdate = datetime.strptime(birthday, "%Y.%m.%d")
                except ValueError:
                    raise ValueError("Invalid date format")
                congratulation_date = _get_congratulation_date(
                    birthdate.date(), _current_date.year)
                if congratulation_date < _current_date:
                    continue
                if congratulation_date - _current_date <= timedelta(days=_days):
                    if congratulation_date.weekday() == _current_date.weekday():
                        notes = "today"
                    elif congratulation_date.weekday() > _current_date.weekday():
                        notes = f"on {congratulation_date.strftime('%A')}"
                    else:
                        notes = f"on next {congratulation_date.strftime('%A')}"
                    yield {
                        "name": name,
                        "congratulation_date": congratulation_date.strftime("%Y.%m.%d"),
                        "_notes": notes,
                    }
            case _:
                raise ValueError("Invalid user format")


def _omit(d: dict, *keys: Hashable):
    return {k: v for k, v in d.items() if k not in keys}


def get_upcoming_birthdays(
        users: Iterable[dict[str, str]],
        _days: int = 7,
        _current_date: date = date.today(),
):
    """Get upcoming birthdays for the next `_days` days.

    >>> users = [
    ... {"name": "John Doe", "birthday": "1985.01.23"},
    ... {"name": "Jane Smith", "birthday": "1990.01.27"},
    ... ]
    >>> current_date = date(2024, 1, 22)
    >>> for user in get_upcoming_birthdays(users, 7, current_date):
    ...     print(user)
    {'name': 'John Doe', 'congratulation_date': '2024.01.23'}
    {'name': 'Jane Smith', 'congratulation_date': '2024.01.29'}

    >>> current_date = date(2024, 6, 26)
    >>> users = [
    ... {"name": "Blackbeard Teach", "birthday": "1680.06.28"},
    ... {"name": "Anne Bonny", "birthday": "1697.06.29"},
    ... {"name": "Calico Jack Rackham", "birthday": "1682.06.30"},
    ... {"name": "Charles Vane", "birthday": "1680.07.01"},
    ... {"name": "Mary Read", "birthday": "1695.07.02"},
    ... {"name": "Edward England", "birthday": "1683.02.09"},
    ... {"name": "Bartholomew Roberts", "birthday": "1682.05.17"},
    ... {"name": "Henry Morgan", "birthday": "1635.01.24"},
    ... {"name": "Samuel Bellamy", "birthday": "1689.02.23"},
    ... {"name": "Stede Bonnet","birthday": "1688.07.29"},
    ... ]

    >>> for user in get_upcoming_birthdays(users, 7, current_date):
    ...     print(user)
    {'name': 'Blackbeard Teach', 'congratulation_date': '2024.06.28'}
    {'name': 'Anne Bonny', 'congratulation_date': '2024.07.01'}
    {'name': 'Calico Jack Rackham', 'congratulation_date': '2024.07.01'}
    {'name': 'Charles Vane', 'congratulation_date': '2024.07.01'}
    {'name': 'Mary Read', 'congratulation_date': '2024.07.02'}

    """
    return list(_omit(u, "_notes") for u in _get_upcoming_birthdays(users, _days, _current_date))


if __name__ == "__main__":
    import argparse
    import json
    import sys
    ap = argparse.ArgumentParser()
    ap.add_argument("users_db_json",
                    type=argparse.FileType("r"),
                    help="Users database JSON file")
    ap.add_argument("--days",
                    type=int,
                    default=7,
                    help="Days to check")
    args = ap.parse_args()
    try:
        users = json.load(args.users_db_json)
        for user in _get_upcoming_birthdays(users, args.days):
            print(
                f"{user['name']:<20} {user['congratulation_date']:>10} ({user['_notes']})")
    except json.JSONDecodeError:
        print("Invalid JSON", file=sys.stderr)
        sys.exit(1)
