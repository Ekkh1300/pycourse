# Lesson 1 — Variables, Types & Operators

> **Goal:** Store values in variables, understand Python's basic data types, and use operators to compute.

---

## 1. Variables

A variable is a named reference to a value:

```python
age = 25          # integer 25 → variable named "age"
message = "Hello"
```

> **Note:** `=` is **assignment**, not equality. `age = 25` means "bind the name `age` to the value `25`".  
> Equality is `==` (covered below).

### 1.1 Naming Rules (PEP 8)

```python
user_name = "Ali"      # snake_case for variables
USER_LIMIT = 10        # UPPER_CASE for constants
class_name = "Car"     # PascalCase for classes
```

Avoid:
- Starting with a digit: `2name` ❌
- Spaces: `my name` ❌
- Reserved keywords: `class`, `if`, `for` ❌
- Hyphens: `user-name` ❌ (use underscore `_`)

---

## 2. Basic Data Types

| Type | Example | Meaning |
|---|---|---|
| `int` | `25` | Whole numbers |
| `float` | `2.5` | Decimals |
| `str` | `"Hello"` | Text (Unicode) |
| `bool` | `True` / `False` | Truth values |

### 2.1 Strings (`str`)

```python
name = "Ali"          # double quotes
city = 'Tehran'       # single quotes — same thing
code = "12345"        # still a string, not a number!
```

Multi-line strings:

```python
text = """
Line one
Line two
"""
```

### 2.2 Booleans (`bool`)

```python
is_student = True
has_car = False
```

### 2.3 Check Type: `type()`

```python
print(type(25))        # <class 'int'>
print(type(2.5))       # <class 'float'>
print(type("hi"))      # <class 'str'>
print(type(True))      # <class 'bool'>
```

### 2.4 Type Conversion (Casting)

```python
s = "123"
print(type(s))         # str
n = int(s)
print(type(n))         # int

print(float("3.14"))   # 3.14
print(str(100))        # "100"
print(bool(0))         # False
print(bool(""))        # False
print(bool("hello"))   # True
```

---

## 3. Operators

### 3.1 Arithmetic

| Op | Name | Example | Result |
|---|---|---|---|
| `+` | Add | `5 + 3` | `8` |
| `-` | Subtract | `5 - 3` | `2` |
| `*` | Multiply | `5 * 3` | `15` |
| `/` | Divide | `5 / 2` | `2.5` **always float!** |
| `//` | Floor divide | `5 // 2` | `2` |
| `%` | Modulo | `5 % 2` | `1` |
| `**` | Power | `2 ** 10` | `1024` |

> **Note:** `/` always returns `float`. `10 / 5` → `2.0`, not `2`.

### 3.2 Comparison (return `bool`)

```python
5 == 5      # True  (equal)
5 != 3      # True  (not equal)
5 > 3       # True
5 >= 5      # True
5 < 3       # False
5 <= 3      # False
```

```python
print(10 / 2 == 5)    # True  because 5.0 == 5 → True
print(10 // 2 == 5)   # True
```

### 3.3 Logical Operators

| Op | Meaning | Example |
|---|---|---|
| `and` | Both true | `age >= 18 and has_id` |
| `or` | At least one true | `is_vip or age >= 18` |
| `not` | Invert | `not is_student` |

> **Note:** `and` / `or` / `not` are **keywords**, not `&` `|` `~`.

### 3.4 Augmented Assignment

```python
a = b = c = 0        # multiple assignment
x = 10
x += 5               # x = x + 5  → 15
x -= 3               # 12
x *= 2               # 24
x /= 4               # 6.0
x **= 2              # 36.0
x //= 5              # 7.0
x %= 3               # 1.0
```

`x += 1` is shorthand for `x = x + 1` — slightly faster and idiomatic.

---

## 4. Quick Practice

```python
# 1. 5 / 2  vs  5 // 2  vs  5 % 2
# 2. bool("False") → ?
# 3. "5" + 5 → ? (Error! Why?)
# 4. 10 / 2 == 5 → ?
# 5. x = x + 1  vs  x += 1 → difference?
```

---

## 🧪 Exercises for This Lesson

Try them: [`exercises/ex01_basics.py`](../exercises/ex01_basics.py)

```powershell
python exercises/ex01_basics.py
```

---
Next: [Lesson 2](02_control_flow.md) — Conditions & Loops.