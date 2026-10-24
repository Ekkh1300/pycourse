# پاسخ تمرین ۱ — متغیرها، انواع داده و عملگرها
# نکته‌ی کلیدی: تقسیم با / همیشه float می‌دهد، برای تقسیم صحیح از // استفاده کن.

name = "Ali"
age = 25
height = 1.75

a = 15
b = 4
sum_ab = a + b
div_ab = a / b
int_div = a // b
mod_ab = a % b
pow_ab = a ** b

text_number = "25"
number = int(text_number)
number_type = type(number)

is_adult = age >= 18
can_vote = is_adult

greeting = f"{name} is {age} years old"


def celsius_to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32
