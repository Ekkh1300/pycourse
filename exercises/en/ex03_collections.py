"""
Exercise 3 — Lists, Tuples, Dicts & Sets
================================================
Run: python exercises/ex03_collections.py

This exercise tests collection types and their operations.
"""

import sys

# Windows: Console default cp1252 messes with Persian. This fixes it.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")


# ─────────────────────────────────────────────────────────────
# TODO 1 — List Operations
# Create list numbers: [12, 7, 25, 3, 18]
# Then calculate:
#   biggest      = largest number
#   smallest     = smallest number
#   total        = sum of all
#   evens        = count of even numbers
#   doubled      = list with each number multiplied by 2 (don't modify original)
# ─────────────────────────────────────────────────────────────
numbers = [12, 7, 25, 3, 18]
biggest = None
smallest = None
total = None
evens = None
doubled = None

# ─────────────────────────────────────────────────────────────
# TODO 2 — Slicing
# For list numbers create:
#   first_two   = first two items
#   last_three  = last three items
#   middle      = items from index 1 to 3 (exclusive)
# ─────────────────────────────────────────────────────────────
first_two = None
last_three = None
middle = None

# ─────────────────────────────────────────────────────────────
# TODO 3 — List Modification
# Start with fruits = ["Apple", "Banana", "Cherry"]
# Then:
#   - Append "Date"
#   - Insert "Elderberry" at index 1
#   - Remove "Banana"
#   - Pop the last item and store in popped
# ─────────────────────────────────────────────────────────────
fruits = ["Apple", "Banana", "Cherry"]
# Do modifications here
popped = None

# ─────────────────────────────────────────────────────────────
# TODO 4 — Tuple Unpacking
# Unpack the tuple (1, 2, 3) into a, b, c
# ─────────────────────────────────────────────────────────────
a = b = c = None

# ─────────────────────────────────────────────────────────────
# TODO 5 — Dict Operations
# Create user = {"name": "Ali", "age": 25, "city": "Tehran"}
# Then:
#   - Update age to 26
#   - Add job = "Developer"
#   - Get email with .get(), default "Not provided"
#   - Delete city
# ─────────────────────────────────────────────────────────────
user = {"name": "Ali", "age": 25, "city": "Tehran"}
# Do modifications here
email = None

# ─────────────────────────────────────────────────────────────
# TODO 6 — Set Operations
# Given sets a = {1, 2, 3}, b = {3, 4, 5}
# Create:
#   union_set     = a ∪ b
#   intersect_set = a ∩ b
#   diff_set      = a - b
#   sym_diff_set  = a ^ b
# ─────────────────────────────────────────────────────────────
a_set = {1, 2, 3}
b_set = {3, 4, 5}
union_set = None
intersect_set = None
diff_set = None
sym_diff_set = None

# ─────────────────────────────────────────────────────────────
# TODO 7 — Deduplication
# Function unique_sorted(lst) returns sorted unique values from lst.
# Example: unique_sorted([3, 1, 2, 3, 2, 1]) → [1, 2, 3]
# ─────────────────────────────────────────────────────────────
def unique_sorted(lst):
    pass


# ═════════════════════════════════════════════════════════════
#  Tests — you can modify them for debugging
# ═════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Testing...\n")

    # TODO 1
    assert biggest == 25, f"biggest should be 25, got {biggest!r}"
    assert smallest == 3, f"smallest should be 3, got {smallest!r}"
    assert total == 65, f"total should be 65, got {total!r}"
    assert evens == 3, f"evens should be 3, got {evens!r}"
    assert doubled == [24, 14, 50, 6, 36], f"doubled should be [24,14,50,6,36], got {doubled!r}"
    assert numbers == [12, 7, 25, 3, 18], "original numbers should not be modified"

    # TODO 2
    assert first_two == [12, 7], f"first_two should be [12,7], got {first_two!r}"
    assert last_three == [25, 3, 18], f"last_three should be [25,3,18], got {last_three!r}"
    assert middle == [7, 25], f"middle should be [7,25], got {middle!r}"

    # TODO 3
    assert fruits == ["Apple", "Elderberry", "Cherry", "Date"], f"fruits should be ['Apple','Elderberry','Cherry','Date'], got {fruits!r}"
    assert popped == "Date", f"popped should be 'Date', got {popped!r}"

    # TODO 4
    assert (a, b, c) == (1, 2, 3), f"unpack failed: got ({a},{b},{c})"

    # TODO 5
    assert user["age"] == 26, f"age should be 26, got {user.get('age')!r}"
    assert user["job"] == "Developer", f"job should be 'Developer', got {user.get('job')!r}"
    assert "city" not in user, "city should be deleted"
    assert email == "Not provided", f"email should be 'Not provided', got {email!r}"

    # TODO 6
    assert union_set == {1, 2, 3, 4, 5}, f"union failed: {union_set!r}"
    assert intersect_set == {3}, f"intersection failed: {intersect_set!r}"
    assert diff_set == {1, 2}, f"diff failed: {diff_set!r}"
    assert sym_diff_set == {1, 2, 4, 5}, f"sym_diff failed: {sym_diff_set!r}"

    # TODO 7
    assert unique_sorted([3, 1, 2, 3, 2, 1]) == [1, 2, 3]
    assert unique_sorted([]) == []
    assert unique_sorted([5]) == [5]

    print("✅ All tests passed!")