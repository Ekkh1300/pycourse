# Lesson 5 — Files, Error Handling & Modules

> **Goal:** Read/write files, handle errors gracefully, and import/reuse your own modules.

---

## 1. File I/O — Reading & Writing

### 1.1 `open()` & Context Manager (`with`)

```python
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()
print(content)
```

> The `with` statement **automatically closes** the file when the block ends — even if an error occurs inside it.

### 1.2 Write Mode (`"w"`) vs Read Mode (`"r"`)

| Mode | Meaning |
|---|---|
| `"r"` | Read only (default). File **must exist**, or `FileNotFoundError`. |
| `"w"` | **Write & truncate** — create or overwrite (empty the file first). |
| `"a"` | Append — add to the end; create if not exists. |
| `"x"` | Exclusive creation — fail if file already exists. |

### 1.3 Writing Lines

```python
lines = ["Hello", "World", "!"]
with open("out.txt", "w", encoding="utf-8") as f:
    for line in lines:
        f.write(line + "\n")
```

### 1.4 Reading All Lines

```python
with open("data.txt", encoding="utf-8") as f:
    lines = f.readlines()      # List of strings, each ending with "\n"

# Or line by line:
with open("data.txt", encoding="utf-8") as f:
    for line in f:
        print(line.strip())  # strip() removes trailing "\n"
```

### 1.5 `encoding="utf-8"` (Essential for Persian/Arabic)

```python
# Without encoding → may raise UnicodeDecodeError on non-ASCII text
with open("persian.txt", encoding="utf-8") as f:
    text = f.read()
```

---

## 2. `try / except / else / finally`

### 2.1 Basic Error Catching

```python
try:
    value = int(input("Enter a number: "))
except ValueError:
    print("That wasn't a valid number!")
```

### 2.2 Multiple Exception Types

```python
try:
    value = int(user_input)
except ValueError:
    print("Not a number!")
except KeyError:
    print("Missing key!")
except Exception as e:
    print(f"Something else: {e}")
```

### 2.3 `else` — Runs if No Exception

```python
try:
    f = open("data.txt", encoding="utf-8")
except FileNotFoundError:
    print("File not found")
else:
    print("File opened successfully — now do stuff with it")
finally:
    print("Cleanup always runs (open file or not)")
```

### 2.4 `finally` — Cleanup Always

Used to close files / release resources, regardless of success/failure:

```python
try:
    f = open("data.txt", encoding="utf-8")
    # process...
except:
    raise
finally:
    if not f.closed:
        f.close()
```

> **Better:** Use `with` statement — it handles cleanup automatically.

---

## 3. Safe Number Conversion

```python
def to_int(text):
    try:
        return int(text)
    except ValueError:
        return None

def parse_age(text):
    if not text.isdigit():
        raise ValueError(f"Invalid age: {text!r}")
    n = int(text)
    if n < 0:
        raise ValueError("Negative age")
    return n
```

### 3.1 `text.isdigit()` Trick

```python
"30".isdigit()      # True
"-5".isdigit()      # False  (minus sign makes it fail)
"abc".isdigit()     # False
"3.5".isdigit()     # False  (dot makes it fail)
```

Use `try/except int()` for robust conversion — `isdigit()` alone isn't enough for all cases.

---

## 4. JSON — Human-Readable Data Format

### 4.1 `json.dump()` & `json.load()`

```python
import json

data = {"name": "Ali", "age": 25, "city": "Tehran"}

# Write to file:
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)  # keep Persian as-is, not \u escapes

# Read from file:
with open("data.json", encoding="utf-8") as f:
    back = json.load(f)

print(back["name"])       # Ali
```

> **`ensure_ascii=False`** is crucial for non-ASCII text (Persian, Arabic, emoji). Without it, `"Ali"` → `\u06ac\u0632\u064a` in the file.

### 4.2 Safe Load (Handle missing/invalid files)

```python
def load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None
```

---

## 5. Modules — Reuse Code

### 5.1 Import Your Own Module

```python
# In mymodule.py
def greet(name):
    return f"Hello, {name}!"

# In main script:
from mymodule import greet
print(greet("Ali"))       # Hello, Ali!
```

### 5.2 Import Specific Names

```python
from mymodule import greet
# or
import mymodule
print(mymodule.greet("Ali"))
```

### 5.3 `__name__ == "__main__"` — Run as Script or Import

```python
# mymodule.py
def greet(name):
    return f"Hello, {name}!"

if __name__ == "__main__":
    # This runs ONLY when executed directly: `python mymodule.py`
    # When imported, this block is skipped.
    print(greet("World"))
```

### 5.4 `pip` & Virtual Environments

```powershell
# Create isolated environment:
python -m venv .venv
.venv\Scripts\activate        # Windows: activate
source .venv/bin/activate     # macOS / Linux

# Install packages:
pip install requests pandas

# Export requirements:
pip freeze > requirements.txt
```

> **Best practice:** Always work inside a virtual environment — it keeps your project's dependencies isolated from the system Python.

---

## 6. `argparse` — Command-Line Arguments

```python
import argparse

parser = argparse.ArgumentParser(description="A CLI tool")
parser.add_argument("--count", type=int, default=5, help="Number of items")
parser.add_argument("--name", required=True, help="Your name")

args = parser.parse_args()

print(args.count, args.name)
```

Run from terminal:

```powershell
python tool.py --name Ali --count 3
# Output: 3 Ali
```

> `--count 5` defaults to `5` if not provided. `--name` is **required** — must be given.

---

## 7. Test Cases

```python
# 1. open("f.txt", "w") truncates the file.
# 2. / or encoding="utf-8" needed for Persian.
# 3. json.dump with ensure_ascii=False preserves Persian.
# 4. to_int("abc") returns None (crash-safe).
# 5. try/except/finally always runs finally.
```

---

## 🎯 Exercises for This Lesson

Try them: [`exercises/ex05_files_errors.py`](../exercises/ex05_files_errors.py)

```powershell
python exercises/ex05_files_errors.py
```

---
Next: [Lesson 6](06_oop.md) — Object-Oriented Programming.