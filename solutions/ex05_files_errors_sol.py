# پاسخ تمرین ۵ — فایل، مدیریت خطا و ماژول
# نکته‌ی کلیدی: همیشه از with استفاده کن و encoding="utf-8" را فراموش نکن.

import json
import sys
import tempfile
from pathlib import Path


def write_lines(path, lines):
    with open(path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")


def read_lines(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def to_int(text):
    try:
        return int(text)
    except (ValueError, TypeError):
        return None


def parse_age(text):
    try:
        age = int(text)
    except (ValueError, TypeError):
        raise ValueError("invalid age")
    if age < 0:
        raise ValueError("negative age")
    return age


def count_words(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return len(f.read().split())
    except FileNotFoundError:
        return 0
