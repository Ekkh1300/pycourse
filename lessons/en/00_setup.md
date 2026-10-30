# Lesson 0 — Setup & First Steps

> **Goal:** Get Python running, write your first program, and understand the edit → run cycle.

---

## 1. Install Python & VS Code (Recommended)

1. Install **VS Code** and add the **Python** extension (Microsoft).
2. Create a folder for your exercises and open it in VS Code.
3. Create a file named `hello.py` and press `Ctrl + F5` to run (no debugger needed).

### 2. Command Prompt / PowerShell

```powershell
cd path\to\your\folder
python hello.py
```

### 3. Interactive REPL (Quick Experiments)

```powershell
python
```

Type code directly; it runs line by line. Exit with `exit()` or `Ctrl+Z` then `Enter`.

---

## 2. Your First Program

```python
# hello.py
print("Hello, World!")
print("This is your first Python program.")
```

Run it: `python hello.py`

### 2.1 `print` Extras

```python
print("a", "b", "c")            # a b c   (space by default)
print("a", "b", sep=" - ")      # a - b   (custom separator)
print("a", end="")               # No newline after
print("b")                       # b       (continues on same line: ab)
print(f"Year: {1403}")          # f-string → Year: 1403
```

**f-strings** let you embed expressions inside `{}`.
Variables just go inside the braces:

```python
name = "Ali"
age = 25
print(f"{name} is {age} years old. In {age * 12} months.")
```

---

## 3. Input & Type Conversion

```python
name = input("Your name: ")
print(f"Hello, {name}!")
```

> **Important:** `input()` always returns a **string**. To do math, convert it:

```python
x = input("Number: ")   # x == "25"  (string!)
print(x + 1)            # TypeError: can only concatenate str
```

Convert to the right type:

```python
x = int(input("Integer: "))     # int("25") → 25
y = float(input("Decimal: "))   # float("2.5") → 2.5
```

`int()` and `float()` raise `ValueError` if the text isn't a valid number (handled later).

---

## 4. Comments

```python
# Single-line comment

"""
Multi-line comment (docstring).
Used at the top of files or functions to explain what they do.
"""
```

Comments are for **humans** — Python ignores them. Use them to explain *why*, not *what*.

---

## 5. Reading Errors (Tracebacks)

When something goes wrong, Python prints a **traceback**:

```
Traceback (most recent call last):
  File "hello.py", line 3, in <module>
    print(name)
NameError: name 'name' is not defined
```

Key parts to read:
- **Error type:** `NameError` (also `TypeError`, `IndentationError`, `SyntaxError`…)
- **Line number:** `line 3` — the line that crashed
- **Code context:** The actual line that failed

`NameError` means you used a name that hasn't been defined yet.

---

## 🎯 Exercises for This Lesson

Open `projects/first_steps.py` and follow the instructions:

1. Create variables for **name** (string), **age** (int), **height** (float) and print them with `print` and f-strings.
2. Work with **integers** and **floats** — try `/`, `//`, `%`, `**`.
3. Use `input()` to read **integers** and **floats** (don't forget `int()` / `float()`).
4. Write a tiny function that converts Celsius to Fahrenheit.

Run it:
```powershell
python projects/first_steps.py
```

---

Next up: [Lesson 1](01_basics.md) — Variables, Types & Operators.