"""
Exercise 2 — Conditions & Loops
================================================
Run: python exercises/ex02_control_flow.py

This exercise tests conditional statements and loops.
"""

import sys

# Windows: Console default cp1252 messes with Persian. This fixes it.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")


# ─────────────────────────────────────────────────────────────
# TODO 1 — Number Sign
# Function sign_of(x) returns one of three strings:
#   "positive" if x > 0
#   "zero"     if x == 0
#   "negative" if x < 0
# ─────────────────────────────────────────────────────────────

def sign_of(x):
    pass


# ─────────────────────────────────────────────────────────────
# TODO 2 — Leap Year Checker
# Function is_leap_year(year) returns True for leap years.
# Rules: divisible by 400 → leap.
#          divisible by 100 → NOT leap.
#          divisible by 4  → leap.
#          otherwise NOT leap.
# (Check in order, use and/or)
# ─────────────────────────────────────────────────────────────

def is_leap_year(year):
    pass


# ─────────────────────────────────────────────────────────────
# TODO 3 — Largest of Three
# Function max_of_three(a, b, c) returns the largest.
# Don't use max() — write conditional logic.
# ─────────────────────────────────────────────────────────────

def max_of_three(a, b, c):
    pass


# ─────────────────────────────────────────────────────────────
# TODO 4 — Count Digits
# Function count_digits(n) returns number of digits in n.
# Example: count_digits(12345) → 5
# Note: don't count the sign for negative (use abs())
# Hint: divide by 10 in a loop
# ─────────────────────────────────────────────────────────────

def count_digits(n):
    pass


# ─────────────────────────────────────────────────────────────
# TODO 5 — Sum to N
# Function sum_to(n) returns sum of 1+2+...+n.
# Example: sum_to(5) → 15
# Use a loop (not formula n*(n+1)/2)
# ─────────────────────────────────────────────────────────────

def sum_to(n):
    pass


# ─────────────────────────────────────────────────────────────
# TODO 6 — Factorial
# Function factorial(n) returns n!.
# Example: factorial(5) → 120
# Note: 0! = 1
# ─────────────────────────────────────────────────────────────

def factorial(n):
    pass


# ─────────────────────────────────────────────────────────────
# TODO 7 — FizzBuzz
# Function fizzbuzz(n) returns a string:
#   if n divisible by both 3 and 5 → "FizzBuzz"
#   if only divisible by 3        → "Fizz"
#   if only divisible by 5        → "Buzz"
#   otherwise                     → string of n itself
# (Order matters!)
# ─────────────────────────────────────────────────────────────

def fizzbuzz(n):
    pass


# ═════════════════════════════════════════════════════════════
#  Tests — you can modify them for debugging
# ═════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Testing...\n")

    # TODO 1
    assert sign_of(5) == "positive", f"sign_of(5) should be 'positive', got {sign_of(5)!r}"
    assert sign_of(0) == "zero", f"sign_of(0) should be 'zero', got {sign_of(0)!r}"
    assert sign_of(-3) == "negative", f"sign_of(-3) should be 'negative', got {sign_of(-3)!r}"

    # TODO 2
    assert is_leap_year(2024) is True, "2024 should be a leap year"
    assert is_leap_year(2023) is False, "2023 should not be a leap year"
    assert is_leap_year(1900) is False, "1900 should not be a leap year (century, divisible by 100)"
    assert is_leap_year(2000) is True, "2000 should be a leap year (divisible by 400)"

    # TODO 3
    assert max_of_three(3, 9, 5) == 9, f"max_of_three(3,9,5) should be 9, got {max_of_three(3,9,5)}"
    assert max_of_three(-2, -5, -1) == -1, "should work with all negative numbers"
    assert max_of_three(4, 4, 4) == 4, "should work when all equal"

    # TODO 4
    assert count_digits(12345) == 5, f"count_digits(12345) should be 5, got {count_digits(12345)}"
    assert count_digits(0) == 1, f"count_digits(0) should be 1, got {count_digits(0)}"
    assert count_digits(-987) == 3, f"count_digits(-987) should be 3 (ignore sign), got {count_digits(-987)}"

    # TODO 5
    assert sum_to(5) == 15, f"sum_to(5) should be 15, got {sum_to(5)}"
    assert sum_to(1) == 1, f"sum_to(1) should be 1, got {sum_to(1)}"
    assert sum_to(10) == 55, f"sum_to(10) should be 55, got {sum_to(10)}"

    # TODO 6
    assert factorial(5) == 120, f"factorial(5) should be 120, got {factorial(5)}"
    assert factorial(0) == 1, f"factorial(0) should be 1, got {factorial(0)}"
    assert factorial(1) == 1, f"factorial(1) should be 1, got {factorial(1)}"

    # TODO 7
    assert fizzbuzz(15) == "FizzBuzz", "fizzbuzz(15) should be 'FizzBuzz'"
    assert fizzbuzz(3) == "Fizz", "fizzbuzz(3) should be 'Fizz'"
    assert fizzbuzz(5) == "Buzz", "fizzbuzz(5) should be 'Buzz'"
    assert fizzbuzz(7) == "7", f"fizzbuzz(7) should be '7', got {fizzbuzz(7)!r}"

    print("✅ All tests passed!")