/* ══════════════════════════════════════════════════════════════
   رندرکننده‌ی Markdown — سبک و آفلاین
   پشتیبانی: عنوان‌ها، کد بلوکی، جدول، فهرست، نقل‌قول، خط جداکننده،
             کد درون‌خطی، بولد، ایتالیک، خط‌خورده، پیوند
   ══════════════════════════════════════════════════════════════ */

window.MD = (function () {
  "use strict";

  var ESCAPES = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" };

  function escapeHtml(text) {
    return String(text).replace(/[&<>"]/g, function (ch) {
      return ESCAPES[ch];
    });
  }

  function escapeAttr(text) {
    return escapeHtml(text).replace(/'/g, "&#39;");
  }

  /* ── متن درون‌خطی ── */
  function inline(text) {
    var codes = [];
    var out = String(text);

    // ۱) کد درون‌خطی را اول بیرون بکش تا محتوایش دست‌نخورده بماند
    out = out.replace(/`([^`\n]+)`/g, function (_, code) {
      codes.push(code);
      return "\u0000CODE" + (codes.length - 1) + "\u0000";
    });

    out = escapeHtml(out);

    // ۲) پیوندها
    out = out.replace(
      /\[([^\]]+)\]\(([^)\s]+)\)/g,
      function (_, label, href) {
        var safe = escapeAttr(href);
        return (
          '<a href="' + safe + '" target="_blank" rel="noopener noreferrer">' +
          label +
          "</a>"
        );
      }
    );

    // ۳) بولد، ایتالیک، خط‌خورده
    out = out.replace(/\*\*\*([^*]+)\*\*\*/g, "<strong><em>$1</em></strong>");
    out = out.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    out = out.replace(/(^|[\s(])_([^_\n]+)_/g, "$1<em>$2</em>");
    out = out.replace(/(^|[\s(])\*([^*\n]+)\*/g, "$1<em>$2</em>");
    out = out.replace(/~~([^~]+)~~/g, "<del>$1</del>");

    // ۴) کدهای درون‌خطی را برگردان
    out = out.replace(/\u0000CODE(\d+)\u0000/g, function (_, index) {
      return "<code>" + escapeHtml(codes[Number(index)]) + "</code>";
    });

    return out;
  }

  /* ── تشخیص نوع بلوک جدول ── */
  function isTableDivider(line) {
    return /^\s*\|?[\s:|-]+\|[\s:|-]*$/.test(line) && line.indexOf("-") !== -1;
  }

  function splitRow(line) {
    var trimmed = line.trim();
    if (trimmed.charAt(0) === "|") trimmed = trimmed.slice(1);
    if (trimmed.charAt(trimmed.length - 1) === "|") trimmed = trimmed.slice(0, -1);

    var cells = [];
    var current = "";
    var escaped = false;
    for (var i = 0; i < trimmed.length; i++) {
      var ch = trimmed.charAt(i);
      if (escaped) {
        current += ch;
        escaped = false;
      } else if (ch === "\\") {
        escaped = true;
      } else if (ch === "|") {
        cells.push(current.trim());
        current = "";
      } else {
        current += ch;
      }
    }
    cells.push(current.trim());
    return cells;
  }

  /* ── رندر اصلی ── */
  function render(markdown) {
    if (!markdown) return "";

    var src = String(markdown).replace(/\r\n/g, "\n");

    // ۱) بلوک‌های کد را جدا کن
    var blocks = [];
    src = src.replace(/```([\w+-]*)\n([\s\S]*?)```/g, function (_, lang, code) {
      blocks.push({ lang: lang || "", code: code.replace(/\n$/, "") });
      return "\u0000FENCE" + (blocks.length - 1) + "\u0000";
    });

    var lines = src.split("\n");
    var html = [];
    var i = 0;

    function flushParagraph(buffer) {
      if (!buffer.length) return;
      html.push("<p>" + inline(buffer.join(" ")) + "</p>");
      buffer.length = 0;
    }

    var paragraph = [];

    while (i < lines.length) {
      var line = lines[i];

      /* بلوک کد */
      var fenceMatch = line.match(/^\u0000FENCE(\d+)\u0000$/);
      if (fenceMatch) {
        flushParagraph(paragraph);
        var block = blocks[Number(fenceMatch[1])];
        html.push(
          '<pre><code class="lang-' +
            escapeAttr(block.lang || "python") +
            '">' +
            escapeHtml(block.code) +
            "</code></pre>"
        );
        i++;
        continue;
      }

      /* خط خالی */
      if (!line.trim()) {
        flushParagraph(paragraph);
        i++;
        continue;
      }

      /* خط جداکننده */
      if (/^\s*([-*_])\s*\1\s*\1[\s\-*_]*$/.test(line)) {
        flushParagraph(paragraph);
        html.push("<hr />");
        i++;
        continue;
      }

      /* عنوان */
      var heading = line.match(/^(#{1,6})\s+(.*)$/);
      if (heading) {
        flushParagraph(paragraph);
        var level = heading[1].length;
        var slug = slugify(heading[2]);
        html.push(
          "<h" +
            level +
            ' id="' +
            slug +
            '">' +
            inline(heading[2].replace(/\s*#+\s*$/, "")) +
            "</h" +
            level +
            ">"
        );
        i++;
        continue;
      }

      /* نقل‌قول */
      if (/^\s*>\s?/.test(line)) {
        flushParagraph(paragraph);
        var quote = [];
        while (i < lines.length && /^\s*>\s?/.test(lines[i])) {
          quote.push(lines[i].replace(/^\s*>\s?/, ""));
          i++;
        }
        html.push("<blockquote><p>" + inline(quote.join(" ")) + "</p></blockquote>");
        continue;
      }

      /* جدول */
      if (line.indexOf("|") !== -1 && i + 1 < lines.length && isTableDivider(lines[i + 1])) {
        flushParagraph(paragraph);
        var header = splitRow(line);
        i += 2;
        var body = [];
        while (i < lines.length && lines[i].indexOf("|") !== -1 && lines[i].trim()) {
          body.push(splitRow(lines[i]));
          i++;
        }
        var table = ["<table><thead><tr>"];
        header.forEach(function (cell) {
          table.push("<th>" + inline(cell) + "</th>");
        });
        table.push("</tr></thead><tbody>");
        body.forEach(function (row) {
          table.push("<tr>");
          for (var c = 0; c < header.length; c++) {
            table.push("<td>" + inline(row[c] || "") + "</td>");
          }
          table.push("</tr>");
        });
        table.push("</tbody></table>");
        html.push(table.join(""));
        continue;
      }

      /* فهرست شماره‌دار (اعداد فارسی هم پشتیبانی می‌شود) */
      if (/^\s*[0-9۰-۹]+[.)]\s+/.test(line)) {
        flushParagraph(paragraph);
        var ordered = [];
        while (i < lines.length && /^\s*[0-9۰-۹]+[.)]\s+/.test(lines[i])) {
          var om = lines[i].match(/^\s*[0-9۰-۹]+[.)]\s+(.*)$/);
          ordered.push(om[1]);
          i++;
        }
        html.push(
          "<ol>" +
            ordered
              .map(function (item) {
                return "<li>" + inline(item) + "</li>";
              })
              .join("") +
            "</ol>"
        );
        continue;
      }

      /* فهرست نشانه‌دار */
      if (/^\s*[-*+]\s+/.test(line)) {
        flushParagraph(paragraph);
        var unordered = [];
        while (i < lines.length && /^\s*[-*+]\s+/.test(lines[i])) {
          var um = lines[i].match(/^\s*[-*+]\s+(.*)$/);
          unordered.push(um[1]);
          i++;
        }
        html.push(
          "<ul>" +
            unordered
              .map(function (item) {
                return "<li>" + inline(item) + "</li>";
              })
              .join("") +
            "</ul>"
        );
        continue;
      }

      /* پاراگراف */
      paragraph.push(line.trim());
      i++;
    }

    flushParagraph(paragraph);

    return html.join("\n");
  }

  /* ── برگرفتن عنوان‌ها برای فهرست ── */
  function headings(markdown) {
    var out = [];
    var re = /^(#{1,4})\s+(.*)$/gm;
    var match;
    while ((match = re.exec(markdown)) !== null) {
      out.push({
        level: match[1].length,
        text: match[2].replace(/[*`]/g, "").trim(),
        id: slugify(match[2]),
      });
    }
    return out;
  }

  function slugify(text) {
    var clean = String(text)
      .replace(/[*`]/g, "")
      .replace(/[^\w؀-ۿ\s-]/g, "")
      .trim()
      .replace(/\s+/g, "-")
      .slice(0, 48);
    return clean || "h";
  }

  return { render: render, headings: headings, escapeHtml: escapeHtml, inline: inline };
})();
