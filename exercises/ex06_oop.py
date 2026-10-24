"""
تمرین ۶ — کلاس‌ها و OOP
================================================================
اجرا:  python exercises/ex06_oop.py
"""

import sys

# ویندوز: کنسول پیش‌فرض cp1252 است و متن فارسی را خراب می‌کنند — این خط‌ها حلش می‌کنند
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")


# ─────────────────────────────────────────────────────────────
# TODO 1 — کلاس پایه
# کلاس Dog بنویس با:
#   __init__(self, name, age)
#   صفت‌ها: name, age
#   متد bark(self) که رشته‌ی "«name» می‌گوید: هاو!" را برگرداند
#   متد __str__(self) که "Dog(name, age)" را برگرداند
# ─────────────────────────────────────────────────────────────


class Dog:
    pass  # کلاس را کامل کن


# ─────────────────────────────────────────────────────────────
# TODO 2 — متدِ تغییردهنده
# به کلاس Dog متد birthday(self) اضافه کن که سن را یکی زیاد کند
# و سن جدید را برگرداند.
# ─────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────
# TODO 3 — کلاس BankAccount
# کلاس BankAccount بنویس:
#   __init__(self, owner, balance=0)
#   صفت‌ها: owner, balance
#   deposit(self, amount)  → موجودی را زیاد کند و موجودی جدید را برگرداند
#   withdraw(self, amount) → اگر amount > balance نبود، ValueError("insufficient funds")
#                            بده؛ وگرنه موجودی را کم کن و موجودی جدید را برگرداند
#   __str__(self) → "balance: X"
# ─────────────────────────────────────────────────────────────


class BankAccount:
    pass


# ─────────────────────────────────────────────────────────────
# TODO 4 — property
# به کلاس BankAccount یک property به نام has_funds اضافه کن
# که True برگرداند اگر balance > 0 باشد.
# (یعنی: account.has_funds بدون پرانتز کار کند)
# ─────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────
# TODO 5 — وراثت
# کلاس SavingsAccount بنویس که از BankAccount ارث ببرد:
#   __init__(self, owner, balance=0, rate=0.05)
#   متد interest(self) که سود سالانه را برگرداند: balance * rate
#   متد add_interest(self) که سود را به موجودی اضافه کند و موجودی جدید را برگرداند
# یادت باشد super().__init__(...) را صدا بزنی.
# ─────────────────────────────────────────────────────────────


class SavingsAccount:
    pass


# ─────────────────────────────────────────────────────────────
# TODO 6 — dataclass
# با dataclass یک کلاس Product بساز:
#   name: str
#   price: float
#   quantity: int = 1
#   متد total(self) که price * quantity را برگرداند
# ─────────────────────────────────────────────────────────────


# ═════════════════════════════════════════════════════════════
#  تست‌ها
# ═════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("در حال بررسی...\n")

    # TODO 1
    d = Dog("شاهو", 3)
    assert d.name == "شاهو", "name اشتباه"
    assert d.age == 3, "age اشتباه"
    assert d.bark() == "شاهو می‌گوید: هاو!", f"bark اشتباه: {d.bark()!r}"
    assert str(d) == "Dog(شاهو, 3)", f"__str__ اشتباه: {str(d)!r}"

    # TODO 2
    d2 = Dog("پتی", 1)
    assert d2.birthday() == 2, "birthday باید 2 برگرداند"
    assert d2.age == 2, "سن باید واقعاً تغییر کند"

    # TODO 3
    acc = BankAccount("مریم", 100)
    assert acc.owner == "مریم", "owner اشتباه"
    assert acc.balance == 100, "balance اشتباه"
    assert acc.deposit(50) == 150, "deposit اشتباه"
    assert acc.balance == 150, "balance باید به‌روز شود"
    assert acc.withdraw(30) == 120, "withdraw اشتباه"
    assert acc.balance == 120, "balance باید به‌روز شود"
    try:
        acc.withdraw(1000)
        raise AssertionError("باید ValueError می‌داد!")
    except ValueError as e:
        assert str(e) == "insufficient funds", f"پیام اشتباه: {e}"
    assert acc.balance == 120, "باید بعد از خطا تغییری نکند!"

    # TODO 4
    assert acc.has_funds is True, "has_funds باید True باشد"
    acc2 = BankAccount("علی")
    assert acc2.has_funds is False, "has_funds باید False باشد"

    # TODO 5
    sav = SavingsAccount("سارا", 1000, 0.05)
    assert sav.interest() == 50, f"interest اشتباه: {sav.interest()!r}"
    assert sav.add_interest() == 1050, "add_interest اشتباه"
    assert sav.balance == 1050, "موجودی باید به‌روز شود"
    assert sav.owner == "سارا", "ارث‌بری درست کار نمی‌کند"
    assert isinstance(sav, BankAccount), "SavingsAccount باید از BankAccount ارث ببرد"

    # TODO 6
    p = Product("کتاب", 50.0, 3)
    assert p.name == "کتاب", "name اشتباه"
    assert p.total() == 150.0, f"total اشتباه: {p.total()!r}"
    assert Product("دفتر", 20.0).quantity == 1, "مقدار پیش‌فرض اشتباه"

    print("✅ همه‌ی تست‌ها پاس شد! حالا کدت را برای من بفرست.")
