"""
First Steps — Your First Python Program
========================================
Run: python projects/first_steps.py

This is your first real exercise. You'll write a simple Python program
that uses variables, print, f-strings, and input().
"""

import sys

# Windows: Console default cp1252 messes with Persian. This fixes it.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")


# ─────────────────────────────────────────────────────────────
# TODO 1 — Variables
# Create variables:
#   name with string "Ali"
#   age with integer 25
#   height with float 1.75
# Print them using print and f-strings.
# ─────────────────────────────────────────────────────────────

name = ...
age = ...
height = ...

print(f"Name: {name}")
print(f"Age: {age}")
print(f"Height: {height}")

# ─────────────────────────────────────────────────────────────
# TODO 2 — Math Operations
# Calculate:
#   sum_ab = 15 + 4
#   div_ab = 15 / 4      (floating division)
#   int_div = 15 // 4
#   mod_ab = 15 % 4
#   pow_ab = 15 ** 4
# ─────────────────────────────────────────────────────────────

sum_ab = ...
div_ab = ...
int_div = ...
mod_ab = ...
pow_ab = ...

print(f"Sum: {sum_ab}")
print(f"Division: {div_ab}")
print(f"Integer division: {int_div}")
print(f"Modulo: {mod_ab}")
print(f"Power: {pow_ab}")

# ─────────────────────────────────────────────────────────────
# TODO 3 — Input & Type Conversion
# Read integer and float from user.
# Remember: input() always returns string!
# Use int() and float() for conversion.
# ─────────────────────────────────────────────────────────────

user_name = input("Enter your name: ")
user_age = int(input("Enter your age: "))
user_height = float(input("Enter your height (meters): "))

print(f"Hello, {user_name}! You are {user_age} years old and {user_height}m tall.")

# ─────────────────────────────────────────────────────────────
# TODO 4 — Simple Function
# Write a function celsius_to_fahrenheit(celsius) that converts Celsius to Fahrenheit.
# Formula: F = C * 9/5 + 32
# ─────────────────────────────────────────────────────────────

def celsius_to_fahrenheit(celsius):
    ...

# Test it
print(f"0°C = {celsius_to_fahrenheit(0)}°F")
print(f"100°C = {celsius_to_fahrenheit(100)}°F")