# Lesson 3 — Lists, Tuples, Dicts & Sets

> **Goal:** Work with Python's core collection types and understand their operations.

---

## 1. Lists (`list`) — Mutable Sequences

A list is an ordered, **changeable** collection:

```python
fruits = ["Apple", "Banana", "Cherry"]
numbers = [1, 2, 3]
mixed = [1, "hello", 3.5, True]      # Different types can mix
empty = []
```

### 1.1 Access & Slicing

```python
fruits = ["Apple", "Banana", "Cherry", "Date", "Elderberry"]
print(fruits[0])      # Apple       [0]  first item
print(fruits[2])      # Cherry
print(fruits[-1])     # Elderberry  last item
print(fruits[-2])     # Date        second from last

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(numbers[2:5])   # [2, 3, 4]     slice from index 2 to 4 (exclusive)
print(numbers[:3])    # [0, 1, 2]     from start to 2 (exclusive)
print(numbers[7:])    # [7, 8, 9]     from index 7 to end
print(numbers[::2])   # [0, 2, 4, 6, 8] every other
print(numbers[::-1])  # Reverse order
```

### 1.2 Modifying Lists

```python
numbers = [5, 3, 8, 1]

numbers.append(10)      # [5, 3, 8, 1, 10]   add to end
numbers.insert(0, 99)   # [99, 5, 3, 8, 1, 10] add at index 0
numbers.remove(99)      # removes 99              Oops not there → ValueError
last = numbers.pop()    # Remove last + return it
last = numbers.pop(2)   # Remove index 2, return it

numbers.sort()          # Sort ascending (in-place)
numbers.reverse()       # Reverse in-place
```

### 1.3 Key Methods Summary

| Method | Meaning |
|---|---|
| `append(x)` | Add `x` to end |
| `insert(i, x)` | Insert `x` at position `i` |
| `pop(i)` | Remove and return item at `i` (last if omitted) |
| `remove(x)` | Remove first item equal to `x` |
| `sort()` | Sort in-place (ascending by default) |
| `reverse()` | Reverse in-place |
| `clear()` | Remove all items |

> **Important:** `sort()` and `reverse()` return `None` — they modify the list **in-place**. To get a sorted copy, use `sorted(numbers)` or `numbers[::-1]`.

### 1.4 List Comprehensions — Concise Creation

```python
# Old way:
squares = []
for i in range(10):
    squares.append(i ** 2)

# New way:
squares = [i ** 2 for i in range(10)]       # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

> **Important:** A comprehension with `if` / `for` / `await` can be harder to read.  
> If the logic gets complex, use a regular `for` loop instead.

```python
evens = [i for i in range(20) if i % 2 == 0]          # Even numbers only
labels = ["✓" if n % 2 == 0 else "✗" for n in range(6)]  # if/else in comp

# Dict comprehension
squares_dict = {n: n ** 2 for n in range(5)}        # {0:0, 1:1, 2:4, 3:9, 4:16}

# Set comprehension (unique values)
unique_initials = {name[0] for name in ["Ali", "Reza", "Sara", "Mina"]}
```

---

## 2. Tuples (`tuple`) — Immutable Sequences

A tuple is **ordered but unchangeable** after creation. Used for fixed data.

```python
point = (3, 5)          # 2D coordinate
point[0]      # 3   (reading works)
# point[0] = 10   ❌ TypeError: 'tuple' does not support item assignment
```

### 2.1 Tuple Unpacking

```python
x, y = (3, 5)        # Unpack: x=3, y=5
a, b, c = 1, 2, 3    # Three variables get three values
```

### 2.2 Single-Item Tuple

```python
nums = (5,)        # Notice trailing comma — without it: just `5` (an int!)
```

### 2.3 Tuple vs List

- Use **tuple** when the data should not change (constants, function return values).
- Use **list** when you need to add/remove/change items later.

---

## 3. Dicts (`dict`) — Key-Value Pairs

A dictionary maps **keys** → **values**. Keys must be hashable (immutable: strings, numbers, tuples).

```python
user = {
    "name": "Ali",
    "age": 25,
    "city": "Tehran",
}
```

### 3.1 Access & Modify

```python
user["name"]            # "Ali"
user["age"] = 26        # Update age
user["job"] = "Developer"   # Add new key
del user["city"]        # Remove key
```

### 3.2 Safe Access: `.get()`

```python
user["name"]      # KeyError if key missing
user.get("name")  # None if key missing (no crash)
user.get("name", "Unknown")  # Default value
```

### 3.3 Check Key Existence

```python
"age" in user           # True
"job" in user           # False
```

### 3.4 Common Dict Operations

| Method | Meaning |
|---|---|
| `keys()` | Return all keys |
| `values()` | Return all values |
| `items()` | Return (key, value) pairs |
| `get(key, default)` | Safe access with default |
| `setdefault(key, val)` | If key missing, set and return `val` |
| `pop(key)` | Remove and return value |
| `update(other_dict)` | Merge another dict's items |

### 3.5 Nested Dicts

```python
users = {
    "ali":  {"age": 30, "city": "Tehran"},
    "sara": {"age": 25, "city": "Shiraz"},
}

print(users["ali"]["city"])          # Tehran
print(users.get("sara", {}).get("age"))  # 25 (safe chain)
```

### 3.6 `setdefault` Pattern

```python
d = {}
d.setdefault("count", 0)
d["count"] += 1
# Now d == {"count": 1}
```

---

## 4. Sets (`set`) — Unique Collections

A **set** is an unordered collection of **unique** values. Great for membership tests and deduplication.

```python
nums = {1, 2, 3, 3, 2}
print(nums)      # {1, 2, 3}  duplicates removed

a = {1, 2, 3}
b = {3, 4, 5}

a | b      # {1,2,3,4,5}   Union
a & b      # {3}           Intersection
a - b      # {1,2}         Difference (in a, not in b)
a ^ b      # {1,2,4,5}     Symmetric diff
```

### 4.1 Creating a Set

```python
allowed = {"ali", "sara", "reza"}
if "ali" in allowed:      # Very fast membership test
    print("Welcome!")
```

```python
numbers = [1, 2, 2, 3, 3, 3, 4]
unique = list(set(numbers))    # [1, 2, 3, 4] — removes duplicates
```

### 4.2 Frozen Sets (Immutable)

```python
fs = frozenset([1, 2, 3])      # Can't add/remove after creation
```

---

## 5. Type Summary (Quick Reference)

| Type | Mutable? | Order? | Unique? | Typical Use |
|---|---|---|---|---|
| `list` | ✅ Yes | ✅ Yes | ❌ No | Collections you modify |
| `tuple` | ❌ No | ✅ Yes | ❌ No | Fixed data, constants |
| `dict` | ✅ Keys can change values | ✅ Yes | ✅ Keys unique | Key → value mappings |
| `set` | ❌ No elements | ❌ No | ✅ Yes | Unique collections, membership tests |

**U+O-U^U~U:** `dict` has `keys()` unique; `list` can have duplicates.

---

## 🎯 Exercises for This Lesson

Try them: [`exercises/ex03_collections.py`](../exercises/ex03_collections.py)

```powershell
python exercises/ex03_collections.py
```

---
Next: [Lesson 4](04_functions.md) — Functions.