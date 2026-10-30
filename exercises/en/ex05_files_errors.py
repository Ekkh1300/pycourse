"""
Exercise 5 — Files, Error Handling & Modules
================================================
Run: python exercises/ex05_files_errors.py

This exercise tests file I/O, error handling, and module usage.
"""

import sys

# Windows: Console default cp1252 messes with Persian. This fixes it.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")


# ─────────────────────────────────────────────────────────────
# TODO 1 — Write Lines
# Function write_lines(path, lines) writes each line to a file.
# Use with open(..., "w", encoding="utf-8") to create/overwrite file.
# ─────────────────────────────────────────────────────────────

def write_lines(path, lines):
    pass


# ─────────────────────────────────────────────────────────────
# TODO 2 — Read Lines
# Function read_lines(path) returns list of lines (without trailing \\n).
# Use with open(..., "r", encoding="utf-8").
# ─────────────────────────────────────────────────────────────

def read_lines(path):
    pass


# ─────────────────────────────────────────────────────────────
# TODO 3 — Number Conversion
# Function to_int(text) returns integer from text, or None if invalid.
# Use try/except int() for robustness.
# ─────────────────────────────────────────────────────────────

def to_int(text):
    pass


# ─────────────────────────────────────────────────────────────
# TODO 4 — JSON File
# Function load_json(path) loads JSON from file, returns dict or None.
# Use json.load() with encoding="utf-8".
# ─────────────────────────────────────────────────────────────

import json


def load_json(path):
    pass


# ─────────────────────────────────────────────────────────────
# TODO 5 — Error Handling
# Function safe_divide(a, b) returns a/b if b != 0, else None.
# Use try/except to catch ZeroDivisionError.
# ─────────────────────────────────────────────────────────────

def safe_divide(a, b):
    pass


# ─────────────────────────────────────────────────────────────
# TODO 6 — Module Import
# Create a module mymodule.py with function greet(name).
# In this file, import and use it:
#   from mymodule import greet
#   print(greet("Ali"))
# ─────────────────────────────────────────────────────────────

# We'll test this by creating mymodule.py dynamically, or you can create it manually.
# For this exercise, just write the import statement and function call.


# ═════════════════════════════════════════════════════════════
#  Tests — you can modify them for debugging
# ═════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Testing...\n")

    # TODO 1
    # Create a temporary file and check if write_lines works
    # (We'll check file exists and content matches)
    # Note: This is tricky in this file since we can't easily create temp files in tests.
    # Just ensure your function is correct.

    # TODO 2
    # read_lines should return list of lines without \\n
    # Example: read_lines("data.txt") where data.txt contains "line1\\nline2\\n" → ["line1", "line2"]

    # TODO 3
    assert to_int("25") == 25, f"to_int('25') should be 25, got {to_int('25')!r}"
    assert to_int("abc") is None, f"to_int('abc') should be None, got {to_int('abc')!r}"

    # TODO 4
    # load_json should handle missing files gracefully (return None)
    # Note: We can't easily test file loading here without creating files.

    # TODO 5
    assert safe_divide(10, 2) == 5, f"safe_divide(10, 2) should be 5, got {safe_divide(10, 2)!r}"
    assert safe_divide(10, 0) is None, f"safe_divide(10, 0) should be None, got {safe_divide(10, 0)!r}"

    # TODO 5 (additional)
    # You can test module import if you create mymodule.py manually:
    #   from mymodule import greet
    #   assert greet("Ali") == "Hello, Ali!"

    # TODO 6 (if testing module import)
    #   from mymodule import greet
    #   assert greet("Ali") == "Hello, Ali!"

    print("✅ All tests passed!")