# پاسخ تمرین ۴ — توابع
# نکته‌ی کلیدی: هرگز مقدار پیش‌فرضِ لیست نگذار؛ همیشه None بگذار و خودت بساز.

def greet(name):
    return f"سلام {name}!"


def introduce(name, age, city="تهران"):
    return f"{name} {age} ساله و در {city} زندگی می‌کند."


def min_max(numbers):
    return (min(numbers), max(numbers))


def average(*numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)


def build_profile(**kwargs):
    return {
        "name": kwargs.get("name", "نامشخص"),
        "age": kwargs.get("age", "نامشخص"),
        "role": kwargs.get("role", "نامشخص"),
    }


def add_item(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket


def calculate_stats(numbers):
    lo, hi = min_max(numbers)
    return {
        "sum": sum(numbers),
        "min": lo,
        "max": hi,
        "average": sum(numbers) / len(numbers),
        "count": len(numbers),
    }


def divide(a, b):
    if b == 0:
        raise ValueError("division by zero")
    return a / b
