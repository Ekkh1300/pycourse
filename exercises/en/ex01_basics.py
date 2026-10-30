"""
Exercise 1 — Variables, Data Types & Operators
================================================
Run: python exercises/ex01_basics.py

This exercise tests basic variable assignment and data types.
"""

import sys

# Windows: Console default cp1252 messes with Persian. This fixes it.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")


# ─────────────────────────────────────────────────────────────
# TODO 1 — Simple Variables
# Create variables named:
#   name with string "Ali"
#   age with integer 25
#   height with float 1.75
# ─────────────────────────────────────────────────────────────

name = None
age = None
height = None

# ─────────────────────────────────────────────────────────────
# TODO 2 — Basic Calculations
# Define two numbers 15 and 4 in variables a and b.
# Calculate:
#   sum_ab   = a + b
#   div_ab   = a / b      (floating division)
#   int_div  = a // b
#   mod_ab   = a % b
#   pow_ab   = a ** b
# ─────────────────────────────────────────────────────────────

a = None
b = None
sum_ab = None
div_ab = None
int_div = None
mod_ab = None
pow_ab = None

# ─────────────────────────────────────────────────────────────
# TODO 3 — Type Conversion
# Variable text_number contains "25".
# Convert it to integer and store in number.
# Create variable number_type to store type of number.
# (Hint: use type() function)
# ─────────────────────────────────────────────────────────────

text_number = "25"
number = None
number_type = None

# ─────────────────────────────────────────────────────────────
# TODO 4 — Comparison & Boolean
# Create variable is_adult:
#   True if age >= 18, otherwise False
# (Use comparison operator, not conditional)
# Create variable can_vote identical to is_adult.
# ─────────────────────────────────────────────────────────────

is_adult = None
can_vote = None

# ─────────────────────────────────────────────────────────────
# TODO 5 — f-string
# Create variable greeting using f-string:
#   "Ali is 25 years old"
# (Use name and age variables, not hardcoded)
# ─────────────────────────────────────────────────────────────

greeting = None

# ─────────────────────────────────────────────────────────────
# TODO 6 — Small function
# Function celsius_to_fahrenheit(celsius) returns fahrenheit.
# Formula: F = C * 9/5 + 32
# ─────────────────────────────────────────────────────────────


def celsius_to_fahrenheit(celsius):
    pass  # Write function body


# ═════════════════════════════════════════════════════════════
#  Tests — you can modify them for debugging
# ═════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Testing...\n")

    # TODO 1
    assert name == "Ali", f"name should be 'Ali', got {name!r}"
    assert age == 25, f"age should be 25, got {age!r}"
    assert height == 1.75, f"height should be 1.75, got {height!r}"
    assert isinstance(name, str), "name should be string"
    assert isinstance(age, int), "age should be integer"
    assert isinstance(height, float), "height should be float"

    # TODO 2
    assert sum_ab == 19, f"sum_ab should be 19, got {sum_ab!r}"
    assert div_ab == 3.75, f"div_ab should be 3.75, got {div_ab!r}"
    assert int_div == 3, f"int_div should be 3, got {int_div!r}"
    assert mod_ab == 3, f"mod_ab should be 3, got {mod_ab!r}"
    assert pow_ab == 50625, f"pow_ab should be 50625, got {pow_ab!r}"

    # TODO 3
    assert number == 25, f"number should be 25, got {number!r}"
    assert number_type is int, f"number_type should be int, got {number_type!r}"

    # TODO 4
    assert is_adult is True, "is_adult should be True"
    assert can_vote is True, "can_vote should be True"

    # TODO 5
    assert greeting == "Ali is 25 years old", f"greeting should be 'Ali is 25 years old', got {greeting!r}"

    # TODO 6
    assert celsius_to_fahrenheit(0) == 32, "0°C should be 32°F"
    assert celsius_to_fahrenheit(100) == 212, "100°C should be 212°F"
    assert celsius_to_fahrenheit(37) == 98.6, "37°C should be 98.6°F"

    print("✅ All tests passed!")