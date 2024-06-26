import re


def normalize_phone(phone: str, country_code: str = "+380"):
    """Normalize phone number to the international format.

    >>> cases = [
    ... "067\\t123 4567",
    ... "(095) 234-5678\\n",
    ... "+380 44 123 4567",
    ... "380501234567",
    ... "    +38(050)123-32-34",
    ... "     0503451234",
    ... "(050)8889900",
    ... "38050-111-22-22",
    ... "38050 111 22 11   ",
    ... "991234567",
    ... ]
    >>> for case in cases:
    ...     print(normalize_phone(case))
    +380671234567
    +380952345678
    +380441234567
    +380501234567
    +380501233234
    +380503451234
    +380508889900
    +380501112222
    +380501112211
    +380991234567
    """
    phone = re.sub(r"\D", "", phone)
    local = f"{phone[-9:]:0>9}"
    return f"{country_code}{local}"


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("data_file", type=argparse.FileType("r"), default="-",
                    help="Data file or `-` for STDIN")
    ap.add_argument("--country-code", default="+380", help="Country code")
    args = ap.parse_args()
    for line in args.data_file:
        print(normalize_phone(line.strip(), args.country_code))
