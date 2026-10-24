/* ══════════════════════════════════════════════════════════════
   لایه‌ی API برای نسخه‌ی استاتیک (HTML تک‌فایلی)

   به‌جای سرور، کد پایتون داخل مرورگر با Pyodide اجرا می‌شود.
   منطق «تشخیص خطا به فارسی» و «تست جداگانه» همان کد پایتونِ
   سرور است که داخل Pyodide اجرا می‌شود — پس رفتار یکسان است.
   ══════════════════════════════════════════════════════════════ */

(function () {
  "use strict";

  var COURSE = window.__COURSE__ || {};
  var PROGRESS_KEY = "pycourse.progress.static";
  var pyodide = null;
  var loading = false;

  // ── پیشرفت ──
  function loadProgress() {
    try {
      var raw = localStorage.getItem(PROGRESS_KEY);
      if (raw) return JSON.parse(raw);
    } catch (e) { /* بی‌خیال */ }
    return {
      lessons_done: [],
      exercises_done: [],
      attempts: {},
      quiz_best: null,
      font_size: 15,
      theme: "amber",
      notes: {},
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
    if (loading) return window.__PYODIDE_READY__;
    loading = true;
    var toast = document.getElementById("toast");
    if (toast) {
      toast.textContent = "در حال بارگذاری موتور پایتون (اولین بار کمی طول می‌کشد)…";
      toast.hidden = false;
    }
    return window.loadPyodide().then(function (instance) {
      pyodide = instance;
      loading = false;
      if (toast) toast.hidden = true;
      return instance;
    });
  }

  function runPython(source) {
    return ensurePyodide().then(function (py) {
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
    });
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

      var diagPromise = diagnose(result.stderr);

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
        };
        if (mode === "check" && body.exercise_id) {
          payload.attempts = bumpAttempt(body.exercise_id);
        }
        return payload;
      });
    });
  }

  function findExercise(id) {
    var list = COURSE.exercises || [];
    for (var i = 0; i < list.length; i++) {
      if (list[i].id === id) return list[i];
    }
    // بعضی تمرین‌ها در پوشه‌ی پروژه‌ها هستند (مثل first_steps درس ۰).
    // سرور خودش به projects/ سر می‌زند؛ اینجا از قبل داخل داده‌ها هست.
    var extra = COURSE.extraExercises || {};
    return extra[id] || null;
  }

  function findLesson(id) {
    var list = COURSE.lessons || [];
    for (var i = 0; i < list.length; i++) {
      if (list[i].id === id) return list[i];
    }
    return null;
  }

  function findProject(id) {
    var list = COURSE.projects || [];
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
        return Promise.resolve({
          lessons: (COURSE.lessons || []).map(function (l) {
            return { id: l.id, number: l.id.split("_")[0], title: l.title };
          }),
          exercises: (COURSE.exercises || []).map(function (e) {
            return {
              id: e.id, number: e.number, title: e.title,
              description: e.description, filename: e.id + ".py",
              has_solution: e.has_solution,
            };
          }),
          projects: (COURSE.projects || []).map(function (p) {
            return { id: p.id, title: p.title, filename: p.id + ".md" };
          }),
          quiz_count: ((COURSE.quiz || {}).questions || []).length,
          python_version: "3.11 (Pyodide)",
        });
      }

      if (r.clean === "/api/progress") {
        return Promise.resolve(loadProgress());
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
          hints: (COURSE.hints || {})[ex.id] || COURSE.generalHints || [],
          attempts: (state.attempts || {})[ex.id] || 0,
        });
      }

      if (r.clean === "/api/hint") {
        var pool = (COURSE.hints || {})[r.query.exercise] || COURSE.generalHints || [];
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
        var solution = (COURSE.solutions || {})[r.query.id];
        if (!solution) {
          return Promise.resolve({ error: "برای این تمرین راه‌حل آماده نشده" });
        }
        return Promise.resolve({ locked: false, source: solution, note: "" });
      }

      if (r.clean === "/api/quiz_questions") {
        return Promise.resolve({
          questions: (COURSE.quiz || {}).questions || [],
          total: ((COURSE.quiz || {}).questions || []).length,
        });
      }

      if (r.clean === "/api/health") {
        return Promise.resolve({ ok: true, python: "pyodide" });
      }

      return Promise.resolve({ error: "مسیر پیدا نشد" });
    },

    post: function (path, body) {
      body = body || {};
      var r = route(path);

      if (r.clean === "/api/run") {
        return runCode(body);
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
        var bank = (COURSE.quiz || {}).questions || [];
        var key2 = (COURSE.quiz || {}).answers || [];
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
            why: (COURSE.quizWhys || [])[index] || "",
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
