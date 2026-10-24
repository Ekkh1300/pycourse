# پاسخ تمرین ۲ — شرط‌ها و حلقه‌ها
# نکته‌ی کلیدی: ترتیب شرط‌ها مهم است؛ اولین شرطِ درست اجرا می‌شود.

def sign_of(x):
    if x > 0:
        return "مثبت"
    elif x == 0:
        return "صفر"
    else:
        return "منفی"


def is_leap_year(year):
    # اول ۴۰۰، بعد ۱۰۰، و در آخر ۴
    return (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)


def max_of_three(a, b, c):
    if a >= b and a >= c:
        return a
    elif b >= c:
        return b
    else:
        return c


def count_digits(n):
    n = abs(n)
    if n == 0:
        return 1
    count = 0
    while n > 0:
        count += 1
        n //= 10
    return count


def sum_to(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total


def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def fizzbuzz(n):
    if n % 3 == 0 and n % 5 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    else:
        return str(n)
