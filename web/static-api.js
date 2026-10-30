/* ══════════════════════════════════════════════════════════════
   لایه‌ی API برای نسخه‌ی استاتیک (HTML تک‌فایلی)

   به‌جای سرور، کد پایتون داخل مرورگر با Pyodide اجرا می‌شود.
   منطق «تشخیص خطا به فارسی» و «تست جداگانه» همان کد پایتونِ
   سرور است که داخل Pyodide اجرا می‌شود — پس رفتار یکسان است.
   ══════════════════════════════════════════════════════════════ */

(function () {
  "use strict";

  var COURSE_BILINGUAL = window.__COURSE__ || {};
  var PROGRESS_KEY = "pycourse.progress.static";

  function currentLanguage() {
    return loadProgress().lang === "fa" ? "fa" : "en";
  }

  function courseData(lang) {
    lang = lang === "fa" ? "fa" : (lang === "en" ? "en" : currentLanguage());
    if (COURSE_BILINGUAL.en || COURSE_BILINGUAL.fa) {
      return COURSE_BILINGUAL[lang] || COURSE_BILINGUAL.en || {};
    }
    return COURSE_BILINGUAL;
  }

  var COURSE = courseData();
  var pyodide = null;
  /* وعده‌ی در جریانِ بارگذاری.

     قبلاً `loading` یک بولین بود و در صورت شکست هیچ‌وقت ریست نمی‌شد؛ بعد
     هر فراخوانی بعدی `window.__PYODIDE_READY__` را برمی‌گرداند که چون تابع
     بارگذار داخل IIFE بود همیشه `null` بود → `.then` روی null → TypeError
     همزمان → `.catch` هیچ‌وقت وصل نمی‌شد → دکمه‌ها برای همیشه `is-busy`
     می‌ماندند و `pointer-events: none` آن‌ها را از کار می‌انداخت. */
  var pendingPyodide = null;
  /* صف اجرا: دو اجرای همزمان `setStdout` را از هم می‌دزدند چون روی خودِ
     نمونه‌ی Pyodide سراسری است و خروجی‌ها قاطی می‌شود. */
  var runQueue = Promise.resolve();

  // ── پیشرفت ──
  function loadProgress() {
    try {
      var raw = localStorage.getItem(PROGRESS_KEY);
      if (raw) {
        var state = JSON.parse(raw);
        if (state.lang !== "fa" && state.lang !== "en") state.lang = "en";
        return state;
      }
    } catch (e) { /* بی‌خیال */ }
    return {
      lessons_done: [],
      exercises_done: [],
      attempts: {},
      quiz_best: null,
      font_size: 15,
      theme: "amber",
      notes: {},
      lang: "en",
    };
  }

  function saveProgress(state) {
    try {
      localStorage.setItem(PROGRESS_KEY, JSON.stringify(state));
    } catch (e) { /* بی‌خیال */ }
  }

  function bumpAttempt(exerciseId) {
    var state = loadProgress();
    state.attempts = state.attempts || {};
    state.attempts[exerciseId] = (state.attempts[exerciseId] || 0) + 1;
    saveProgress(state);
    return state.attempts[exerciseId];
  }

  // ── Pyodide ──
  function ensurePyodide() {
    if (pyodide) return Promise.resolve(pyodide);
    // هیچ‌وقت null برنمی‌گردانیم؛ همیشه یک وعده‌ی معتبر برمی‌گردد
    if (pendingPyodide) return pendingPyodide;

    var toast = document.getElementById("toast");
    if (toast) {
      toast.dataset.locked = "1";
      toast.textContent = "در حال بارگذاری موتور پایتون (اولین بار کمی طول می‌کشد)…";
      toast.hidden = false;
    }

    pendingPyodide = Promise.resolve()
      .then(function () {
        return window.loadPyodide();
      })
      .then(function (instance) {
        pyodide = instance;
        pendingPyodide = null;
        if (toast) {
          toast.dataset.locked = "";
          toast.hidden = true;
        }
        return instance;
      })
      .catch(function (err) {
        // ریست، تا کاربر بتواند دوباره تلاش کند — نه دکمه‌ی مرده
        pendingPyodide = null;
        if (toast) {
          toast.dataset.locked = "";
          toast.textContent =
            "موتور پایتون بارگذاری نشد. دکمه را دوباره بزن تا از نو تلاش شود. (" +
            String((err && err.message) || err).slice(0, 120) +
            ")";
          toast.hidden = false;
        }
        throw err;
      });

    return pendingPyodide;
  }

  function runPython(source) {
    // اجراها را صف می‌کنیم تا setStdout هم‌زمان عوض نشود
    var task = runQueue
      .then(function () {
        return ensurePyodide();
      })
      .then(function (py) {
        var out = "";
        var err = "";
        py.setStdout({ batched: function (text) { out += text + "\n"; } });
        py.setStderr({ batched: function (text) { err += text + "\n"; } });
        return py
          .runPythonAsync(source)
          .then(function () {
            return { stdout: out, stderr: err, failed: false };
          })
          .catch(function (e) {
            err += String(e && e.message ? e.message : e);
            return { stdout: out, stderr: err, failed: true };
          });
      })
      .catch(function (e) {
        // بارگذاری ناموفق بود: خطا را به شکل نتیجه برمی‌گردانیم
        // (engine_failed تا تشخیص خطا دوباره موتور را بار نگذارد)
        return {
          stdout: "",
          stderr: String((e && e.message) || e),
          failed: true,
          engine_failed: true,
        };
      });

    // صف بدون توجه به نتیجه، فقط بعد از اتمام این کار جلو می‌رود
    runQueue = task.then(
      function () {},
      function () {}
    );
    return task;
  }

  // ── تشخیص خطا به فارسی (همان کد سرور، اجرا در Pyodide) ──
  function diagnose(stderr) {
    if (!stderr || !stderr.trim()) return Promise.resolve(null);
    var source =
      "import json as __json\n" +
      "exec(compile(" + JSON.stringify(window.__ERRORS_SRC__ || "") + ", 'errors_fa.py', 'exec'), globals())\n" +
      "__d = diagnose(" + JSON.stringify(stderr) + ")\n" +
      "print('__DIAG__' + __json.dumps(__d.to_dict() if __d else None, ensure_ascii=False))\n";

    return runPython(source).then(function (result) {
      var marker = result.stdout.indexOf("__DIAG__");
      if (marker === -1) return null;
      var json = result.stdout.slice(marker + 8).trim();
      try {
        return JSON.parse(json);
      } catch (e) {
        return null;
      }
    });
  }

  // ── اجرای کد ──
  function runCode(body) {
    var mode = body.mode || "run";
    var code = body.code || "";

    if (!code.trim()) {
      return Promise.resolve({
        stdout: "", stderr: "", diagnosis: null, returncode: null,
        duration_ms: 0, timed_out: false, mode: mode, tests: [],
      });
    }

    var start = Date.now();
    var source = code;

    if (mode === "check") {
      var exercise = findExercise(body.exercise_id);
      if (exercise) {
        source =
          "import json as __json\n" +
          "exec(compile(" + JSON.stringify(window.__TESTER_SRC__ || "") + ", 'tester.py', 'exec'), globals())\n" +
          "__script = build_check_script(" + JSON.stringify(code) + ", " +
          JSON.stringify(exercise.tests_part) + ")\n" +
          "if __script:\n" +
          "    exec(compile(__script, 'check.py', 'exec'), globals())\n";
      }
    }

    return runPython(source).then(function (result) {
      var duration = Date.now() - start;
      var tests = [];
      var stdout = result.stdout;

      if (mode === "check") {
        var marker = stdout.indexOf("__PYCOURSE_RESULTS__");
        if (marker !== -1) {
          var json = stdout.slice(marker + "__PYCOURSE_RESULTS__".length).trim();
          stdout = stdout.slice(0, marker).trim();
          try {
            tests = (JSON.parse(json) || []).map(function (item) {
              return { status: item[0], message: item[1] };
            });
          } catch (e) {
            tests = [];
          }
        }
      }

      // شکست موتور: تشخیص خطا خودش به Pyodide نیاز دارد، پس دوباره بارش نکن
      var diagPromise = result.engine_failed
        ? Promise.resolve(null)
        : diagnose(result.stderr);

      return diagPromise.then(function (diag) {
        var payload = {
          stdout: stdout,
          stderr: result.stderr && !diag ? result.stderr : "",
          raw_stderr: result.stderr,
          diagnosis: diag,
          returncode: result.failed ? 1 : 0,
          duration_ms: duration,
          timed_out: false,
          mode: mode,
          tests: tests,
          engine_failed: !!result.engine_failed,
        };
        if (mode === "check" && body.exercise_id) {
          payload.attempts = bumpAttempt(body.exercise_id);
        }
        return payload;
      });
    });
  }

  function findExercise(id) {
    var list = courseData().exercises || [];
    for (var i = 0; i < list.length; i++) {
      if (list[i].id === id) return list[i];
    }
    // بعضی تمرین‌ها در پوشه‌ی پروژه‌ها هستند (مثل first_steps درس ۰).
    // سرور خودش به projects/ سر می‌زند؛ اینجا از قبل داخل داده‌ها هست.
    var extra = courseData().extraExercises || {};
    return extra[id] || null;
  }

  function findLesson(id) {
    var list = courseData().lessons || [];
    for (var i = 0; i < list.length; i++) {
      if (list[i].id === id) return list[i];
    }
    return null;
  }

  function findProject(id) {
    var list = courseData().projects || [];
    for (var i = 0; i < list.length; i++) {
      if (list[i].id === id) return list[i];
    }
    return null;
  }

  // ── مسیریابی API ──
  function route(path) {
    var clean = path.split("?")[0];
    var query = {};
    var qIndex = path.indexOf("?");
    if (qIndex !== -1) {
      path.slice(qIndex + 1).split("&").forEach(function (pair) {
        var parts = pair.split("=");
        query[decodeURIComponent(parts[0])] = decodeURIComponent(parts[1] || "");
      });
    }
    return { clean: clean, query: query };
  }

  window.__API__ = {
    get: function (path) {
      var r = route(path);

      if (r.clean === "/api/curriculum") {
        var requestedLang = r.query.lang === "fa" ? "fa" : (r.query.lang === "en" ? "en" : currentLanguage());
        var selectedCourse = COURSE_BILINGUAL[requestedLang] || COURSE_BILINGUAL;
        return Promise.resolve({
          lang: requestedLang,
          lessons: (selectedCourse.lessons || []).map(function (l) {
            return { id: l.id, number: l.id.split("_")[0], title: l.title };
          }),
          exercises: (selectedCourse.exercises || []).map(function (e) {
            return {
              id: e.id, number: e.number, title: e.title,
              description: e.description, filename: e.id + ".py",
              has_solution: e.has_solution,
            };
          }),
          projects: (selectedCourse.projects || []).map(function (p) {
            return { id: p.id, title: p.title, filename: p.id + ".md" };
          }),
          quiz_count: ((selectedCourse.quiz || {}).questions || []).length,
          python_version: "3.11 (Pyodide)",
        });
      }

      if (r.clean === "/api/progress") {
        return Promise.resolve(loadProgress());
      }

      if (r.clean === "/api/health") {
        return Promise.resolve({ ok: true, python: "pyodide", lang: loadProgress().lang || "en" });
      }

      if (r.clean === "/api/doc") {
        var lesson = findLesson(r.query.id);
        if (lesson) {
          return Promise.resolve({ id: lesson.id, title: lesson.title, body: lesson.body });
        }
        var project = findProject(r.query.id);
        if (project) {
          return Promise.resolve({ id: project.id, title: project.title, body: project.body });
        }
        if (r.query.id === "first_steps") {
          return Promise.resolve({
            id: "first_steps", title: "اولین قدم‌ها",
            body: "# اولین قدم‌ها\n\nاین بخش در نسخه‌ی وب به‌صورت فایل پایتون است.\n",
            kind: "code",
          });
        }
        return Promise.resolve({ error: "سند پیدا نشد" });
      }

      if (r.clean === "/api/exercise") {
        var ex = findExercise(r.query.id);
        if (!ex) return Promise.resolve({ error: "تمرین پیدا نشد" });
        var state = loadProgress();
        return Promise.resolve({
          id: ex.id,
          title: ex.title,
          description: ex.description,
          source: ex.user_part + ex.tests_part,
          user_part: ex.user_part,
          tests_part: ex.tests_part,
          hints: (courseData().hints || {})[ex.id] || courseData().generalHints || [],
          attempts: (state.attempts || {})[ex.id] || 0,
        });
      }

      if (r.clean === "/api/hint") {
        var pool = (courseData().hints || {})[r.query.exercise] || courseData().generalHints || [];
        var level = Math.max(1, Math.min(parseInt(r.query.level, 10) || 1, pool.length));
        return Promise.resolve({
          level: level, total: pool.length, hint: pool[level - 1],
        });
      }

      if (r.clean === "/api/solution") {
        var state2 = loadProgress();
        var attempts = (state2.attempts || {})[r.query.id] || 0;
        if (attempts < 3) {
          return Promise.resolve({
            locked: true,
            attempts: attempts,
            needed: 3,
            message:
              "برای دیدن راه‌حل باید حداقل ۳ بار تلاش کنی. الان " +
              attempts + " بار تلاش کرده‌ای — اول راهنماها را بخوان.",
          });
        }
        var solution = (courseData().solutions || {})[r.query.id];
        if (!solution) {
          return Promise.resolve({ error: "برای این تمرین راه‌حل آماده نشده" });
        }
        return Promise.resolve({ locked: false, source: solution, note: "" });
      }

      if (r.clean === "/api/quiz" || r.clean === "/api/quiz_questions") {
        return Promise.resolve({
          questions: (courseData().quiz || {}).questions || [],
          total: ((courseData().quiz || {}).questions || []).length,
        });
      }

      return Promise.resolve({ error: "مسیر پیدا نشد" });
    },

    post: function (path, body) {
      body = body || {};
      var r = route(path);

      if (r.clean === "/api/run") {
        return runCode(body);
      }

      if (r.clean === "/api/set-language") {
        if (body.lang !== "fa" && body.lang !== "en") {
          return Promise.resolve({ error: "Invalid language" });
        }
        var languageState = loadProgress();
        languageState.lang = body.lang;
        saveProgress(languageState);
        return Promise.resolve({ ok: true, lang: body.lang });
      }

      if (r.clean === "/api/progress") {
        var state = loadProgress();
        if (body.section && body.item) {
          var key = body.section === "lessons" ? "lessons_done" : "exercises_done";
          var items = state[key] || [];
          var index = items.indexOf(body.item);
          var done;
          if (index === -1) {
            items.push(body.item);
            done = true;
          } else {
            items.splice(index, 1);
            done = false;
          }
          state[key] = items;
          saveProgress(state);
          return Promise.resolve({ done: done, state: state });
        }
        Object.keys(body).forEach(function (key) {
          if (key === "lessons_done" || key === "exercises_done") {
            state[key] = Array.from(new Set((state[key] || []).concat(body[key])));
          } else if (key === "attempts" || key === "notes") {
            state[key] = Object.assign({}, state[key] || {}, body[key]);
          } else {
            state[key] = body[key];
          }
        });
        saveProgress(state);
        return Promise.resolve({ state: state });
      }

      if (r.clean === "/api/quiz") {
        var answers = body.answers || [];
        var bank = (courseData().quiz || {}).questions || [];
        var key2 = (courseData().quiz || {}).answers || [];
        var results = [];
        var score = 0;
        bank.forEach(function (question, index) {
          var chosen = index < answers.length ? answers[index] : null;
          var correct = chosen === key2[index];
          if (correct) score += 1;
          results.push({
            index: index,
            chosen: chosen,
            correct_index: key2[index],
            is_correct: correct,
            why: (courseData().quizWhys || [])[index] || "",
            question: question.q,
            options: question.options,
          });
        });
        var total = bank.length;
        var percent = total ? Math.round((score / total) * 100) : 0;
        var state3 = loadProgress();
        if (state3.quiz_best == null || percent > state3.quiz_best) {
          state3.quiz_best = percent;
          saveProgress(state3);
        }
        return Promise.resolve({
          score: score, total: total, percent: percent, results: results,
        });
      }

      return Promise.resolve({ error: "مسیر پیدا نشد" });
    },
  };
})();
