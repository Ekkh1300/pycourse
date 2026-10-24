# پاسخ تمرین ۳ — لیست، تاپل، دیکشنری و ست
# نکته‌ی کلیدی: برای برش، اندیس دوم شامل نمی‌شود؛ و برای داده‌ی تودرتو از .get استفاده کن.

numbers = [12, 7, 25, 3, 18]
biggest = max(numbers)
smallest = min(numbers)
total = sum(numbers)
evens = sum(1 for n in numbers if n % 2 == 0)
doubled = [n * 2 for n in numbers]

first_two = numbers[:2]
last_two = numbers[-2:]
reversed_list = numbers[::-1]

student = {"name": "سارا", "age": 21, "grades": [85, 90, 78]}
average = sum(student["grades"]) / len(student["grades"])
highest = max(student["grades"])
info = f"{student['name']}: {student['age']}"
summary = {"name": student["name"], "average": average}

a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7}
union = a | b
intersection = a & b
difference = a - b

raw = [1, 2, 2, 3, 3, 3, 4, 4, 5]
seen = set()
repeated = set()
duplicates = []
for item in raw:
    if item in seen:
        if item not in repeated:
            repeated.add(item)
            duplicates.append(item)
    else:
        seen.add(item)


def word_count(text):
    counts = {}
    for word in text.split():
        counts[word] = counts.get(word, 0) + 1
    return counts


def even_squares(numbers):
    return [n * n for n in numbers if n % 2 == 0]
