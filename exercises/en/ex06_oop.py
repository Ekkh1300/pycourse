"""
Exercise 6 — Object-Oriented Programming
================================================
Run: python exercises/ex06_oop.py

This exercise tests classes, inheritance, and OOP concepts.
"""

import sys

# Windows: Console default cp1252 messes with Persian. This fixes it.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")


# ─────────────────────────────────────────────────────────────
# TODO 1 — Basic Class
# Class Rectangle with width and height attributes.
# Methods: area(), perimeter()
# ─────────────────────────────────────────────────────────────

class Rectangle:
    def __init__(self, width, height):
        pass

    def area(self):
        pass

    def perimeter(self):
        pass


# ─────────────────────────────────────────────────────────────
# TODO 2 — __str__ and __repr__
# Add __str__ and __repr__ to Rectangle:
#   __str__: "Rectangle(width=3, height=4)"
#   __repr__: "Rectangle(width=3, height=4)"  (same, evaluable)
# ─────────────────────────────────────────────────────────────

# Modify the Rectangle class above


# ─────────────────────────────────────────────────────────────
# TODO 3 — Inheritance
# Class Square inherits from Rectangle.
# __init__ takes only one argument (side) and calls super().__init__(side, side).
# ─────────────────────────────────────────────────────────────

class Square(Rectangle):
    def __init__(self, side):
        pass


# ─────────────────────────────────────────────────────────────
# TODO 4 — Class Method
# Class Point with x, y coordinates.
# @classmethod from_origin(cls) returns Point(0, 0)
# @classmethod from_coords(cls, x, y) returns Point(x, y)
# ─────────────────────────────────────────────────────────────

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def from_origin(cls):
        pass

    @classmethod
    def from_coords(cls, x, y):
        pass


# ─────────────────────────────────────────────────────────────
# TODO 5 — Static Method
# Class Math with @staticmethod add(a, b) and multiply(a, b)
# ─────────────────────────────────────────────────────────────

class Math:
    @staticmethod
    def add(a, b):
        pass

    @staticmethod
    def multiply(a, b):
        pass


# ─────────────────────────────────────────────────────────────
# TODO 6 — Property
# Class Circle with radius.
# Property area (read-only) returns π * r² (use math.pi)
# Property diameter (read-only) returns 2 * r
# ─────────────────────────────────────────────────────────────

import math


class Circle:
    def __init__(self, radius):
        pass

    @property
    def area(self):
        pass

    @property
    def diameter(self):
        pass


# ─────────────────────────────────────────────────────────────
# TODO 7 — Composition
# Class Engine with horsepower.
# Class Car with name and engine (composition: Car HAS an Engine).
# Car.drive() returns "CarName: Engine started with X HP!"
# ─────────────────────────────────────────────────────────────

class Engine:
    def __init__(self, horsepower):
        pass

    def start(self):
        pass


class Car:
    def __init__(self, name, engine):
        pass

    def drive(self):
        pass


# ═════════════════════════════════════════════════════════════
#  Tests — you can modify them for debugging
# ═════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Testing...\n")

    # TODO 1
    r = Rectangle(3, 4)
    assert r.area() == 12, f"area should be 12, got {r.area()!r}"
    assert r.perimeter() == 14, f"perimeter should be 14, got {r.perimeter()!r}"

    # TODO 2
    assert str(r) == "Rectangle(width=3, height=4)", f"__str__ failed: {str(r)!r}"
    assert repr(r) == "Rectangle(width=3, height=4)", f"__repr__ failed: {repr(r)!r}"

    # TODO 3
    s = Square(5)
    assert s.area() == 25, f"Square area should be 25, got {s.area()!r}"
    assert s.perimeter() == 20, f"Square perimeter should be 20, got {s.perimeter()!r}"

    # TODO 4
    p1 = Point.from_origin()
    assert (p1.x, p1.y) == (0, 0), f"from_origin failed: ({p1.x}, {p1.y})"
    p2 = Point.from_coords(3, 4)
    assert (p2.x, p2.y) == (3, 4), f"from_coords failed: ({p2.x}, {p2.y})"

    # TODO 5
    assert Math.add(2, 3) == 5, f"Math.add(2,3) should be 5, got {Math.add(2,3)!r}"
    assert Math.multiply(4, 5) == 20, f"Math.multiply(4,5) should be 20, got {Math.multiply(4,5)!r}"

    # TODO 6
    c = Circle(3)
    assert abs(c.area - 28.274333882308138) < 0.0001, f"Circle area failed: {c.area}"
    assert c.diameter == 6, f"Circle diameter failed: {c.diameter}"

    # TODO 7
    e = Engine(150)
    assert e.start() == "Engine started with 150 HP!", f"Engine.start failed: {e.start()!r}"
    car = Car("Tesla", e)
    assert car.drive() == "Tesla: Engine started with 150 HP!", f"Car.drive failed: {car.drive()!r}"

    print("✅ All tests passed!")