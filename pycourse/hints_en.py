"""
English hints for exercises.

Each key is an exercise ID and the value is a list of hints (level 1, 2, 3...).
Also includes GENERAL_HINTS that apply across exercises.
"""

from __future__ import annotations

HINTS: dict[str, list[str]] = {
    "ex01_basics": [
        "To add two numbers: `a + b`.",
        "To exponentiate: `a ** b`.",
        "The function `celsius_to_fahrenheit` should `return` the result.",
        "`celsius * 9 / 5 + 32`",
    ],
    "ex02_control_flow": [
        "Use `if/elif/else` for conditions.",
        "Remember `and`, `or`, `not` operators.",
        "For `count_digits`: convert the number to strings and count, "
        "or use `len(str(number))`.",
    ],
    "ex03_collections": [
        "To filter evens: `sum(1 for n in numbers if n % 2 == 0)`.",
        "To double each: `[n * 2 for n in numbers]`.",
        "To compute average: `sum(numbers) / len(numbers)`.",
        "Use `float()` if you need decimal division.",
    ],
    "ex04_functions": [
        "To define a function: `def f(a, b=2):`.",
        "For `min_max`: `return (min(a, b), max(a, b))`.",
        "For `average` with `*numbers`: `sum(numbers) / len(numbers)`.",
        "If `bucket` is None: `bucket = []`.",
    ],
    "ex05_files_errors": [
        "To write: `with open(path, \"w\", encoding=\"utf-8\") as f:\\n` `f.write(line + \"\\n\")`.",
        "To read lines: `try:\\n    lines = open(path).readlines()\\n except FileNotFoundError:\\n    lines = []`.",
        "For `to_int`: `try: return int(text) except ValueError: return None`.",
    ],
    "ex06_oop": [
        "`self` is the instance. Define as `def bark(self):`.",
        "`property` uses `@property`. For `x`: `@property` and `@x.setter`.",
        "For `SavingsAccount`: `super().__init__(owner, balance)`.",
        "Then define your own method, e.g. `deposit(amount)`.",
    ],
    "ex07_advanced": [
        "For `squares_under`: comprehension `[i ** 2 for i in range(n) if i % 2 == 0]`.",
        "For `invert_dict`: `for k, v in d.items():` then build new dict.",
        "For `wrapper`: define a function that takes another function and returns a wrapper.",
    ],
}

GENERAL_HINTS = [
    "Or use `print(type(x))` followed by `print(repr(x))` to see the exact type and value.",
    "If the result is `None`, check that you have a `return` statement.",
    "Pay attention to types: `3` and `3.0` are different.",
]