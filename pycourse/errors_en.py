"""
English translation of Python error diagnoses.

This module takes a raw Python traceback and converts it into a readable
"diagnosis": what happened? why? what to do?

No external dependencies.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field

# ─────────────────────────────────────────────────────────────
# Output model
# ─────────────────────────────────────────────────────────────


@dataclass
class Diagnosis:
    """An error diagnosis in English."""

    kind: str = ""  # Name of the Python error, like NameError
    message: str = ""  # Main Python error message
    line: int | None = None  # Line number
    source: str = ""  # The line of code
    title: str = ""  # Short English title
    what: str = ""  # What happened?
    why: str = ""  # Why did this happen?
    fix: list[str] = field(default_factory=list)  # What to do?
    category: str = "error"  # error | warning | info

    def to_dict(self) -> dict:
        return asdict(self)


# ─────────────────────────────────────────────────────────────
# Traceback parsing
# ─────────────────────────────────────────────────────────────

_FRAME_RE = re.compile(r'^\s*File "(?P<file>.+?)", line (?P<line>\d+)(?:, in (?P<func>.+))?\s*$')
_EXC_RE = re.compile(r"^(?P<kind>[A-Za-z_][A-Za-z0-9_]*(?:Error|Exception|Warning|Exit|Interrupt))(?::\s*(?P<msg>.*))?$")
_CARET_RE = re.compile(r"^\s*\^\s*$")


def _clean_source(line: str) -> str:
    """Extract the code line from a traceback."""
    return line.strip()


def parse_traceback(stderr: str) -> tuple[str, str, int | None, str]:
    """Parse Python stderr output.

    Returns: (error_type, message, line_number, code_line)
    """
    if not stderr:
        return "", "", None, ""

    lines = stderr.replace("\r\n", "\n").split("\n")

    # --- Find the last traceback frame ---
    last_frame_line: int | None = None
    last_func = ""
    source = ""
    for i, raw in enumerate(lines):
        m = _FRAME_RE.match(raw)
        if m:
            last_frame_line = int(m.group("line"))
            last_func = (m.group("func") or "").strip()
            # The next line is the code
            if i + 1 < len(lines):
                source_candidate = lines[i + 1]
                if not _CARET_RE.match(source_candidate) and not _FRAME_RE.match(source_candidate):
                    source = _clean_source(source_candidate)
                else:
                    source = ""
            else:
                source = ""

    # --- Find the last line that declares the error kind ---
    kind = ""
    message = ""
    for raw in reversed(lines):
        raw = raw.strip()
        if not raw:
            continue
        m = _EXC_RE.match(raw)
        if m:
            kind = m.group("kind")
            message = (m.group("msg") or "").strip()
            break
        # If the last line is an ExceptionInfo (e.g. SyntaxError with more details)
        if raw.startswith(("SyntaxError:", "IndentationError:")):
            kind, _, message = raw.partition(":")
            kind = kind.strip()
            message = message.strip()
            break

    # SyntaxError sometimes has multi-line message
    if kind in ("SyntaxError", "IndentationError", "TabError") and "was never closed" not in message:
        pass

    return kind, message, last_frame_line, source


def split_suggestion(message: str) -> tuple[str, str]:
    """Python 3.12+ adds 'Did you mean ...?' to error messages.

    We separate this so we can match patterns on the main message
    and still show the suggestion to the learner.
    """
    for marker in (". Did you mean", ". Or did you forget"):
        if marker in message:
            head, _, tail = message.partition(marker)
            return head.strip(), (marker + tail).strip()
    return message.strip(), ""


# ─────────────────────────────────────────────────────────────
# Diagnosis rules
# ─────────────────────────────────────────────────────────────
# Each rule: (regex pattern on error message, title, what happened, why, list of fixes)

Rule = tuple[re.Pattern, str, str, str, list[str]]

RULES: list[Rule] = [
    # ── NameError ───────────────────────────────────────────
    (
        re.compile(r"^name '(?P<name>[^']+)' is not defined$"),
        "Undefined variable",
        "Python couldn't find the name you used in your code.",
        "Before using any variable, you need to define it (e.g. `x = 5`). "
        "You may have misspelled it or not defined it at all.",
        [
            "Check the name exactly against a definition — case matters.",
            "Define the variable before using it: `{name} = ...`",
            "If inside a function, remember that a variable assigned there is local "
            "to that function (or use `global` to make it outer).",
        ],
    ),
    # ── IndentationError / TabError ─────────────────────────
    (
        re.compile(r"expected an indented block"),
        "Indentation error",
        "A block was expected after this line but wasn't received.",
        "In Python, blocks are defined by indentation. Any line inside "
        "`if` or a loop must be indented 4 spaces.",
        [
            "Indent the next line 4 spaces.",
            "You can select the whole file and press `Shift+Alt+F` in VS Code to format it.",
        ],
    ),
    (
        re.compile(r"unindent does not match|unexpected indent"),
        "Inconsistent indentation",
        "The indentation of one line doesn't match the previous line.",
        "All blocks must have exactly 4 spaces (or all tabs). Python doesn't mix tabs and spaces.",
        [
            "Make all indentation consistent: 4 spaces for each level.",
            "Use VS Code's «Convert indentation to tab» or vice versa.",
        ],
    ),
    (
        re.compile(r"inconsistent use of tabs and spaces"),
        "Mix of tabs and spaces",
        "Some lines in the file have tab indentation and some have spaces.",
        "Python can't decide which to treat as 4 spaces.",
        ["Format the whole file with 4 consistent spaces."],
    ),
    # ── SyntaxError ─────────────────────────────────────────
    (
        re.compile(r"invalid syntax"),
        "Syntax error",
        "The code you wrote is not valid Python syntax.",
        "Most common causes: `=` instead of `==` in a condition, missing `:`, "
        "or writing `print` without parentheses.",
        [
            "If inside `if` or a loop, the end of the line must have `:`",
            "In conditions, swap `=` for `==`",
            "The full error message usually says exactly where the problem is — read that line.",
        ],
    ),
    (
        re.compile(r"was never closed"),
        "Unclosed parenthesis or quote",
        "You opened a `(` or `[` or `\"` but didn't close it.",
        "Every opened parenthesis must have a closing one.",
        [
            "Count the parentheses: `(` and `)` must be equal.",
            "Same applies for `[` `]` and `{` `}`.",
        ],
    ),
    (
        re.compile(r"cannot assign to"),
        "Invalid assignment",
        "Python doesn't allow this kind of assignment.",
        "For example, you can't assign a value to a function or a constant.",
        [
            "Make sure the variable is a valid name and not a keyword.",
            "If you want to assign a new value in a loop, use `+=` or `=`.",
        ],
    ),
    # ── TypeError ───────────────────────────────────────────
    (
        re.compile(r"can only concatenate str \(not \"(?P<t>[^\"]+)\"\) to str"),
        "Concatenating string with number",
        "You tried to concatenate a string with a number, but Python can't do that.",
        "In Python, `str` and `int` can't be directly glued together.",
        "The main reason: `input()` always returns a **string**.",
        [
            "Convert `input()` output: `int(input(...))`",
            "Or convert a number to string: `str(number)`",
            "Use f-strings for concatenation: `f'Value: {x}'`",
        ],
    ),
    (
        re.compile(r"unsupported operand type\(s\) for (?P<op>[^:]+): '(?P<a>[^']+)' and '(?P<b>[^']+)'"),
        "Unsupported operator for types",
        "This operator can't be used on these types of data.",
        "For example, `+` on `str` and `int` doesn't work. The most common reason: "
        "one of the sides ended up as a string.",
        [
            "Check the type of both sides with `print(type(x))`",
            "If one came from `input()`, convert it.",
        ],
    ),
    (
        re.compile(r"'(?P<t>[^']+)' object is not callable"),
        "Not callable",
        "You tried to call something that isn't a function.",
        "Either you called a name as a function when it's not, or you forgot parentheses.",
        [
            "If you wanted to call a function's value, add parentheses: `f()`",
            "If you're calling a method on an object, make sure that object supports it.",
        ],
    ),
    (
        re.compile(r"takes (?P<n>\d+) positional arguments? but (?P<m>\d+) (?:was|were) given"),
        "Wrong number of arguments",
        "You called a function with a different number of arguments than it expects.",
        "The function signature defines how many arguments it takes. Default arguments count too.",
        ["Check the function definition: `def f(a, b=2)` means 1 to 2 arguments."],
    ),
    (
        re.compile(r"missing (?P<n>\d+) required positional argument"),
        "Missing required argument",
        "The function you called requires more arguments.",
        "Functions you define yourself can also have required arguments.",
        ["Check the function signature and the number and order of your arguments."],
    ),
    # ── ValueError ──────────────────────────────────────────
    (
        re.compile(r"invalid literal for int\(\) with base 10: '(?P<v>[^']*)'"),
        "Invalid literal for int()",
        "You tried to convert a string to an integer but its content isn't a number.",
        "The `int()` function only accepts strings that are themselves numbers.",
        [
            "Use `try/except ValueError` if the input might not be a number.",
            "For decimals use `float()` instead of `int()`.",
            "To remove extra spaces: `int(text.strip())`",
        ],
    ),
    (
        re.compile(r"invalid literal for int\(\)"),
        "Invalid literal for int()",
        "The string you wanted to convert to a number wasn't a number.",
        "`int()` only accepts integer numbers.",
        [
            "Use `try/except ValueError`.",
            "If it's a decimal, use `float()` and if you need zero: `int(float(x))`.",
        ],
    ),
    (
        re.compile(r"not enough values to unpack"),
        "Not enough values to unpack",
        "You tried to unpack a tuple into fewer variables than it has values.",
        "For example, `a, b = [1]` fails because there's only one value.",
        ["Make the number of variables match the number of elements."],
    ),
    (
        re.compile(r"too many values to unpack"),
        "Too many values to unpack",
        "You tried to unpack a tuple into more variables than it has values.",
        "For example, `a, b = [1, 2, 3]` fails.",
        ["Use `*rest`: `a, b, *rest = [1, 2, 3]`"],
    ),
    # ── IndexError / KeyError ────────────────────────────────
    (
        re.compile(r"list index out of range|index out of range"),
        "Index out of range",
        "You referred to a list cell that doesn't exist.",
        "List indices start at 0 and the last index is `len(list) - 1`. Negative indices count from the end.",
        [
            "Use `for` for safe iteration, not `while i < len(x)`.",
            "Negative index `-1` is the last element.",
        ],
    ),
    (
        re.compile(r"^'(?P<k>[^']+)'$"),
        "Key error",
        "The key you wanted in a dictionary doesn't exist.",
        "A dictionary only has keys that have been added before.",
        [
            "Use `d.get(key)` instead of `d[key]` which returns `None` instead of an error.",
            "For nested dicts: `d.get(\"a\", {}).get(\"b\")`",
        ],
    ),
    # ── ZeroDivisionError ───────────────────────────────────
    (
        re.compile(r"division by zero"),
        "Division by zero",
        "The divisor became zero.",
        "Python doesn't allow division by zero.",
        [
            "Check the divisor before dividing.",
            "For dictionary keys, `d.get(k, 0)` is better than `d[k]`.",
        ],
    ),
    # ── AttributeError ──────────────────────────────────────
    (
        re.compile(r"'(?P<t>[^']+)' object has no attribute '(?P<a>[^']+)'"),
        "Attribute not found",
        "On this object, such a property or method is not defined.",
        "Every data type has its own methods. For example, `str` has no `append` method "
        "and `list` has no `upper` method.",
        [
            "Make sure the variable type is what you think: `print(type(x))`",
            "For text use `str.strip()` and `str.upper()`, for lists use `list.append()`.",
        ],
    ),
    # ── FileNotFoundError ───────────────────────────────────
    (
        re.compile(r"No such file or directory"),
        "File not found",
        "The file you wanted to open doesn't exist on disk.",
        "The path is resolved relative to **the folder running the script**, not the terminal.",
        [
            "Print the path: `print(Path('data.txt').absolute())`",
            "If the file might not exist: `if path.exists():`",
            "Use `pathlib`: `Path(\"data\") / \"f.txt\"`",
        ],
    ),
    (
        re.compile(r"No module named '(?P<m>[^']+)'"),
        "Module not found",
        "The module you `import`ed isn't installed on this Python.",
        "External libraries aren't part of Python and must be installed separately.",
        [
            "Install it with `pip install <module-name>`.",
            "Make sure you're installing in the same environment you're running Python in: `python -m pip install ...`",
        ],
    ),
    # ── AssertionError (from our exercise tests) ───────────────
    (
        re.compile(r"^$"),
        "Assertion error",
        "Your code ran without error, but the result differs from what was expected.",
        "The tests expect a specific value. The message above tells which value.",
        [
            "See the actual value by printing: `print(type(x), repr(x))` — `3` and `3.0` differ.",
            "Read the lower test files; they exactly say what's required.",
            "If the data type is wrong, use `int()` or `float()` for conversion.",
        ],
    ),
    # ── Other ────────────────────────────────────────────────
    (
        re.compile(r"maximum recursion depth exceeded"),
        "Infinite recursion",
        "A function calls itself forever and never reaches the base case.",
        "Usually the base case (stop condition) is missing or wrong.",
        ["Add a base case that stops the recursion."],
    ),
    (
        re.compile(r"local variable '([^']+)' referenced before assignment"),
        "Variable referenced before assignment",
        "A variable created inside a function was used before it got a value.",
        "If you assign a name inside a function, it becomes **local** — even if it exists outside the function too.",
        [
            "Define the variable before using it.",
            "If you want to change an outer variable: `global x` — but better to pass it as an argument and return it.",
        ],
    ),
    (
        re.compile(r"unhashable type"),
        "Unhashable type for dictionary key",
        "What you used as a key isn't usable as a dictionary key.",
        "Dictionary keys must be hashable: numbers, strings, or tuples. Lists and dicts aren't.",
        ["Instead of a list, use a tuple: `(1, 2)` instead of `[1, 2]`"],
    ),
    (
        re.compile(r"list object is not iterable|is not iterable"),
        "Not iterable",
        "You put a `for` loop on something that isn't a collection.",
        "Only strings, lists, tuples, dicts, and sets are iterable. Numbers (`int`) and others aren't.",
        [
            "First check `None` isn't the value, then convert to a list.",
        ],
    ),
]


# ─────────────────────────────────────────────────────────────
# Final diagnosis
# ─────────────────────────────────────────────────────────────


def _fallback(kind: str, message: str, line: int | None = None, source: str = "") -> Diagnosis:
    """When no specific rule matched."""
    pretty = {
        "NameError": "Undefined variable",
        "TypeError": "Unsupported operator",
        "ValueError": "Invalid value",
        "IndexError": "Index out of range",
        "KeyError": "Key not found",
        "AttributeError": "Attribute not found",
        "ZeroDivisionError": "Division by zero",
        "FileNotFoundError": "File not found",
        "ModuleNotFoundError": "Module not found",
        "IndentationError": "Indentation error",
        "TabError": "Mixed tabs and spaces",
        "SyntaxError": "Syntax error",
        "RecursionError": "Infinite recursion",
        "UnboundLocalError": "Variable referenced before assignment",
        "AssertionError": "Assertion error",
        "MemoryError": "Out of memory",
        "KeyboardInterrupt": "Interrupted by user",
        "StopIteration": "Stopped without reason",
        "SystemExit": "Exit the program",
    }.get(kind, "Unknown error")

    return Diagnosis(
        kind=kind,
        message=message,
        line=line,
        source=source,
        title=pretty,
        what=f"Program stopped with a `{kind}` error.",
        why=message or "No exact message was available.",
        fix=[
            "Read the last error message — it usually tells the problem itself.",
            "Find the line number in the traceback and locate that line in your code.",
        ],
    )


def diagnose(stderr: str) -> Diagnosis | None:
    """Convert raw traceback into an English diagnosis."""
    kind, message, line, source = parse_traceback(stderr)
    if not kind:
        return None

    base, suggestion = split_suggestion(message)

    for pattern, title, what, why, fix in RULES:
        m = pattern.search(base)
        if not m:
            continue

        # Special fix: NameError about self
        if kind == "NameError":
            g = m.groupdict()
            if g.get("name") == "self":
                return Diagnosis(
                    kind=kind,
                    message=message,
                    line=line,
                    source=source,
                    title="`self` undefined",
                    what="You referenced `self` inside a method but didn't receive it as an argument.",
                    why="Methods in classes always take `self` as the first argument. "
                    "If you call it yourself, you must pass it manually.",
                    fix=[
                        "Method definition: `def method(self):` — not `def method():`",
                        "Calling it: `obj.method()` provides `self` automatically.",
                    ],
                )

        # Special fix: ModuleNotFoundError — bring the module name into the fix
        if kind == "ModuleNotFoundError":
            module = m.groupdict().get("m", "")
            return Diagnosis(
                kind=kind,
                message=message,
                line=line,
                source=source,
                title="Module not found",
                what=f"Module `{module}` is not installed on this Python.",
                why="External libraries are not part of Python and must be installed separately.",
                fix=[
                    f"Install it with `pip install {module}`.",
                    "If you have a virtual environment, activate it first.",
                    f"Install in the same Python: `python -m pip install {module}`",
                ],
            )

        return Diagnosis(
            kind=kind,
            message=message,
            line=line,
            source=source,
            title=title,
            what=what,
            why=why,
            fix=list(fix) + ([suggestion] if suggestion else []),
        )

    return _fallback(kind, message, line, source)


def diagnose_assertion(message: str, line: int | None = None, source: str = "") -> Diagnosis:
    """For AssertionError from our own exercise tests (they have English messages)."""
    return Diagnosis(
        kind="AssertionError",
        message=message,
        line=line,
        source=source,
        title="Assertion error",
        what=message or "The code result differs from the expected value.",
        why="The code ran without error, but the result differs from what was expected. "
        "The message above says what value was expected.",
        fix=[
            "See the actual value: `print(repr(x))` — `3` and `3.0` differ.",
            "Read the lower test files; they exactly say what's required.",
            "If the data type is wrong, use `int()` or `float()` for conversion.",
        ],
    )