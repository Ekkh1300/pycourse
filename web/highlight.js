/* ══════════════════════════════════════════════════════════════
   رنگ‌آمیزی سینتکس پایتون — خالص، بدون کتابخانه
   خروجی: آرایه‌ای از خط‌های HTML (یکی به ازای هر خط کد)
   ══════════════════════════════════════════════════════════════ */

window.Highlight = (function () {
  "use strict";

  var KEYWORDS = new Set([
    "False","None","True","and","as","assert","async","await","break","class",
    "continue","def","del","elif","else","except","finally","for","from",
    "global","if","import","in","is","lambda","nonlocal","not","or","pass",
    "raise","return","try","while","with","yield","match","case",
  ]);

  var BUILTINS = new Set([
    "abs","all","any","bool","bytes","callable","chr","dict","dir","divmod",
    "enumerate","eval","filter","float","format","frozenset","getattr","hasattr",
    "hash","help","id","input","int","isinstance","issubclass","iter","len",
    "list","map","max","min","next","object","oct","open","ord","pow","print",
    "range","repr","reversed","round","set","setattr","slice","sorted","str",
    "sum","super","tuple","type","vars","zip","self","cls","Exception",
    "ValueError","TypeError","NameError","KeyError","IndexError","ZeroDivisionError",
    "AttributeError","FileNotFoundError","AssertionError","NotImplementedError",
  ]);

  var TOKEN_RE = new RegExp(
    [
      "(?:[rRbBuUfF]{1,3})?'''(?:\\\\.|[^\\\\])*?'''", // رشته‌ی سه‌تایی تک
      "(?:[rRbBuUfF]{1,3})?\"\"\"(?:\\\\.|[^\\\\])*?\"\"\"", // رشته‌ی سه‌تایی دوتایی
      "(?:[rRbBuUfF]{1,3})?'(?:\\\\.|[^'\\\\\\n])*'", // رشته‌ی تک‌تایی
      '(?:[rRbBuUfF]{1,3})?"(?:\\\\.|[^"\\\\\\n])*"', // رشته‌ی دوتایی
      "@[A-Za-z_][\\w.]*", // دکوراتور
      "#[^\\n]*", // توضیح
      "\\b\\d+(?:\\.\\d+)?(?:[eE][+-]?\\d+)?\\b", // عدد
      "\\b[A-Za-z_]\\w*\\b", // شناسه
      "\\s+", // فاصله
      "[^\\sA-Za-z0-9_]", // عملگر
    ].join("|"),
    "g"
  );

  function escapeHtml(text) {
    return String(text)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  function classify(text, prev) {
    var first = text.charAt(0);

    if (first === "#") {
      if (/^\s*#\s*TODO/i.test(text)) return "tok-todo";
      if (/^\s*#\s*[─═\-\u2500-\u257F]/.test(text)) return "tok-rule";
      return "tok-comment";
    }
    if (first === "@") return "tok-deco";
    if (first === '"' || first === "'") return "tok-string";
    if (/^[rRbBuUfF]{1,3}['"]/.test(text)) return "tok-string";
    if (/^\d/.test(text)) return "tok-number";

    if (/^[A-Za-z_]/.test(text)) {
      if (KEYWORDS.has(text)) return "tok-keyword";
      if (BUILTINS.has(text)) return "tok-builtin";
      if (prev && prev.type === "tok-keyword" && (prev.text === "def" || prev.text === "class")) {
        return "tok-def";
      }
      return "tok-plain";
    }

    if (/^\s+$/.test(text)) return "space";
    return "tok-op";
  }

  /* ── توکن‌سازی کل فایل ── */
  function tokenize(source) {
    var lines = [[]];
    var prev = null;
    var match;

    TOKEN_RE.lastIndex = 0;
    while ((match = TOKEN_RE.exec(source)) !== null) {
      var text = match[0];
      var type = classify(text, prev);

      // آیا بعد از این شناسه، پرانتز باز می‌آید؟ → نام تابع
      if (type === "tok-plain") {
        var after = source.slice(TOKEN_RE.lastIndex);
        if (/^\s*\(/.test(after)) type = "tok-func";
      }

      var parts = text.split("\n");
      for (var p = 0; p < parts.length; p++) {
        if (p > 0) lines.push([]);
        if (parts[p].length) {
          lines[lines.length - 1].push({ type: type, text: parts[p] });
        }
      }

      if (type !== "space") prev = { type: type, text: text };
      if (text.length === 0) TOKEN_RE.lastIndex++; // جلوگیری از حلقه‌ی بی‌پایان
    }

    return lines;
  }

  function renderTokens(tokens) {
    var out = [];
    for (var i = 0; i < tokens.length; i++) {
      var token = tokens[i];
      if (token.type === "space" || token.type === "tok-plain") {
        out.push(escapeHtml(token.text));
      } else {
        out.push('<span class="' + token.type + '">' + escapeHtml(token.text) + "</span>");
      }
    }
    return out.join("");
  }

  /* ── API عمومی ── */

  /** آرایه‌ای از HTML برای هر خط */
  function lines(source) {
    return tokenize(source || "").map(renderTokens);
  }

  /**
   * HTML کامل برای نمایش در لایه‌ی زیرِ ویرایشگر.
   * @param {string} source
   * @param {number|null} errorLine شماره‌ی خطی که باید قرمز شود (۱-based)
   */
  function toHtml(source, errorLine) {
    var rendered = lines(source);
    var body = rendered
      .map(function (html, index) {
        var lineNo = index + 1;
        if (errorLine && lineNo === errorLine) {
          return '<span class="hl-line-error">' + (html || " ") + "</span>";
        }
        return html || " ";
      })
      .join("\n");
    return body + "\n";
  }

  return { lines: lines, toHtml: toHtml, escapeHtml: escapeHtml };
})();
