# Lesson 2 — Conditions & Loops

> **Goal:** Make decisions with `if/elif/else` and repeat work with `while`/`for` loops.

---

## 1. `if` & Branching

```python
age = 20

if age >= 18:
    print("You are an adult")
```

The block under `if` runs **only** when the condition is `True`.  
Indentation (4 spaces) defines the block — no `{}` needed.

### 1.1 `if / else`

```python
age = 15

if age >= 18:
    print("Adult")
else:
    print("Minor")
```

### 1.2 `if / elif / else` — Multiple Branches

```python
grade = 85

if grade >= 90:
    print("A")
elif grade >= 75:
    print("B")
elif grade >= 60:
    print("C")
else:
    print("F")
```

> **Tip:** Only the **first** matching branch runs. Order matters — check stricter conditions first.

---

## 2. Boolean Operators in Conditions

```python
age = 20
has_ticket = True

if age >= 18 and has_ticket:
    print("Entry allowed")
elif age >= 18 or has_ticket:
    print("One condition met")
else:
    print("Entry denied")
```

| Operator | Result |
|---|---|
| `a and b` | True only if both are true |
| `a or b` | True if at least one is true |
| `not a` | Inverts |
| `a != b` | Not equal |

**Short-circuit gotcha:** `and` / `or` return the *actual value*, not just `True/False`:

```python
value = 5
print(value and 10)    # 10   (value is truthy → returns 10)
value = 0
print(value and 10)    # 0    (value is falsy → returns 0)
```

This is useful but can surprise you — be explicit with `bool()` if needed.

---

## 3. `while` Loops — Repeat Until False

```python
count = 0

while count < 5:
    print(count)
    count += 1
```

> **Warning:** **Infinite loops** happen when the condition never becomes false.  
> Always ensure something inside the loop changes the condition.

---

## 4. `for` Loops — Iterate Over Sequences

```python
for i in range(5):
    print(i)
# 0 1 2 3 4
```

### 4.1 `range` — Three Forms

```python
range(5)          # 0, 1, 2, 3, 4              (stop only)
range(2, 6)       # 2, 3, 4, 5                 (start, stop)
range(0, 10, 2)   # 0, 2, 4, 6, 8              (start, stop, step)
range(5, 0, -1)   # 5, 4, 3, 2, 1              (reverse)
```

### 4.2 Iterate Over Strings & Lists

```python
for ch in "hello":
    print(ch)

for item in [10, 20, 30]:
    print(item)
```

---

## 5. `break` & `continue`

```python
for i in range(10):
    if i == 5:
        break        # Exit loop entirely
    print(i)
# 0 1 2 3 4

for i in range(10):
    if i % 2 == 0:
        continue     # Skip rest of this iteration
    print(i)
# 1 3 5 7 9
```

---

## 6. `else` on Loops (Rare but Useful)

A loop's `else` runs **only if the loop wasn't `break`ed**:

```python
for n in range(2, 10):
    if n == 7:
        print("Found 7!")
        break
else:
    print("No 7 found")
```

---

## 7. Common Loop Patterns

### 7.1 Reverse Countdown

```python
for i in range(10, 0, -1):
    print(i)
```

### 7.2 Input Until Valid (while True + break)

```python
while True:
    raw = input("Enter a positive number: ")
    try:
        number = int(raw)
        break
    except ValueError:
        print("Not a valid integer — try again.")

print(f"You entered: {number}")
```

### 7.3 Accumulator (Sum/Count)

```python
total = 0
for i in range(1, 6):
    total += i
print(total)   # 15
```

Accumulator = loop + variable updated each iteration. Very common pattern.

---

## 8. Common Mistakes

| Mistake | Fix |
|---|---|
| `=` instead of `==` | `if x = 5:` → `SyntaxError` — use `==` |
| Forgetting `==` with numbers | `if x:` is true for any non-zero — use `if x == 0:` |
| Missing indentation | `IndentationError` — indent all block lines by 4 spaces |
| Infinite loop | Add a way to change the condition inside the loop |
| `or` / `and` vs `||` / `&&` | Python uses `or` / `and` — no `||` `&&` |

---

## 🎯 Practice Exercises

Predict the output:

1. ```python
   x = 5
   if x > 10:
       print("A")
   elif x > 3:
       print("B")
   else:
       print("C")
   ```

2. ```python
   for i in range(1, 10, 3):
       print(i, end=" ")
   ```

3. ```python
   n = 0
   while n < 3:
       print(n)
       n += 1
   else:
       print("done")
   ```

---

## 🧪 Exercises for This Lesson

Try them: [`exercises/ex02_control_flow.py`](../exercises/ex02_control_flow.py)

```powershell
python exercises/ex02_control_flow.py
```

---
Next: [Lesson 3](03_collections.md) — Lists, Tuples, Dicts & Sets.