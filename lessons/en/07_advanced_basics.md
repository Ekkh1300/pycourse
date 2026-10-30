# Lesson 7 — Advanced Basics

> **Goal:** Learn Python features you'll use constantly in real-world code: comprehensions, lambdas, map/filter, enumerate/zip, sorting, decorators, `__main__`, pathlib, context managers, argparse, virtual environments, pytest.

---

## 1. List Comprehensions

Create lists concisely:

```python
# Traditional loop:
squares = []
for i in range(10):
    squares.append(i ** 2)

# Comprehension:
squares = [i ** 2 for i in range(10)]   # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

### 1.1 With Condition

```python
evens = [i for i in range(20) if i % 2 == 0]   # Even numbers only
labels = ["✓" if n % 2 == 0 else "✗" for n in range(6)]  # if/else inline
```

### 1.2 Dict & Set Comprehensions

```python
squares_dict = {n: n ** 2 for n in range(5)}   # {0:0, 1:1, 2:4, 3:9, 4:16}
unique_initials = {name[0] for name in ["Ali", "Reza", "Sara"]}   # {'A', 'R', 'S'}
```

> **Important:** Comprehensions are great for simple transformations. If the logic becomes complex, use a regular `for` loop — readability wins.

---

## 2. `lambda` — Anonymous Functions

Small throwaway functions:

```python
square = lambda x: x ** 2
square(4)      # 16
```

Typically used with `key` argument in sorting:

```python
people = [("Ali", 25), ("Sara", 30), ("Reza", 22)]
people.sort(key=lambda p: p[1])   # Sort by age → [(Reza, 22), (Ali, 25), (Sara, 30)]
```

`lambda` is for **simple expressions only** — no statements, no multi-line bodies. Use `def` for anything complex.

---

## 3. `map` / `filter` / `reduce`

### 3.1 `map` — Apply Function to Each Item

```python
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))   # [2, 4, 6, 8, 10]
```

### 3.2 `filter` — Keep Items Matching Condition

```python
evens = list(filter(lambda x: x % 2 == 0, numbers))   # [2, 4]
```

### 3.3 `reduce` — Combine Into One Value

```python
from functools import reduce
total = reduce(lambda a, b: a + b, numbers, 0)   # 15
```

> **Tip:** List comprehensions are usually more readable than `map`/`filter`. Use `map`/`filter` when you already have a named function.

---

## 4. `enumerate` & `zip`

### 4.1 `enumerate` — Index + Item

```python
fruits = ["Apple", "Banana", "Cherry"]
for i, fruit in enumerate(fruits, start=1):
    print(i, fruit)
# 1 Apple
# 2 Banana
# 3 Cherry
```

### 4.2 `zip` — Pair Multiple Iterables

```python
names = ["Ali", "Sara", "Reza"]
ages  = [25, 30, 22]

for name, age in zip(names, ages):
    print(name, age)
```

> `zip` stops at the **shortest** iterable. In Python 3.10+, `strict=True` raises if lengths mismatch:

```python
zip(names, ages, strict=True)   # Raises ValueError if lengths differ
```

---

## 5. `sorted` & `key`

Sort with custom logic:

```python
users = [
    {"name": "Ali", "age": 25},
    {"name": "Sara", "age": 30},
    {"name": "Reza", "age": 22},
]

users.sort(key=lambda u: u["age"])              # Sort by age (ascending)
users.sort(key=lambda u: u["name"], reverse=True)  # Sort by name (descending)
```

### 5.1 Sort by Multiple Criteria

```python
users.sort(key=lambda u: (u["age"], u["name"]))   # Age first, then name
```

---

## 6. Decorators — Wrap Functions

A decorator **wraps** a function to add behavior without changing its source.

### 6.1 Simple Timer

```python
import functools
import time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_work(n):
    return sum(range(n))

slow_work(1000000)
```

### 6.2 Decorator with Arguments

```python
def retry(times=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == times - 1:
                        raise
        return wrapper
    return decorator

@retry(times=5)
def flaky_network_call(): ...
```

> `@functools.wraps(func)` preserves the original function's metadata (`__name__`, `__doc__`).

---

## 7. `__main__.py` — Run as Script vs Import

```python
def main():
    print("Running as main script!")

if __name__ == "__main__":
    main()
```

- Executed directly (`python script.py`): `__name__ == "__main__"` → `main()` runs.
- Imported as module (`import script`): `__name__ != "__main__"` → `main()` does **not** run.

> **Best practice:** Always put your "run as script" code inside this guard. It makes your code reusable as a module.

### 7.1 `__main__.py` for Packages

Create `my_project/__main__.py` so `python -m my_project` works:

```
my_project/
├── __main__.py    # Entry point for python -m my_project
├── __init__.py
├── models.py
└── utils.py
```

---

## 8. `pathlib` — Modern Path Handling

```python
from pathlib import Path

folder = Path("data")
folder.mkdir(exist_ok=True)          # Create dir if missing

for txt in folder.glob("*.txt"):
    print(txt.name, txt.stat().st_size)   # Name + size
```

Path operations:

```python
p = Path("data") / "sub" / "file.txt"
p.parent.mkdir(parents=True, exist_ok=True)
if p.exists():
    text = p.read_text(encoding="utf-8")
    p.write_text("New content", encoding="utf-8")
```

> Prefer `pathlib` over `os.path` — it's more readable and object-oriented.

---

## 9. Context Managers — Resource Cleanup

A context manager runs setup before and teardown after — even on exceptions:

```python
from contextlib import contextmanager
import time

@contextmanager
def timer(name):
    start = time.perf_counter()
    yield               # Code inside `with` runs here
    print(f"{name}: {time.perf_counter() - start:.3f}s")

with timer("work"):
    do_something()
```

> **Built-in context managers:** `open()`, `sqlite3.connect()`, `threading.Lock()` all support `with`.

---

## 10. `argparse` — Command-Line Arguments

Build CLI tools easily:

```python
import argparse

parser = argparse.ArgumentParser(description="CLI tool")
parser.add_argument("--count", type=int, default=5, help="Number of items")
parser.add_argument("--name", required=True, help="Your name")

args = parser.parse_args()
print(args.count, args.name)
```

Run:

```powershell
python tool.py --name Ali --count 3
# Output: 3 Ali
```

> `--count 5` has a default; `--name` is required.

---

## 11. Virtual Environments & Dependencies

Keep each project's packages isolated:

```powershell
# Create environment:
python -m venv .venv

# Activate:
.venv\Scripts\activate        # Windows CMD/PowerShell
source .venv/bin/activate     # macOS / Linux

# Install packages:
pip install requests pandas

# Export requirements:
pip freeze > requirements.txt
```

---

## 12. `pytest` — Automated Testing

```python
# test_math.py
def test_add():
    from mymodule import add
    assert add(2, 3) == 5
```

Run:

```powershell
pip install pytest
pytest -v
```

> Write tests early — they catch bugs fast and document expected behavior.

---

## Test Cases

```python
# 1. [i*i for i in range(5) if i % 2 == 0] → ?
# 2. list(map(str, [1,2])) → ?
# 3. sort() vs sorted() — in-place vs new list?
```

---

## 🎯 Exercises for This Lesson

Try them: [`exercises/ex07_advanced.py`](../exercises/ex07_advanced.py)

```powershell
python exercises/ex07_advanced.py
```

---
Done with all lessons! You've covered the full beginner Python curriculum.