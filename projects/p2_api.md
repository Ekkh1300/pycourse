# پروژه ۲ — وب‌سرویس مدیریت کتاب‌ها (مسیر وب و بک‌اند)

> **هدف:** یک API واقعی با FastAPI. اول مفاهیم HTTP را یاد می‌گیری، بعد پیاده‌سازی.

---

## بخش ۱ — مفاهیم لازم (قبل از کد)

اگر با HTTP آشنا نیستی، این چهار چیز را بفهم:

| مفهوم | توضیح |
|---|---|
| **Method** | `GET` (خواندن), `POST` (ساختن), `PUT` (کامل جایگزینی), `PATCH` (تغییر جزئی), `DELETE` (حذف) |
| **URL** | آدرس چیزی: `/books/12` یعنی کتاب با شناسه ۱۲ |
| **Status Code** | `200` موفق، `201` ساخته شد، `400` ورودی بد، `404` پیدا نشد، `422` اعتبارسنجی ناموفق، `500` خطای سرور |
| **JSON** | قالب داده: `{"title": "پایتون", "year": 2024}` |

نمونه‌ی درخواست و پاسخ:

```
GET /books
200 OK
[{"id": 1, "title": "پایتون", "year": 2024}]
```

---

## بخش ۲ — راه‌اندازی

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install fastapi uvicorn
```

```powershell
uvicorn main:app --reload
```

سپس در مرورگر: <http://127.0.0.1:8000/docs>
(این صفحه‌ی خودکار Swagger است — تست API را همان‌جا انجام می‌دهی.)

---

## بخش ۳ — صورت مسئله

یک API برای مدیریت کتاب‌ها بنویس:

| Method | URL | کار | پاسخ |
|---|---|---|---|
| `GET` | `/books` | لیست همه‌ی کتاب‌ها | `200` + آرایه |
| `GET` | `/books/{id}` | یک کتاب | `200` یا `404` |
| `POST` | `/books` | ساخت کتاب جدید | `201` + کتاب ساخته‌شده |
| `PUT` | `/books/{id}` | جایگزینی کامل | `200` یا `404` |
| `DELETE` | `/books/{id}` | حذف | `204` (بدون بدنه) |
| `GET` | `/books/search?title=...` | جست‌وجو | `200` + آرایه |

---

## بخش ۴ — ساختار پیشنهادی

```
bookapi/
├── main.py          # اپلیکیشن و روت‌ها
├── models.py        # مدل‌های Pydantic
├── database.py      # ذخیره‌سازی
└── requirements.txt
```

### مدل Pydantic

```python
from pydantic import BaseModel, Field

class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1)
    year: int = Field(ge=0, le=2100)
    pages: int | None = Field(default=None, ge=1)

class Book(BookCreate):
    id: int
```

مزیت Pydantic: **اعتبارسنجی خودکار**. اگر `year=9999` بفرستی، خود FastAPI
پاسخ `422` می‌دهد و لازم نیست دستی چک کنی.

### ذخیره‌سازی

برای شروع، یک لیست در حافظه کافی است:

```python
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Book API")
books: list[Book] = []
_next_id = 1
```

بعداً می‌توانی به SQLite با SQLAlchemy مهاجرت کنی.

---

## بخش ۵ — نکته‌های کلیدی

۱. **مدیریت خطا با `HTTPException`:**

```python
if book is None:
    raise HTTPException(status_code=404, detail="Book not found")
```

۲. **`response_model`:** برای اینکه خروجی همیشه همان شکل باشد.

۳. **فیلتر و مرتب‌سازی:** `/books?author=...&sort=year`

۴. **کد تمیز:** منطق در `database.py`، روت‌ها در `main.py`.

---

## امتیاز ویژه (اختیاری)

- [ ] ذخیره در SQLite با SQLAlchemy
- [ ] اعتبارسنجی با Pydantic v2
- [ ] تست با `pytest` + `TestClient`
- [ ] احراز هویت ساده با header

---

## تعریف «تمام شد»

- [ ] همه‌ی ۶ مسیر کار می‌کنند
- [ ] کتاب تکراری با id یکتا ساخته می‌شود
- [ ] مسیر ناموجود `404` با پیام فارسی می‌دهد
- [ ] ورودی نامعتبر `422` می‌گیرد (از Pydantic)

---

کدت را برایم بفرست تا بازبینی کنم.
