# پاسخ تمرین ۷ — ابزارهای حرفه‌ای
# نکته‌ی کلیدی: برای دکوریتور از functools.wraps استفاده کن و برای شمارنده از nonlocal.

import functools
from functools import reduce


def squares_under(n):
    return [i * i for i in range(n) if i % 2 == 0]


def invert_dict(d):
    return {value: key for key, value in d.items()}


def pair_with_index(items):
    return list(enumerate(items, start=1))


def sort_by_length(words):
    return sorted(words, key=lambda word: (len(word), word))


def stats(numbers):
    if not numbers:
        return (0, 0, 0, 0)
    total = reduce(lambda acc, n: acc + n, numbers, 0)
    average = total / len(numbers)
    return (total, average, max(numbers), min(numbers))


def repeat(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(times):
                result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


def make_counter():
    count = 0

    def counter():
        nonlocal count
        count += 1
        return count

    return counter
