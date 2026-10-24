"""
ساخت اسکریپت بررسی: هر تست جداگانه اجرا و گزارش می‌شود.

به‌جای اینکه یک `assert` شکست‌خورده کل بقیه‌ی تست‌ها را از کار بیندازد،
همه‌ی تست‌ها را جدا می‌کنیم و نتیجه‌ی هرکدام را جداگانه می‌گیریم.
"""

from __future__ import annotations

import ast

RESULTS_MARKER = "__PYCOURSE_RESULTS__"


def _wrap_assert(node: ast.Assert) -> ast.stmt:
    """یک assert را به try/except تبدیل می‌کند که نتیجه را ثبت کند.

    علاوه بر AssertionError، هر خطای دیگری هم گرفته می‌شود — مثلاً وقتی
    تابعی که باید ساخته شود هنوز تعریف نشده، همان تست باید «خطا» گزارش شود
    نه اینکه کل اجرا را از کار بیندازد.
    """
    code = ast.unparse(node)
    indented = "\n".join("    " + line for line in code.splitlines())
    source = (
        "try:\n"
        f"{indented}\n"
        "except AssertionError as __e:\n"
        "    __results.append(['FAIL', str(__e)])\n"
        "except BaseException as __e:\n"
        "    __results.append(['ERROR', type(__e).__name__ + ': ' + str(__e)])\n"
        "else:\n"
        "    __results.append(['PASS', ''])\n"
    )
    return ast.parse(source).body[0]


def _wrap_raise(node: ast.Raise) -> ast.stmt:
    """یک raise از نوع AssertionError را به ثبت نتیجه‌ی ناموفق تبدیل می‌کند."""
    message = ""
    exc = node.exc
    if isinstance(exc, ast.Call) and exc.args:
        first = exc.args[0]
        if isinstance(first, ast.Constant) and isinstance(first.value, str):
            message = first.value
    source = f"__results.append(['FAIL', {message!r}])"
    return ast.parse(source).body[0]


def _transform(statements: list[ast.stmt]) -> list[ast.stmt]:
    """بازگشتی: هر assert/raise درون بلوک‌های تودرتو را هم پیدا می‌کند."""
    result: list[ast.stmt] = []

    for stmt in statements:
        if isinstance(stmt, ast.Assert):
            result.append(_wrap_assert(stmt))
            continue

        if isinstance(stmt, ast.Raise):
            result.append(_wrap_raise(stmt))
            continue

        if isinstance(stmt, ast.Try):
            stmt.body = _transform(stmt.body)
            stmt.handlers = [
                type(handler)(**{**handler.__dict__, "body": _transform(handler.body)})
                for handler in stmt.handlers
            ]
            stmt.orelse = _transform(stmt.orelse)
            stmt.finalbody = _transform(stmt.finalbody)
            result.append(stmt)
            continue

        if isinstance(stmt, (ast.If, ast.While)):
            stmt.body = _transform(stmt.body)
            stmt.orelse = _transform(stmt.orelse)
            result.append(stmt)
            continue

        if isinstance(stmt, (ast.For, ast.AsyncFor)):
            stmt.body = _transform(stmt.body)
            stmt.orelse = _transform(stmt.orelse)
            result.append(stmt)
            continue

        if isinstance(stmt, (ast.With, ast.AsyncWith)):
            stmt.body = _transform(stmt.body)
            result.append(stmt)
            continue

        result.append(stmt)

    return result


def _find_main_block(tree: ast.Module) -> ast.If | None:
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            test = node.test
            if (
                isinstance(test, ast.Compare)
                and isinstance(test.left, ast.Name)
                and test.left.id == "__name__"
                and len(test.comparators) == 1
                and isinstance(test.comparators[0], ast.Constant)
                and test.comparators[0].value == "__main__"
            ):
                return node
    return None


def build_check_script(user_code: str, tests_source: str) -> str | None:
    """اسکریپتی می‌سازد که همه‌ی تست‌ها را جداگانه اجرا می‌کند.

    خروجی روی stdout به شکل یک خط JSON با پیشوند مخصوص چاپ می‌شود.
    """
    if not tests_source.strip():
        return None

    try:
        tree = ast.parse(tests_source)
    except SyntaxError:
        return None

    main_block = _find_main_block(tree)
    if main_block is None:
        return None

    body = _transform(main_block.body)
    if not body:
        return None

    # هر تست در یک try/except جداگانه تا خطای یک تست، بقیه را از کار نیندازد
    guarded: list[ast.stmt] = []
    for stmt in body:
        source = (
            "try:\n"
            + "\n".join("    " + line for line in ast.unparse(stmt).splitlines())
            + "\n"
            "except BaseException as __e:\n"
            "    __results.append(['ERROR', type(__e).__name__ + ': ' + str(__e)])\n"
        )
        guarded.append(ast.parse(source).body[0])

    module = ast.Module(body=guarded, type_ignores=[])
    try:
        test_code = ast.unparse(module)
    except Exception:  # noqa: BLE001
        return None

    template = '''# -*- coding: utf-8 -*-
import json as __json

__results = []

__USER_CODE = {user_code!r}

try:
    exec(compile(__USER_CODE, "<user_code>", "exec"), globals())
except BaseException as __e:
    __results.append(["ERROR", "کد شما اجرا نشد → " + type(__e).__name__ + ": " + str(__e)])

{test_code}

print({marker!r} + __json.dumps(__results, ensure_ascii=False))
'''

    return template.format(
        user_code=user_code,
        test_code=test_code,
        marker=RESULTS_MARKER,
    )


def parse_results(stdout: str) -> list[dict] | None:
    """نتیجه‌ها را از خروجی اسکریپت بیرون می‌کشد."""
    for line in stdout.splitlines():
        line = line.strip()
        if line.startswith(RESULTS_MARKER):
            import json

            try:
                raw = json.loads(line[len(RESULTS_MARKER):])
            except (ValueError, TypeError):
                return None
            out = []
            for item in raw:
                if not isinstance(item, (list, tuple)) or len(item) < 2:
                    continue
                out.append({"status": item[0], "message": item[1]})
            return out
    return None
