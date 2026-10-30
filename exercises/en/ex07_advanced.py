"""
Exercise 7 — Advanced Basics
================================================
Run: python exercises/ex07_advanced.py

This exercise tests advanced Python features.
"""

import sys

# Windows: Console default cp1252 messes with Persian. This fixes it.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")


# ─────────────────────────────────────────────────────────────
# TODO 1 — List Comprehension
# Given numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# Create:
#   squares      = [n*n for n in numbers]
#   evens        = [n for n in numbers if n % 2 == 0]
#   evens_squared = [n*n for n in numbers if n % 2 == 0]
# ─────────────────────────────────────────────────────────────
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squares = None
evens = None
evens_squared = None


# ─────────────────────────────────────────────────────────────
# TODO 2 — Dict Comprehension
# Given words = ["apple", "banana", "cherry", "date"]
# Create: word_lengths = {word: len(word) for word in words}
# ─────────────────────────────────────────────────────────────
words = ["apple", "banana", "cherry", "date"]
word_lengths = None


# ─────────────────────────────────────────────────────────────
# TODO 3 — lambda with map/filter
# Given numbers = [1, 2, 3, 4, 5]
# Use map to create doubled = [2, 4, 6, 8, 10]
# Use filter to create greater_than_3 = [4, 5]
# ─────────────────────────────────────────────────────────────
numbers = [1, 2, 3, 4, 5]
doubled = None
greater_than_3 = None


# ─────────────────────────────────────────────────────────────
# TODO 4 — enumerate and zip
# Given names = ["Ali", "Sara", "Reza"]
# ages = [25, 30, 22]
# Create:
#   indexed_names = list(enumerate(names, start=1))
#   paired = list(zip(names, ages))
# ─────────────────────────────────────────────────────────────
names = ["Ali", "Sara", "Reza"]
ages = [25, 30, 22]
indexed_names = None
paired = None


# ─────────────────────────────────────────────────────────────
# TODO 5 — Sorting with key
# Given users = [{"name": "Ali", "age": 25}, {"name": "Sara", "age": 30}, {"name": "Reza", "age": 22}]
# Sort by age ascending, store in by_age
# Sort by name descending, store in by_name_desc
# ─────────────────────────────────────────────────────────────
users = [{"name": "Ali", "age": 25}, {"name": "Sara", "age": 30}, {"name": "Reza", "age": 22}]
by_age = None
by_name_desc = None


# ─────────────────────────────────────────────────────────────
# TODO 6 — Decorator
# Create a timer decorator that prints function name and elapsed time.
# Use functools.wraps to preserve metadata.
# ─────────────────────────────────────────────────────────────
import time
import functools


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        pass
    return wrapper


# ─────────────────────────────────────────────────────────────
# TODO 7 — pathlib
# Using pathlib.Path, create a file "test.txt" in a folder "data"
# Write "Hello World" to it, then read it back.
# ─────────────────────────────────────────────────────────────
from pathlib import Path


def write_and_read():
    pass


# ═════════════════════════════════════════════════════════════
#  Tests — you can modify them for debugging
# ═════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Testing...\n")

    # TODO 1
    assert squares == [1, 4, 9, 16, 25, 36, 49, 64, 81, 100], f"squares failed: {squares!r}"
    assert evens == [2, 4, 6, 8, 10], f"evens failed: {evens!r}"
    assert evens_squared == [4, 16, 36, 64, 100], f"evens_squared failed: {evens_squared!r}"

    # TODO 2
    assert word_lengths == {"apple": 5, "banana": 6, "cherry": 6, "date": 4}, f"word_lengths failed: {word_lengths!r}"

    # TODO 3
    assert doubled == [2, 4, 6, 8, 10], f"doubled failed: {doubled!r}"
    assert greater_than_3 == [4, 5], f"greater_than_3 failed: {greater_than_3!r}"

    # TODO 4
    assert indexed_names == [(1, "Ali"), (2, "Sara"), (3, "Reza")], f"indexed_names failed: {indexed_names!r}"
    assert paired == [("Ali", 25), ("Sara", 30), ("Reza", 22)], f"paired failed: {paired!r}"

    # TODO 5
    assert by_age == [{"name": "Reza", "age": 22}, {"name": "Ali", "age": 25}, {"name": "Sara", "age": 30}], f"by_age failed: {by_age!r}"
    assert by_name_desc == [{"name": "Sara", "age": 30}, {"name": "Reza", "age": 22}, {"name": "Ali", "age": 25}], f"by_name_desc failed: {by_name_desc!r}"

    # TODO 6
    @timer
    def test_func():
        time.sleep(0.01)
        return 42

    result = test_func()
    assert result == 42, f"decorator should preserve return value, got {result!r}"

    # TODO 7
    content = write_and_read()
    assert content == "Hello World", f"pathlib read failed: {content!r}"

    print("✅ All tests passed!")