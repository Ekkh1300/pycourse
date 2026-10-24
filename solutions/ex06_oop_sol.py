# پاسخ تمرین ۶ — کلاس‌ها و OOP
# نکته‌ی کلیدی: متدهای کلاس همیشه self را به‌عنوان اولین آرگومان می‌گیرند.

from dataclasses import dataclass


class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        return f"{self.name} می‌گوید: هاو!"

    def birthday(self):
        self.age += 1
        return self.age

    def __str__(self):
        return f"Dog({self.name}, {self.age})"


class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amount
        return self.balance

    @property
    def has_funds(self):
        return self.balance > 0

    def __str__(self):
        return f"balance: {self.balance}"


class SavingsAccount(BankAccount):
    def __init__(self, owner, balance=0, rate=0.05):
        super().__init__(owner, balance)
        self.rate = rate

    def interest(self):
        return self.balance * self.rate

    def add_interest(self):
        self.balance += self.interest()
        return self.balance


@dataclass
class Product:
    name: str
    price: float
    quantity: int = 1

    def total(self):
        return self.price * self.quantity
