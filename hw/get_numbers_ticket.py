import random


def get_numbers_ticket(min: int, max: int, quantity: int, _seed: int | None = None):
    """Get a list of random numbers within the given range.

    >>> get_numbers_ticket(1, 10, 5, 0)
    [1, 3, 5, 7, 10]
    >>> get_numbers_ticket(1, 1000, 10, 0)
    [42, 266, 395, 431, 498, 524, 777, 865, 912, 989]
    >>> get_numbers_ticket(1, 10, 10)
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    >>> get_numbers_ticket(0, 10, 5)
    []
    >>> get_numbers_ticket(1, 1001, 5)
    []
    >>> get_numbers_ticket(1, 10, 11)
    []
    >>> for _ in range(100):
    ...     assert len(set(get_numbers_ticket(1, 1000, 50))) == 50
    """
    if min < 1:
        return []
    if max > 1000:
        return []
    if min >= max:
        return []
    if quantity > max - min + 1:
        return []
    r = random.Random(_seed)
    return sorted(r.sample(range(min, max + 1), quantity))


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("min", type=int, help="Minimum number")
    ap.add_argument("max", type=int, help="Maximum number")
    ap.add_argument("quantity", type=int, help="Quantity of numbers")
    ap.add_argument("--seed", type=int, help="Random seed")
    args = ap.parse_args()
    print(get_numbers_ticket(args.min, args.max, args.quantity, args.seed))
