# Lesson 4 — Functions

> **Goal:** Write reusable blocks of code with parameters, arguments, return values, and scope rules.

---

## 1. Defining & Calling Functions

```python
def greet():
    print("Hello!")

greet()      # Call it
```

### 1.1 Functions With Parameters

```python
def greet(name):
    print(f"Hello, {name}!")

greet("Ali")
```

### 1.2 Return Values

```python
def add(a, b):
    return a + b

result = add(3, 5)    # result = 8
```

> **Important:** Without `return` (or `return` with no value), the function returns `None`.  
> ```python
> def f():  return 5
> def g():  print(5)      # returns None!
> ```

---

## 2. Argument Patterns

### 2.1 Default Arguments

```python
def greet(name, greeting="Hello"):
    print(f"{greeting} {name}!")

greet("Ali")                 # Hello Ali!
greet("Ali", "Good morning")    # Good morning Ali!
```

### 2.2 Keyword Arguments (named)

```python
def greet(name, greeting="Hello"):
    ...

greet(greeting="Hi", name="Ali")      # Named order (clarity)
```

### 2.3 Positional-Only Arguments (`/`)

```python
def greet(name, /, greeting="Hello"):
    ...
greet("Ali", "Hi")    # OK
greet(name="Ali")     # ❌ TypeError — name is positional-only
```

### 2.4 Variable Arguments (`*args` and `**kwargs`)

```python
def total(*args):
    return sum(args)

total(1, 2, 3)      # 6

def profile(name, **kwargs):
    print(name, kwargs)

profile("Ali", age=25, city="Tehran")
# Ali {'age': 25, 'city': 'Tehran'}
```

### 2.5 Full Signature

```python
def f(a, b=2, *args, c, **kwargs):
    ...
```

Order: positional-only (`/`) → standard params with defaults → `*args` → keyword-only (`c`) → `**kwargs`.

---

## 3. Type Hints (Annotations)

Type hints are **optional** hints for IDEs and readers — they don't enforce anything at runtime.

```python
def add(a: int, b: int) -> int:
    return a + b

def greet(name: str, excited: bool = False) -> str:
    return f"Hi {name}!"

def items() -> list[str]:
    return ["a", "b"]
```

Type hints improve:
- IDE autocomplete & warnings (`len` on an `int`)
- Documentation (`list[str]` is clearer than vague `list`)
- Static checking (`mypy`, `pyright`)

But use them consistently — mixed code (some hints, some not) is worse than none.

---

## 4. Scope — Where Variables Live

```python
x = "outer"

def show():
    print(x)          # Reads x from outer scope

def change():
    x = "inner"       # Creates a NEW local x — does NOT affect outer x!
    print(x)          # inner

change()
print(x)              # Still "outer"
```

**Scope rules:** A name **assigned** inside a function is **local** — even if a name with the same name exists outside.

### 4.1 `global` — Mutating Outer Variables

```python
counter = 0

def increment():
    global counter
    counter += 1
```

> **Warning:** `global` is discouraged — pass values as arguments and `return` the result instead:
> ```python
> def increment(counter):
>     return counter + 1
> ```

### 4.2 Mutable Default Arguments (⚠️ Trap!)

```python
def add_item(item, bucket=[]):     # ❌ BUG
    bucket.append(item)
    return bucket

add_item(1)   # [1]
add_item(2)   # [1, 2]  ← shared list!
```

**Fix:** Default to `None` and create inside:

```python
def add_item(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket
```

**Rule:** Never use mutable defaults like `[]`, `{}` — they get **shared across calls**.

---

## 5. Functions Are First-Class Objects

Functions can be assigned, passed around, and stored in data structures:

```python
def double(x):  return x * 2
def triple(x):  return x * 3

ops = {"double": double, "triple": triple}
print(ops["double"](5))    # 10

numbers = [1, 2, 3, 4]
doubled = list(map(double, numbers))     # [2, 4, 6, 8]
```

Or use `lambda` for tiny throwaway functions:

```python
people = [("Ali", 25), ("Sara", 30), ("Reza", 22)]
people.sort(key=lambda p: p[1])   # Sort by age (second element)
```

---

## 6. Docstrings — Document Your Functions

```python
def area(width, height):
    """Calculate the area of a rectangle.

    Args:
        width: The width,
        height: The height,

    Returns:
        The area.
    """
    return width * height
```

`help(area)` and `area.__doc__` read the docstring.  
**Always document *why*, not *what*.**

---

## 7. Test Cases

Predict the output:

```python
def greet(name, greeting="Hello"):
    return f"{greeting} {name}"

greet("Ali")                # ?
greet("Ali", "Good morning")    # ?
greet(greeting="Hi", name="Ali")  # ?
```

---

## 🧪 Exercises for This Lesson

Try them: [`exercises/ex04_functions.py`](../exercises/ex04_functions.py)

```powershell
python exercises/ex04_functions.py
```

---
Next: [Lesson 5](05_files_errors_modules.md) — Files, Errors & Modules.