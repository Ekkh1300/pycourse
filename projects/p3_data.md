# پروژه ۳ — تحلیل داده‌ی فروش (مسیر داده و هوش مصنوعی)

> **هدف:** با Pandas داده‌ی خام CSV را بخوان، تمیز کن، تحلیل کن و گزارش بساز.

---

## بخش ۱ — نصب

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install pandas matplotlib seaborn
```

---

## بخش ۲ — داده‌ی نمونه

فایل `sales.csv`:

```csv
date,product,category,price,quantity,city
1403/01/05,کیبورد,الکترونیک,850000,2,تهران
1403/01/07,ماوس,الکترونیک,320000,5,تهران
1403/01/12,دفتر,لوازم‌التحریر,45000,20,اصفهان
1403/02/01,مانیتور,الکترونیک,3200000,1,شیراز
```

برای تست، خودت یک فایل ۵۰-۱۰۰ ردیفی بساز (می‌توانی با یک اسکریپت پایتون
تولیدش کنی — تمرین خوبی برای حلقه و دیکشنری است).

---

## بخش ۳ — مراحل کار

### گام ۱ — خواندن و شناخت داده

```python
import pandas as pd

df = pd.read_csv("sales.csv", encoding="utf-8")
print(df.head())
print(df.info())
print(df.describe())
print(df.isna().sum())        # چندتا داده گم شده؟
```

### گام ۲ — پاک‌سازی

- تبدیل ستون `date` به نوع تاریخ (`pd.to_datetime`)
- حذف ردیف‌های تکراری (`df.drop_duplicates()`)
- پر کردن یا حذف مقادیر گمشده
- یکدست کردن متن ستون‌های رشته‌ای (فاصله‌های اضافه)

### گام ۳ — ستون‌های محاسباتی

```python
df["total"] = df["price"] * df["quantity"]
df["month"] = df["date"].dt.month
df["weekday"] = df["date"].dt.day_name()
```

### گام ۴ — تحلیل (groupby)

```python
df.groupby("category")["total"].sum().sort_values(ascending=False)
df.groupby("city")["total"].mean()
df.pivot_table(index="category", columns="month", values="total", aggfunc="sum")
```

### گام ۵ — نمودار

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
df.groupby("category")["total"].sum().plot(kind="bar")
plt.title("فروش بر اساس دسته")
plt.ylabel("مجموع فروش (تومان)")
plt.tight_layout()
plt.savefig("sales_by_category.png", dpi=150)
```

### گام ۶ — گزارش

یک تابع `generate_report(df)` بنویس که:
- آمار کلی (تعداد رکورد، مجموع فروش، میانگین سبد) را چاپ کند
- ۳ محله یا دسته‌ی برتر را مشخص کند
- یک نمودار ذخیره کند
- نتیجه را در یک فایل متنی (`report.txt`) بنویسد

---

## گام ۷ — قالب فارسی در نمودار

برای اینکه نمودار فارسی درست باشد:

```python
import matplotlib
matplotlib.rcParams["font.sans-serif"] = ["Tahoma"]
matplotlib.rcParams["axes.unicode_minus"] = False
```

---

## ساختار پیشنهادی

```
sales-analysis/
├── data/
│   └── sales.csv
├── analysis/
│   ├── loaders.py
│   ├── cleaners.py
│   └── reporting.py
├── main.py
└── requirements.txt
```

---

## امتیاز ویژه (اختیاری)

- [ ] نمودار چندتایی (subplot)
- [ ] مقایسه‌ی ماه‌به‌ماه
- [ ] خروجی HTML با `pandas.to_html`
- [ ] پیش‌بینی فروش ماه بعد با `scikit-learn` (linear regression)

---

## تعریف «تمام شد»

- [ ] CSV خوانده و پاک‌سازی می‌شود
- [ ] ستون `total` درست محاسبه می‌شود
- [ ] حداقل ۳ تحلیل `groupby` انجام شده
- [ ] یک نمودار با فونت فارسی ذخیره می‌شود
- [ ] گزارش متنی تولید می‌شود

---

کدت را برایم بفرست تا بازبینی کنم.
