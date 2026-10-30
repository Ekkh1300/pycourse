"""
Exercise 4 — Functions
================================================
Run: python exercises/ex04_functions.py

This exercise tests function definition, parameters, and scope.
"""

import sys

# Windows: Console default cp1252 messes with Persian. This fixes it.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")


# ─────────────────────────────────────────────────────────────
# TODO 1 — Simple Function
# Function greet(name) returns "Hello, {name}!"
# ─────────────────────────────────────────────────────────────

def greet(name):
    pass


# ─────────────────────────────────────────────────────────────
# TODO 2 — Default Argument
# Function introduce(name, age, city="Tehran") returns a sentence:
#   "Ali is 25 years old and lives in Tehran."
# If city is not provided, default to "Tehran".
# ─────────────────────────────────────────────────────────────

def introduce(name, age, city="Tehran"):
    pass


# ─────────────────────────────────────────────────────────────
# TODO 3 — Return vs Print
# Function square(x) returns x*x (don't print it).
# Function square_print(x) prints x*x (returns None).
# ─────────────────────────────────────────────────────────────

def square(x):
    pass


def square_print(x):
    pass


# ─────────────────────────────────────────────────────────────
# TODO 4 — Keyword Arguments
# Function describe(name, role="Student", level="Beginner")
# Returns: "Ali (Beginner Student)"
# Try calling with keyword arguments.
# ─────────────────────────────────────────────────────────────

def describe(name, role="Student", level="Beginner"):
    pass


# ─────────────────────────────────────────────────────────────
# TODO 5 — Variable Arguments
# Function total(*args) returns sum of all arguments.
# ─────────────────────────────────────────────────────────────

def total(*args):
    pass


# ─────────────────────────────────────────────────────────────
# TODO 6 — Type Hints
# Function add(a: int, b: int) -> int returns a + b
# Function is_even(n: int) -> bool returns True if n is even
# ─────────────────────────────────────────────────────────────

def add(a, b):
    pass


def is_even(n):
    pass


# ─────────────────────────────────────────────────────────────
# TODO 7 — Scope
# Function increment_counter() uses a counter variable.
# If using global, use global keyword.
# Better: use a mutable default or return the new value.
# ─────────────────────────────────────────────────────────────

counter = 0

def increment_counter():
    pass


# ═════════════════════════════════════════════════════════════
#  Tests — you can modify them for debugging
# ═════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Testing...\n")

    # TODO 1
    assert greet("Ali") == "Hello, Ali!", f"greet('Ali') should be 'Hello, Ali!', got {greet('Ali')!r}"
    assert greet("Sara") == "Hello, Sara!", f"greet('Sara') should be 'Hello, Sara!', got {greet('Sara')!r}"

    # TODO 2
    assert introduce("Ali", 25) == "Ali is 25 years old and lives in Tehran.", f"default city failed: {introduce('Ali', 25)!r}"
    assert introduce("Ali", 25, "Shiraz") == "Ali is 25 years old and lives in Shiraz.", f"custom city failed: {introduce('Ali', 25, 'Shiraz')!r}"

    # TODO 3
    assert square(5) == 25, f"square(5) should be 25, got {square(5)!r}"
    assert square_print(5) is None, "square_print should return None"
    # square_print prints to stdout — that's fine, we just test return value

    # TODO 4
    assert describe("Ali") == "Ali (Beginner Student)", f"default failed: {describe('Ali')!r}"
    assert describe("Ali", "Teacher") == "Ali (Beginner Teacher)", f"role failed: {describe('Ali', 'Teacher')!r}"
    assert describe("Ali", "Developer", "Advanced") == "Ali (Advanced Developer)", f"both failed: {describe('Ali', 'Developer', 'Advanced')!r}"
    # Keyword call test
    assert describe("Ali", level="Advanced", role="Developer") == "Ali (Advanced Developer)", "keyword args should work"

    # TODO 5
    assert total(1, 2, 3) == 6, f"total(1,2,3) should be 6, got {total(1,2,3)!r}"
    assert total() == 0, f"total() should be 0, got {total()!r}"
    assert total(10) == 10, f"total(10) should be 10, got {total(10)!r}"

    # TODO 6
    assert add(2, 3) == 5, f"add(2,3) should be 5, got {add(2,3)!r}"
    assert is_even(4) is True, f"is_even(4) should be True, got {is_even(4)!r}"
    assert is_even(7) is False, f"is_even(7) should be False, got {is_even(7)!r}"

    # TODO 7
    assert increment_counter() == 1, f"first call should return 1, got {increment_counter()!r}"
    assert increment_counter() == 2, f"second call should return 2, got {increment_counter()!r}"

    print("✅ All tests passed!")