# Lesson 6 — Object-Oriented Programming (OOP)

> **Goal:** Understand classes, objects, inheritance, and key OOP concepts in Python.

---

## 1. Classes & Objects

A **class** is a blueprint for creating **objects** (instances). Each object has its own state (attributes) and behavior (methods).

### 1.1 Basic Class

```python
class Dog:
    def __init__(self, name, age):
        self.name = name      # Instance attribute
        self.age = age

    def bark(self):
        print(f"{self.name} goes Woof!")

# Create an object (instance):
rex = Dog("Rex", 3)
print(rex.name)      # Rex
rex.bark()           # Rex goes Woof!
```

> **`self`** refers to the current instance. It's always the first parameter of a method, but you **don't pass it** when calling: `rex.bark()`, not `Dog.bark(rex)`.

### 1.2 `__init__` — Constructor

```python
class Dog:
    def __init__(self, name, age=1, breed=None):
        self.name = name
        self.age = age
        self.breed = breed if breed else "Mixed"
```

> **Tip:** `age` and `breed` have defaults, so `Dog("Ali")` works without errors.

### 1.3 Multiple Objects

```python
a = Dog("Ali")
b = Dog("The Dog", 4)
c = Dog("The Dog", 2, "Mixed")
```

Each has its own `name`, `age`, `breed` — they're **independent**.

---

## 2. Instance Attributes vs Class Attributes

```python
class Dog:
    species = "Canine"      # Class attribute (shared by all)

    def __init__(self, name):
        self.name = name     # Instance attribute (unique per dog)
```

```python
d = Dog("Fido")
print(Dog.species)      # "Canine" — accessible via class
print(d.species)        # "Canine" — also via instance
Dog.species = "Wolf"    # Change for all
print(d.species)        # "Wolf" — reflects class change
```

- Class attribute: shared, defined directly in the class body.
- Instance attribute: unique per object, set in `__init__`.

---

## 3. `__str__` vs `__repr__`

Both return a string representation, but for different uses.

### 3.1 `__str__` — "Human readable"

```python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.name} ({self.age} years old)"

    def __repr__(self):
        return f"Dog(name={self.name!r}, age={self.age!r})"
```

```python
d = Dog("Fido", 2)
print(d)            # Fido (2 years old)          ← __str__
print(repr(d))      # Dog(name='Fido', age=2)     ← __repr__
```

- `print(d)` uses `__str__` (or falls back to `__repr__`).
- `repr(d)` or interactive display uses `__repr__`.

### 3.2 `__repr__` — "Developer readable"

Good `__repr__` should be **executable** — if you copy-paste it, it creates the same object:

```python
def __repr__(self):
    return f"Dog(name={self.name!r}, age={self.age!r})"
```

> The `!r` applies `repr()` to the value, giving the quoted string form.

---

## 4. Class Methods (`@classmethod`) and Static Methods (`@staticmethod`)

### 4.1 `@classmethod` — First arg is `cls`

```python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def from_birth_year(cls, name, birth_year, current_year=2026):
        """Create a Dog from birth year instead of age."""
        age = current_year - birth_year
        return cls(name, age)      # cls → Dog class itself

# Usage:
rex = Dog.from_birth_year("Rex", 2020)   # cls is Dog automatically
# rex.age == 6  (2026 - 2020)
```

> **`@classmethod`** receives the class (`Dog`) as first arg (`cls`). Can create instances **without knowing the exact subclass**.

### 4.2 `@staticmethod` — No `self` or `cls`

```python
class Dog:
    @staticmethod
    def is_adult(age):
        return age >= 18

# Usage (no instance or class needed):
print(Dog.is_adult(20))      # True
```

> **`@staticmethod`** is just a function living inside a class namespace — useful for utility helpers.

---

## 5. Inheritance — Reuse & Extend

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f"{self.name} makes a sound.")

    def __str__(self):
        return f"{type(self).__name__} named {self.name}"

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)      # Call Animal.__init__
        self.breed = breed

    def speak(self):                # Override (polymorphism)
        print(f"{self.name}: Woof!")

class Cat(Animal):
    def __init__(self, name, indoor=True):
        super().__init__(name)
        self.indoor = indoor
```

```python
d = Dog("Fido", "Labrador")
d.speak()      # Fido: Woof!   (Dog's version)
print(d)        # Dog named Fido   (Animal's __str__)
```

### 5.1 `super()` — Call Parent's Method

```python
super().__init__(name)      # Call Animal's __init__
```

Useful when you want to extend, not replace, the parent's init.

### 5.2 Override vs Extend

- **Override:** Provide a completely new implementation (`Dog.speak()` replaces `Animal.speak()`).
- **Extend:** Call `super()` first, then add behavior.

---

## 6. Composition (Has-a vs Is-a)

```python
class Engine:
    def __init__(self, horsepower):
        self.horsepower = horsepower

    def start(self):
        return "Engine started!"

class Car:
    def __init__(self, name, engine):
        self.name = name
        self.engine = engine     # Car *has an* Engine

    def drive(self):
        return f"{self.name}: {self.engine.start()}"
```

> **Inheritance (Is-a):** `Dog` *is an* `Animal`.  
> **Composition (Has-a):** `Car` *has an* `Engine`.  
> Prefer composition when you can — it's more flexible and avoids deep inheritance hierarchies.

---

## 7. `@property` — Controlled Attribute Access

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def area(self):
        return self.width * self.height

    @property
    def perimeter(self):
        return 2 * (self.width + self.height)

    @width.setter
    def width(self, value):
        if value <= 0:
            raise ValueError("Width must be positive!")
        self._width = value
```

```python
r = Rectangle(3, 4)
print(r.area)        # 12   (computed, not stored!)
print(r.perimeter)   # 14
```

### 7.1 Setter Validation

The `@width.setter` lets you add checks when someone does `r.width = 5`. Without it, direct assignment `r.width = -1` would silently corrupt data.

### 7.2 `@property` as Getter Only

Just define the getter (no setter) to make an attribute **read-only**:

```python
@property
def computed(self):
    return self.x ** 2
```

Attempting `obj.computed = 10` → `AttributeError: can't set attribute`.

---

## 8. Class Methods & Static Methods Summary

| Decorator | First arg | Typical use |
|---|---|---|
| `@classmethod` | `cls` | Alternative constructors (`from_...`), class-level data |
| `@staticmethod` | None | Utility functions, helpers, pure computation |

---

## 9. Test Cases

```python
# 1. __str__ vs __repr__ difference.
# 2. @classmethod vs @staticmethod distinction.
# 3. super().__init__() in inheritance.
# 4. Composition vs Inheritance choice.
```

---

## 🎯 Exercises for This Lesson

Try them: [`exercises/ex06_oop.py`](../exercises/ex06_oop.py)

```powershell
python exercises/ex06_oop.py
```

---
Next: [Lesson 7](07_advanced_basics.md) — Advanced Basics.