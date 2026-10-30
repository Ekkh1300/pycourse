/* ══════════════════════════════════════════════════════════════
   ترمینال پایتون — منطق برنامه
   ══════════════════════════════════════════════════════════════ */

(function () {
  "use strict";

  /* ── وضعیت ── */
  var state = {
    curriculum: { lessons: [], exercises: [], projects: [] },
    progress: { lessons_done: [], exercises_done: [], attempts: {}, quiz_best: null },
    docId: null,
    docKind: "lesson",
    exerciseId: null,
    exercise: null,
    errorLine: null,
    consoleTab: "output",
    hintLevel: 0,
    timerStart: null,
    timerHandle: null,
    splitRatio: 46,
    consoleRatio: 34,
    lessonCache: {},
    paletteIndex: 0,
    paletteItems: [],
    lastResult: null,
    lang: "en",  /* current UI language: "en" or "fa" */
  };

  /* ── میان‌برها ── */
  var $ = function (id) { return document.getElementById(id); };

  var TEXT = {
    sidebarLessons: "Lessons", sidebarExercises: "Exercises", sidebarProjects: "Projects",
    docLesson: "Lesson", docExercise: "Exercise", docProject: "Project", docQuiz: "Quick Quiz", docScratch: "Free Note", docSearch: "Search", docDone: "Done",
    exerciseHints: "Hints", exerciseFullSolution: "Full solution", exerciseDone: "Done", exerciseUndone: "Undone", exerciseReset: "Code reset.", exerciseCopied: "Code copied.", exerciseSelectFirst: "Open an exercise first.", exerciseLocked: "Solution locked", exerciseUnlockMsg: "To unlock solution, need {MIN} attempts. You have {N} — read hints first.",
    progressLessons: "Lessons", progressExercises: "Exercises", progressDone: "Done", progressRead: "Read", progressOf: "of", progressPercent: "%",
    quizTitle: "Quick Quiz", quizQuestions: "13 questions", quizSubmit: "Submit answers", quizQuestionPrefix: "Question", quizOptions: ["A", "B", "C", "D"], quizCorrect: "Correct answer:", quizWhy: "Why?", quizScore: "Score", quizTotal: "of", quizPercent: "%",
    diagKind: "Error", diagTitle: "Diagnosis", diagWhat: "What happened?", diagWhy: "Why?", diagHowto: "How to fix it?", notConnected: "Could not connect to the server: ",
    searchTitle: "Search", searchPlaceholder: "Search all documents…", noSearchResults: "No results found for",
    paletteLessons: "Lesson", paletteExercise: "Exercise", paletteDisplay: "Display", cleanClear: "Clear console",
    navLessons: "Lessons", navExercises: "Exercises", navProjects: "Projects", navQuiz: "Quiz", navScratch: "Notes", navSearch: "Search all documents", navHelp: "Help",
    themeCRT: "CRT green theme", themeAmber: "Amber theme", fontInc: "Font size: {N} px", langSwitchEn: "Language switched to English", langSwitchFa: "Language switched to Persian", loading: "Loading…", noContent: "No content available", resetConfirm: "Reset code? Your changes will be lost.", exerciseDescPrefix: "Exercise {num}:", briefSectionHints: "Hints", briefSectionSolution: "Solution", quizResult: "Quiz result", quizPerfect: "Perfect score!", quizTryAgain: "Try again", quizScoreLabel: "Your score", quizResults: "Results", hintLabel: "Hint", solutionLabel: "Solution", docSearch: "Search", noDoc: "No document selected", language: "Language"
  };
  var faTexts = {
    sidebarLessons: "درس‌ها", sidebarExercises: "تمرین‌ها", sidebarProjects: "پروژه‌ها",
    docLesson: "درس", docExercise: "تمرین", docProject: "پروژه", docQuiz: "آزمون سریع", docScratch: "یادداشت آزاد", docSearch: "جست‌وجو", docDone: "خواندم",
    exerciseHints: "راهنماها", exerciseFullSolution: "راه‌حل کامل", exerciseDone: "انجام‌شده", exerciseUndone: "انجام‌نشده", exerciseReset: "کد بازنشانی شد.", exerciseCopied: "کد کپی شد.", exerciseSelectFirst: "ابتدا یک تمرین باز کن.", exerciseLocked: "راه‌حل قفل است", exerciseUnlockMsg: "برای دیدن راه‌حل باید {MIN} بار تلاش کنی. تو {N} بار تلاش کرده‌ای — اول راهنماها را بخوان.",
    progressLessons: "درس‌ها", progressExercises: "تمرین‌ها", progressDone: "تمام", progressRead: "خوانده‌شده", progressOf: "از", progressPercent: "٪",
    quizTitle: "آزمون سریع", quizQuestions: "۱۳ سؤال", quizSubmit: "ثبت پاسخ‌ها", quizQuestionPrefix: "سؤال", quizOptions: ["الف", "ب", "ج", "د"], quizCorrect: "پاسخ درست:", quizWhy: "چرا؟", quizScore: "نمره", quizTotal: "از", quizPercent: "٪",
    diagKind: "خطا", diagTitle: "تشخیص", diagWhat: "چه شد؟", diagWhy: "چرا؟", diagHowto: "چطور درستش کنم؟", notConnected: "اتصال به سرور برقرار نشد: ",
    searchTitle: "جست‌وجو", searchPlaceholder: "جست‌وجو در همه‌ی جزوه‌ها…", noSearchResults: "نتیجه‌ای برای", paletteLessons: "درس", paletteExercise: "تمرین", paletteDisplay: "نمایش", cleanClear: "پاک کردن کنسول",
    navLessons: "درس‌ها", navExercises: "تمرین‌ها", navProjects: "پروژه‌ها", navQuiz: "آزمون", navScratch: "یادداشت", navSearch: "جست‌وجو در همه‌ی جزوه‌ها", navHelp: "راهنما", themeCRT: "پوسته‌ی سبز CRT", themeAmber: "پوسته‌ی کهربایی", fontInc: "اندازه‌ی فونت: {N} پیکسل", langSwitchEn: "زبان به انگلیسی تغییر کرد", langSwitchFa: "زبان به فارسی تغییر کرد", loading: "در حال بارگذاری…", noContent: "محتوایی در دسترس نیست", resetConfirm: "کد به حالت اول برگردد؟ تغییرات پاک می‌شود.", exerciseDescPrefix: "تمرین {num}:", briefSectionHints: "راهنماها", briefSectionSolution: "راه‌حل", quizResult: "نتیجه‌ی آزمون", quizPerfect: "نمره‌ی کامل!", quizTryAgain: "دوباره تلاش کن", quizScoreLabel: "نمره‌ی تو", quizResults: "نتایج", hintLabel: "راهنما", solutionLabel: "راه‌حل", noDoc: "سندی انتخاب نشده", language: "زبان"
  };
  var MIN_ATTEMPTS_FOR_SOLUTION = 3;
  function getText(key) {
    var v = state.lang === "fa" && faTexts[key] !== undefined ? faTexts[key] : (TEXT[key] || key);
    if (v === undefined) return key;
    if (typeof v !== "string") return v;
    var n = state.lastResult ? (state.lastResult.attempts || 0) : 0;
    return v.replace(/\{N\}/g, n).replace(/\{MIN\}/g, MIN_ATTEMPTS_FOR_SOLUTION || 3);
  }

  var dom = {
    boot: $("boot"), bootMsg: $("bootMsg"), app: $("app"),
    searchInput: $("searchInput"),
    btnPalette: $("btnPalette"), btnTheme: $("btnTheme"), btnFont: $("btnFont"), btnHelp: $("btnHelp"),
    navLessons: $("navLessons"), navExercises: $("navExercises"), navProjects: $("navProjects"),
    countLessons: $("countLessons"), countExercises: $("countExercises"), countProjects: $("countProjects"),
    navQuiz: $("navQuiz"), navScratch: $("navScratch"), navSearchAll: $("navSearchAll"), quizBadge: $("quizBadge"),
    progressFill: $("progressFill"), progressLabel: $("progressLabel"), progressPct: $("progressPct"),
    fileDot: $("fileDot"), fileName: $("fileName"), fileDirty: $("fileDirty"),
    btnRun: $("btnRun"), btnCheck: $("btnCheck"), btnHint: $("btnHint"),
    btnSolution: $("btnSolution"), btnCopy: $("btnCopy"), btnReset: $("btnReset"),
    editorWrap: $("editorWrap"), gutter: $("gutter"), highlight: $("highlight"),
    highlightCode: $("highlightCode"), code: $("code"),
    vsplit: $("vsplit"),
    stdout: $("stdout"), diag: $("diag"), tests: $("tests"), btnClearConsole: $("btnClearConsole"),
    hsplit: $("hsplit"),
    docKind: $("docKind"), docTitle: $("docTitle"), docBody: $("docBody"),
    docToc: $("docToc"), docSelect: $("docSelect"), btnDocDone: $("btnDocDone"),
    paneDoc: $("paneDoc"), sidebar: $("sidebar"),
    stMode: $("stMode"), stDoc: $("stDoc"), stExercise: $("stExercise"),
    stTests: $("stTests"), stTimer: $("stTimer"), stPython: $("stPython"),
    palette: $("palette"), paletteInput: $("paletteInput"), paletteList: $("paletteList"),
    helpModal: $("helpModal"), helpBody: $("helpBody"), btnHelpClose: $("btnHelpClose"),
    toast: $("toast"),
  };

  /* ── ابزارها ── */
  function faNumber(n) {
    var digits = ["۰", "۱", "۲", "۳", "۴", "۵", "۶", "۷", "۸", "۹"];
    if (state.lang === "en") {
      return String(n);
    }
    return String(n).replace(/\d/g, function (d) { return digits[Number(d)]; });
  }

  function faPad(num) {
    return faNumber(num < 10 ? "0" + num : num);
  }

  function toast(message, kind) {
    // پیام «در حال بارگذاری موتور» نباید با یک toast موقتی گم شود
    if (dom.toast.dataset.locked === "1") return;
    dom.toast.textContent = message;
    dom.toast.className = "toast" + (kind ? " is-" + kind : "");
    dom.toast.hidden = false;
    clearTimeout(toast._t);
    toast._t = setTimeout(function () {
      // اگر در حین بارگذاری موتوریم، این تایمر نباید پیام ماندگار را پنهان کند
      if (dom.toast.dataset.locked === "1") return;
      dom.toast.hidden = true;
    }, 3600);
  }

  function api(path, options) {
    // در نسخه‌ی استاتیک (HTML تک‌فایلی) لایه‌ی API محلی است
    if (window.__API__ && window.__API__.get) return window.__API__.get(path);
    return fetch(path, options).then(function (res) {
      return res.json();
    });
  }

  function post(path, payload) {
    if (window.__API__ && window.__API__.post) return window.__API__.post(path, payload);
    return fetch(path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload || {}),
    }).then(function (res) {
      return res.json();
    });
  }

  function storeKey(id) { return "pycourse.code." + id; }

  function loadSavedCode(id) {
    try { return localStorage.getItem(storeKey(id)) || ""; }
    catch (e) { return ""; }
  }

  function saveCode(id, code) {
    try { localStorage.setItem(storeKey(id), code); } catch (e) { /* بی‌خیال */ }
  }

  function esc(text) {
    return String(text == null ? "" : text)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  /* ══════════════════════════════════════════════════════════
     راه‌اندازی
     ══════════════════════════════════════════════════════════ */

  function boot() {
    var injected = window.__BOOTSTRAP__;

    if (injected && injected.curriculum) {
      // داده‌ها از قبل داخل صفحه هستند — بدون تأخیر رندر می‌کنیم
      state.curriculum = injected.curriculum;
      state.progress = injected.progress || state.progress;
      if (injected.lang) state.lang = injected.lang;
      startApp();
      return;
    }

    api("/api/curriculum?lang=" + state.lang)
      .then(function (data) {
        state.curriculum = data;
        return api("/api/progress");
      })
      .then(function (progress) {
        state.progress = progress;
        startApp();
      })
      .catch(function (err) {
        dom.bootMsg.textContent = "اتصال به سرور برقرار نشد: " + err.message;
      });
  }

  function startApp() {
    applySettings(state.progress);
    renderSidebar();
    renderDocSelect();
    dom.stPython.textContent = "Python " + (state.curriculum.python_version || "");
    dom.boot.hidden = true;
    dom.app.hidden = false;

    // اولین درس را باز کن
    var first = (state.curriculum.lessons || [])[0];
    if (first) openLesson(first.id);
    else openScratch();
  }

  function applySettings(progress) {
    if (progress.font_size) {
      document.documentElement.style.setProperty("--fs-code", progress.font_size + "px");
      document.documentElement.style.setProperty("--fs-ui", progress.font_size + "px");
    }
    if (progress.theme) {
      document.documentElement.setAttribute("data-theme", progress.theme);
    }
  }

  /* ══════════════════════════════════════════════════════════
     نوار کناری
     ══════════════════════════════════════════════════════════ */

  function renderSidebar() {
    var lessons = state.curriculum.lessons || [];
    var exercises = state.curriculum.exercises || [];

    dom.countLessons.textContent = faNumber(lessons.length);
    dom.countExercises.textContent = faNumber(exercises.length);
    dom.countProjects.textContent = faNumber((state.curriculum.projects || []).length);

    dom.navLessons.innerHTML = lessons.map(function (lesson) {
      var done = state.progress.lessons_done.indexOf(lesson.id) !== -1;
      return (
        '<li><button class="navitem' + (done ? " is-done" : "") +
        '" data-kind="lesson" data-id="' + esc(lesson.id) + '">' +
        '<span class="navitem__check" aria-hidden="true">✓</span>' +
        '<span class="navitem__num">' + esc(lesson.number) + '</span>' +
        '<span class="navitem__text">' + esc(lesson.title) + "</span>" +
        "</button></li>"
      );
    }).join("");

    dom.navExercises.innerHTML = exercises.map(function (ex) {
      var done = state.progress.exercises_done.indexOf(ex.id) !== -1;
      var attempts = (state.progress.attempts || {})[ex.id] || 0;
      return (
        '<li><button class="navitem' + (done ? " is-done" : "") +
        '" data-kind="exercise" data-id="' + esc(ex.id) + '">' +
        '<span class="navitem__check" aria-hidden="true">✓</span>' +
        '<span class="navitem__num">' + faNumber(ex.number) + '</span>' +
        '<span class="navitem__text">' + esc(ex.title) + "</span>" +
        (attempts ? '<span class="navitem__badge">' + faNumber(attempts) + "</span>" : "") +
        "</button></li>"
      );
    }).join("");

    dom.navProjects.innerHTML = (state.curriculum.projects || []).map(function (proj) {
      return (
        '<li><button class="navitem" data-kind="project" data-id="' + esc(proj.id) + '">' +
        '<span class="navitem__mark" aria-hidden="true">◇</span>' +
        '<span class="navitem__text">' + esc(proj.title) + "</span>" +
        "</button></li>"
      );
    }).join("");

    if (state.progress.quiz_best != null) {
      dom.quizBadge.textContent = faNumber(state.progress.quiz_best) + "٪";
    }

    updateProgressBar();
    highlightActiveNav();
  }

  function updateProgressBar() {
    var total = (state.curriculum.lessons || []).length + (state.curriculum.exercises || []).length;
    var done = (state.progress.lessons_done || []).length + (state.progress.exercises_done || []).length;
    var pct = total ? Math.round((done / total) * 100) : 0;
    dom.progressFill.style.width = pct + "%";
    dom.progressLabel.textContent = faNumber(done) + " از " + faNumber(total);
    dom.progressPct.textContent = faNumber(pct) + "٪";
  }

  function highlightActiveNav() {
    var buttons = document.querySelectorAll(".navitem[data-id]");
    for (var i = 0; i < buttons.length; i++) {
      var btn = buttons[i];
      var isActive =
        (btn.dataset.kind === "exercise" && btn.dataset.id === state.exerciseId) ||
        (btn.dataset.kind === "lesson" && btn.dataset.id === state.docId && state.docKind === "lesson") ||
        (btn.dataset.kind === "project" && btn.dataset.id === state.docId && state.docKind === "project");
      btn.classList.toggle("is-active", isActive);
    }
  }

  /* ══════════════════════════════════════════════════════════
     پنل سند
     ══════════════════════════════════════════════════════════ */

  function renderDocSelect() {
    var groups = [
      { label: "درس‌ها", items: state.curriculum.lessons || [], kind: "lesson" },
      { label: "تمرین‌ها", items: state.curriculum.exercises || [], kind: "exercise" },
      { label: "پروژه‌ها", items: state.curriculum.projects || [], kind: "project" },
    ];
    var html = '<option value="">— انتخاب کن —</option>';
    groups.forEach(function (group) {
      html += '<optgroup label="' + esc(group.label) + '">';
      group.items.forEach(function (item) {
        html += '<option value="' + esc(group.kind + ":" + item.id) + '">' + esc(item.title) + "</option>";
      });
      html += "</optgroup>";
    });
    dom.docSelect.innerHTML = html;
  }

  function renderDoc(markdown, title) {
    var html = MD.render(markdown);
    var holder = document.createElement("div");
    holder.innerHTML = html;
    // عنوانِ تکراری بالای سند را حذف کن (در نوار بالای پنل هست)
    var firstH1 = holder.querySelector("h1");
    if (firstH1 && title && firstH1.textContent.trim() === String(title).trim()) {
      holder.removeChild(firstH1);
    }
    return holder.innerHTML;
  }

  function openLesson(id) {
    api("/api/doc?id=" + encodeURIComponent(id) + "&lang=" + state.lang).then(function (doc) {
      if (doc.error) { toast(doc.error, "error"); return; }
      state.docId = id;
      state.docKind = "markdown";
      state.exercise = null;

      dom.docKind.textContent = "جزوه";
      dom.docTitle.textContent = doc.title;
      dom.docBody.innerHTML = '<div class="doc">' + renderDoc(doc.body, doc.title) + "</div>";
      dom.docBody.scrollTop = 0;
      renderToc(doc.body);
      dom.stDoc.textContent = doc.title;
      dom.docSelect.value = "lesson:" + id;

      // تمرین متناظر را در ویرایشگر بارگذاری کن
      var match = exerciseForLesson(id);
      if (match) loadExercise(match, true);

      highlightActiveNav();
      updateDocDoneButton();
    });
  }

  function openProject(id) {
    api("/api/doc?id=" + encodeURIComponent(id) + "&lang=" + state.lang).then(function (doc) {
      if (doc.error) { toast(doc.error, "error"); return; }
      state.docId = id;
      state.docKind = "project";
      dom.docKind.textContent = "پروژه";
      dom.docTitle.textContent = doc.title;
      dom.docBody.innerHTML = '<div class="doc">' + renderDoc(doc.body, doc.title) + "</div>";
      dom.docBody.scrollTop = 0;
      renderToc(doc.body);
      dom.stDoc.textContent = doc.title;
      dom.docSelect.value = "project:" + id;
      highlightActiveNav();
      updateDocDoneButton();
    });
  }

  function renderToc(markdown) {
    var heads = MD.headings(markdown).filter(function (h) { return h.level >= 2 && h.level <= 3; });
    if (!heads.length) { dom.docToc.hidden = true; return; }
    dom.docToc.hidden = false;
    dom.docToc.innerHTML = heads.map(function (h) {
      return '<a data-target="' + esc(h.id) + '">' + esc(h.text) + "</a>";
    }).join("");
  }

  function exerciseForLesson(lessonId) {
    var lessons = state.curriculum.lessons || [];
    var exercises = state.curriculum.exercises || [];
    var index = -1;
    for (var i = 0; i < lessons.length; i++) {
      if (lessons[i].id === lessonId) { index = i; break; }
    }
    if (index === -1) return null;
    if (lessons[index].id === "00_setup") return "first_steps";
    return exercises[index] ? exercises[index].id : null;
  }

  /* ── تمرین ── */

  function loadExercise(id, keepDoc) {
    api("/api/exercise?id=" + encodeURIComponent(id) + "&lang=" + state.lang).then(function (ex) {
      if (ex.error) { toast(ex.error, "error"); return; }
      state.exercise = ex;
      state.exerciseId = ex.id;
      state.hintLevel = 0;
      state.errorLine = null;

      var saved = loadSavedCode(ex.id);
      dom.code.value = saved || ex.user_part || "";
      dom.fileName.textContent = ex.id + ".py";
      dom.fileDirty.hidden = true;
      dom.fileDot.className = "codepane__dot";
      dom.stExercise.textContent = ex.title;

      if (!keepDoc) showExerciseBrief(ex);
      refreshEditor();
      updateStatusTests(null);
      highlightActiveNav();
      startTimer();
    });
  }

  function showExerciseBrief(ex) {
    state.docId = ex.id;
    state.docKind = "exercise";

    var related = relatedLesson(ex.id);
    var relatedBtn = related
      ? '<button class="brief__link" data-goto-lesson="' + esc(related.id) + '">' +
        "◂ " + esc(related.title) + "</button>"
      : "";

    var html =
      '<div class="brief">' +
      (ex.description ? '<pre class="brief__desc">' + esc(ex.description) + "</pre>" : "") +
      '<div class="brief__section">راهنما</div>' +
      '<button class="brief__link" id="briefHint">؟ راهنمای مرحله‌ای (۳ سطح)</button> ' +
      '<button class="brief__link" id="briefSolution">★ راه‌حل کامل</button>' +
      '<div class="brief__section">بخش مرتبط</div>' +
      relatedBtn +
      '<div id="briefExtra"></div>' +
      "</div>";

    dom.docKind.textContent = "تمرین";
    dom.docTitle.textContent = ex.title;
    dom.docBody.innerHTML = html;
    dom.docBody.scrollTop = 0;
    dom.docToc.hidden = true;
    dom.stDoc.textContent = ex.title;
    dom.docSelect.value = "exercise:" + ex.id;

    var hintBtn = $("briefHint");
    if (hintBtn) hintBtn.onclick = showHint;
    var solBtn = $("briefSolution");
    if (solBtn) solBtn.onclick = showSolution;

    var link = dom.docBody.querySelector("[data-goto-lesson]");
    if (link) {
      link.onclick = function () { openLesson(link.dataset.gotoLesson); };
    }
    updateDocDoneButton();
  }

  function relatedLesson(exerciseId) {
    var lessons = state.curriculum.lessons || [];
    var exercises = state.curriculum.exercises || [];
    var index = -1;
    for (var i = 0; i < exercises.length; i++) {
      if (exercises[i].id === exerciseId) { index = i; break; }
    }
    if (index === -1) return null;
    return lessons[index] || null;
  }

  function openScratch() {
    state.exerciseId = null;
    state.exercise = null;
    state.docId = "scratch";
    state.docKind = "scratch";
    dom.code.value = loadSavedCode("scratch");
    dom.fileName.textContent = "yaddasht.py";
    dom.docKind.textContent = "یادداشت";
    dom.docTitle.textContent = "یادداشت آزاد";
    dom.docBody.innerHTML =
      '<div class="brief"><p class="diag__empty">این یک بوم خالی است. هر چه بنویسی ' +
      "اینجا می‌ماند. برای شروع، یک تمرین را از نوار کناری باز کن.</p></div>";
    dom.docToc.hidden = true;
    dom.stDoc.textContent = "یادداشت آزاد";
    dom.stExercise.textContent = "—";
    refreshEditor();
    highlightActiveNav();
  }

  function updateDocDoneButton() {
    var isLesson = state.docKind === "lesson";
    var isProject = state.docKind === "project";
    var isExercise = state.docKind === "exercise";
    dom.btnDocDone.hidden = !(isLesson || isProject || isExercise);

    var done = false;
    if (isLesson) done = state.progress.lessons_done.indexOf(state.docId) !== -1;
    else if (isProject) done = false;
    else if (isExercise) done = state.progress.exercises_done.indexOf(state.docId) !== -1;

    dom.btnDocDone.textContent = done ? "✓ خوانده شد" : "✓ خواندم";
  }

  /* ══════════════════════════════════════════════════════════
     ویرایشگر
     ══════════════════════════════════════════════════════════ */

  function refreshEditor() {
    var code = dom.code.value;
    var lines = Highlight.lines(code);

    var html = lines.map(function (line, index) {
      var cls = state.errorLine === index + 1 ? ' class="hl-line-error"' : "";
      return "<div" + cls + ">" + (line || " ") + "</div>";
    }).join("");
    dom.highlightCode.innerHTML = html + "<div> </div>";

    // شماره‌ی خط‌ها
    var count = code.split("\n").length;
    var gutter = [];
    for (var i = 1; i <= count; i++) {
      var cls = "";
      if (state.errorLine === i) cls = " is-error";
      gutter.push('<span class="gl' + cls + '">' + i + "</span>");
    }
    dom.gutter.innerHTML = gutter.join("");

    syncScroll();
  }

  function syncScroll() {
    dom.highlight.scrollTop = dom.code.scrollTop;
    dom.highlight.scrollLeft = dom.code.scrollLeft;
    dom.gutter.scrollTop = dom.code.scrollTop;
  }

  function markDirty(dirty) {
    dom.fileDirty.hidden = !dirty;
    if (dirty) {
      dom.fileDot.className = "codepane__dot is-dirty";
    }
  }

  /* ══════════════════════════════════════════════════════════
     اجرا و بررسی
     ══════════════════════════════════════════════════════════ */

  function runCode(mode) {
    /* روی گوشی بارگذاری موتور ۸ تا ۱۵ ثانیه طول می‌کشد. قبلاً دکمه در این
       بازه `pointer-events: none` بود و کلیک کاربر بی‌صدا بلعیده می‌شد؛
       حالا پاسخ فوری می‌دهیم که واقعاً در حال کاریم. */
    if (dom.btnRun.classList.contains("is-busy")) {
      if (dom.toast.dataset.locked === "1") {
        // در حین بارگذاری موتوریم: پیام ماندگار را دوباره نمایان کن
        dom.toast.hidden = false;
      } else {
        toast("در حال اجرا… چند لحظه صبر کن", "info");
      }
      return;
    }

    var code = dom.code.value;
    saveCode(state.exerciseId || "scratch", code);

    dom.btnRun.classList.add("is-busy");
    dom.btnCheck.classList.add("is-busy");
    setConsoleTab("output");

    /* اگر `post` خطا بدهد (مثلاً TypeError هنگام بارگذاری موتور)، آن خطا
       «همزمان» است و از زنجیره‌ی .then/.catch رد می‌شود — در نتیجه
       `classList.remove("is-busy")` اجرا نمی‌شد و دکمه‌ها با
       `pointer-events: none` برای همیشه می‌مُردند. اینجا تبدیلش می‌کنیم
       به وعده‌ی ردشده تا .catch همیشه اجرا شود. */
    var request;
    try {
      request = post("/api/run", {
        code: code,
        mode: mode,
        exercise_id: state.exerciseId || "",
        timeout: 10,
      });
    } catch (err) {
      request = Promise.reject(err);
    }

    request
      .then(function (result) {
        state.lastResult = result;
        dom.btnRun.classList.remove("is-busy");
        dom.btnCheck.classList.remove("is-busy");

        if (result && result.engine_failed) {
          // موتور پایتون بالا نیامد — دکمه‌ها آزاد شدند و می‌توان دوباره تلاش کرد
          dom.stdout.textContent =
            "❗ " + (result.stderr || "بارگذاری موتور پایتون ناموفق بود.");
          dom.diag.innerHTML =
            '<p class="diag__empty">موتور پایتون بارگذاری نشد. ' +
            "دکمه‌ی «اجرا» را دوباره بزن تا از نو تلاش شود؛ معمولاً به خاطر " +
            "کمبود حافظه یا کندی گوشی پیش می‌آید.</p>";
          state.errorLine = null;
          dom.stMode.textContent = "IDLE";
          dom.stMode.className = "statusline__mode";
          refreshEditor();
          toast("بارگذاری موتور ناموفق بود — دوباره تلاش کن", "error");
          return;
        }

        dom.stdout.textContent = result.stdout || "";
        if (!result.stdout) {
          dom.stdout.textContent = result.stderr ? "" : "(بدون خروجی)";
        }

        renderDiagnosis(result.diagnosis, result);

        if (mode === "check") {
          renderTests(result.tests || []);
          if (result.attempts) {
            state.progress.attempts = state.progress.attempts || {};
            state.progress.attempts[state.exerciseId] = result.attempts;
            renderSidebar();
          }
        }
      })
      .catch(function (err) {
        dom.btnRun.classList.remove("is-busy");
        dom.btnCheck.classList.remove("is-busy");
        toast("اجرا نشد: " + (err && err.message ? err.message : err), "error");
      });
  }

  function renderDiagnosis(diag, result) {
    if (!diag) {
      dom.diag.innerHTML =
        '<p class="diag__empty">خطایی گزارش نشده. کدت بدون مشکل اجرا شد.</p>';
      state.errorLine = null;
      dom.stMode.textContent = "NORMAL";
      dom.stMode.className = "statusline__mode is-ok";
      refreshEditor();
      return;
    }

    state.errorLine = diag.line || null;
    refreshEditor();

    dom.stMode.textContent = diag.kind || "ERROR";
    dom.stMode.className = "statusline__mode is-error";

    var fixHtml = (diag.fix || []).map(function (item) {
      return "<li>" + esc(item) + "</li>";
    }).join("");

    var snippet = "";
    if (diag.source) {
      snippet =
        '<pre class="codesnippet"><span class="hl-line-error">' +
        esc(diag.source) +
        "</span></pre>";
    }

    var raw = "";
    if (result && result.raw_stderr) {
      raw =
        '<div class="diagrow"><span class="diagrow__label">خروجی خام پایتون</span>' +
        '<pre class="codesnippet">' + esc(result.raw_stderr.trim()) + "</pre></div>";
    }

    dom.diag.innerHTML =
      '<div class="card">' +
      '<div class="card__head">' +
      '<span class="card__kind">' + esc(diag.kind || "Error") + "</span>" +
      '<span class="card__title">' + esc(diag.title || "خطا") + "</span>" +
      (diag.line ? '<span class="card__line">خط ' + faNumber(diag.line) + "</span>" : "") +
      "</div>" +
      '<div class="card__body">' +
      '<div class="diagrow"><span class="diagrow__label">چه شد؟</span>' +
      '<p class="diagrow__text">' + esc(diag.what || "") + "</p></div>" +
      '<div class="diagrow"><span class="diagrow__label">چرا؟</span>' +
      '<p class="diagrow__text">' + esc(diag.why || "") + "</p></div>" +
      (fixHtml
        ? '<div class="diagrow"><span class="diagrow__label">چه کنم؟</span>' +
          '<ul class="fixlist">' + fixHtml + "</ul></div>"
        : "") +
      snippet +
      raw +
      "</div></div>";

    setConsoleTab("problems");
  }

  function renderTests(tests) {
    if (!tests.length) {
      dom.tests.innerHTML = '<p class="diag__empty">تستی اجرا نشد.</p>';
      updateStatusTests(null);
      return;
    }

    var passed = tests.filter(function (t) { return t.status === "PASS"; }).length;
    var failed = tests.length - passed;
    var pct = Math.round((passed / tests.length) * 100);

    dom.tests.innerHTML =
      '<div class="tests__summary ' + (failed === 0 ? "is-pass" : "is-fail") + '">' +
      "<span>" + (failed === 0 ? "✓ همه‌ی تست‌ها پاس شد" : "✗ " + faNumber(failed) + " تست ناموفق") + "</span>" +
      '<span class="tests__bar"><i style="width:' + pct + '%"></i></span>' +
      "<span>" + faNumber(passed) + "/" + faNumber(tests.length) + " تست</span>" +
      "</div>" +
      '<ul class="testlist">' +
      tests.map(function (t) {
        var ok = t.status === "PASS";
        var label = ok ? "✓" : t.status === "ERROR" ? "!" : "✗";
        var text = t.message || (ok ? "پاس شد" : "ناموفق");
        return (
          '<li class="' + (ok ? "is-pass" : "is-fail") + '">' +
          '<span class="testlist__mark">' + label + "</span>" +
          '<span class="testlist__text">' + esc(text) + "</span></li>"
        );
      }).join("") +
      "</ul>";

    updateStatusTests({ passed: passed, total: tests.length });
    if (failed === 0) {
      dom.stMode.textContent = "PASS";
      dom.stMode.className = "statusline__mode is-ok";
      toast("همه‌ی تست‌ها پاس شد! 🎉", "ok");
    } else {
      setConsoleTab("tests");
    }
  }

  function updateStatusTests(summary) {
    if (!summary) {
      dom.stTests.textContent = "—";
      dom.stTests.className = "";
      return;
    }
    dom.stTests.textContent = faNumber(summary.passed) + "/" + faNumber(summary.total);
    dom.stTests.className = summary.passed === summary.total ? "is-pass" : "is-fail";
  }

  function setConsoleTab(name) {
    state.consoleTab = name;
    var tabs = document.querySelectorAll(".console__tab");
    for (var i = 0; i < tabs.length; i++) {
      tabs[i].classList.toggle("is-active", tabs[i].dataset.tab === name);
    }
    ["output", "problems", "tests"].forEach(function (key) {
      $("tab" + key.charAt(0).toUpperCase() + key.slice(1)).classList.toggle("is-active", key === name);
    });
  }

  /* ══════════════════════════════════════════════════════════
     راهنما و راه‌حل
     ══════════════════════════════════════════════════════════ */

  function showHint() {
    if (!state.exerciseId) { toast("اول یک تمرین را باز کن.", "error"); return; }
    var level = state.hintLevel + 1;
    api("/api/hint?exercise=" + encodeURIComponent(state.exerciseId) + "&level=" + level + "&lang=" + state.lang)
      .then(function (data) {
        if (data.error) { toast(data.error, "error"); return; }
        state.hintLevel = data.level;
        var target = $("briefExtra") || dom.docBody;
        var list = target.querySelector(".hintlist");
        if (!list) {
          list = document.createElement("ul");
          list.className = "hintlist";
          target.appendChild(list);
        }
        var item = document.createElement("li");
        item.innerHTML = "<b>راهنمای " + faNumber(data.level) + ":</b> " + esc(data.hint);
        list.appendChild(item);
        item.scrollIntoView({ block: "nearest" });
        toast("راهنمای " + faNumber(data.level) + " از " + faNumber(data.total) + " باز شد.");
      });
  }

  function showSolution() {
    if (!state.exerciseId) { toast("اول یک تمرین را باز کن.", "error"); return; }
    api("/api/solution?id=" + encodeURIComponent(state.exerciseId) + "&lang=" + state.lang).then(function (data) {
      if (data.error) { toast(data.error, "error"); return; }
      if (data.locked) {
        toast(data.message, "error");
        return;
      }
      var target = $("briefExtra") || dom.docBody;
      var box = document.createElement("div");
      box.className = "callout";
      box.innerHTML =
        "<strong>راه‌حل کامل</strong>" +
        (data.note ? "<br>" + esc(data.note) : "") +
        '<pre style="margin-top:8px"><code>' + esc(data.source) + "</code></pre>";
      target.appendChild(box);
      box.scrollIntoView({ block: "nearest" });
    });
  }

  /* ══════════════════════════════════════════════════════════
     آزمون
     ══════════════════════════════════════════════════════════ */

  function openQuiz() {
    state.docId = "quiz";
    state.docKind = "quiz";
    dom.docKind.textContent = "آزمون";
    dom.docTitle.textContent = "آزمون سریع — ۲۰ سوال";
    dom.docToc.hidden = true;
    dom.stDoc.textContent = "آزمون سریع";
    dom.docSelect.value = "";

    dom.docBody.innerHTML = '<div class="quiz" id="quizRoot"><p class="diag__empty">در حال آماده‌سازی…</p></div>';
    api("/api/quiz_questions?lang=" + state.lang).then(function (data) {
      if (!data.questions || !data.questions.length) {
        dom.docBody.innerHTML = '<p class="diag__empty">بانک سؤالات در دسترس نیست.</p>';
        return;
      }
      renderQuiz(data.questions);
    });
  }

  function renderQuiz(questions) {
    var root = $("quizRoot");
    root.innerHTML =
      '<p class="diag__empty">به هر سوال یک گزینه را انتخاب کن، بعد «ثبت پاسخ‌ها» را بزن. ' +
      "برای هر پاسخ غلط، دلیلش توضیح داده می‌شود.</p>" +
      '<button class="btn btn--check" id="btnQuizSubmit">ثبت پاسخ‌ها</button>' +
      '<div id="quizQuestions"></div>';

    var container = $("quizQuestions");
    container.innerHTML = questions.map(function (q, index) {
      return (
        '<div class="quiz__q" data-q="' + index + '">' +
        '<p class="quiz__text">' + faNumber(index + 1) + ". " + esc(q.q) + "</p>" +
        '<div class="quiz__opts">' +
        q.options.map(function (opt, oi) {
          return (
            '<button class="quiz__opt" data-q="' + index + '" data-o="' + oi + '">' +
            '<span class="quiz__key">' + String.fromCharCode(97 + oi) + "</span>" +
            "<span>" + esc(opt) + "</span></button>"
          );
        }).join("") +
        "</div></div>"
      );
    }).join("");

    $("btnQuizSubmit").onclick = function () {
      var answers = [];
      questions.forEach(function (_, index) { answers.push(null); });
      container.querySelectorAll(".quiz__opt").forEach(function (btn) {
        answers[Number(btn.dataset.q)] = Number(btn.dataset.o);
      });
      var unanswered = answers.filter(function (a) { return a === null; }).length;
      if (unanswered > 0) {
        toast(faNumber(unanswered) + " سوال بی‌پاسخ مانده.", "error");
        return;
      }
      submitQuiz(answers, questions);
    };
  }

  function submitQuiz(answers, questions) {
    post("/api/quiz", { answers: answers, lang: state.lang }).then(function (result) {
      var root = $("quizRoot");
      var head = root.querySelector(".quiz__q");
      var summary = document.createElement("div");
      summary.className = "quiz__result";
      summary.textContent =
        "نمره: " + faNumber(result.score) + " از " + faNumber(result.total) +
        "  (" + faNumber(result.percent) + "٪)";

      root.querySelectorAll(".quiz__opt").forEach(function (btn) {
        var qIndex = Number(btn.dataset.q);
        var oIndex = Number(btn.dataset.o);
        var res = result.results[qIndex];
        btn.classList.remove("is-picked");
        if (oIndex === res.correct_index) btn.classList.add("is-right");
        else if (oIndex === res.chosen) btn.classList.add("is-wrong");
      });

      result.results.forEach(function (res) {
        var block = root.querySelector('.quiz__q[data-q="' + res.index + '"]');
        if (!block) return;
        if (!res.is_correct) {
          var why = document.createElement("p");
          why.className = "quiz__why";
          why.innerHTML = "<b>پاسخ درست:</b> " +
            String.fromCharCode(97 + res.correct_index) + ") " +
            esc(res.options[res.correct_index]) +
            "<br><b>چرا؟</b> " + esc(res.why);
          block.appendChild(why);
        }
      });

      root.insertBefore(summary, head);
      summary.scrollIntoView({ block: "start", behavior: "smooth" });

      state.progress.quiz_best = Math.max(state.progress.quiz_best || 0, result.percent);
      renderSidebar();
      toast("نمره‌ی آزمون: " + faNumber(result.percent) + "٪", result.percent >= 70 ? "ok" : "error");
    });
  }

  /* ══════════════════════════════════════════════════════════
     جست‌وجو
     ══════════════════════════════════════════════════════════ */

  function searchAll(query) {
    var q = query.trim();
    if (q.length < 2) { toast("حداقل ۲ حرف بنویس.", "error"); return; }

    state.docKind = "search";
    dom.docKind.textContent = "جست‌وجو";
    dom.docTitle.textContent = "نتایج: «" + q + "»";
    dom.docToc.hidden = true;
    dom.stDoc.textContent = "جست‌وجو";
    dom.docSelect.value = "";

    var lessons = state.curriculum.lessons || [];
    var pending = lessons.length;
    var results = [];

    if (!pending) {
      dom.docBody.innerHTML = '<p class="diag__empty">چیزی برای جست‌وجو نیست.</p>';
      return;
    }

    lessons.forEach(function (lesson) {
      api("/api/doc?id=" + encodeURIComponent(lesson.id) + "&lang=" + state.lang).then(function (doc) {
        if (!doc.error) {
          var lower = doc.body.toLowerCase();
          var needle = q.toLowerCase();
          var index = lower.indexOf(needle);
          if (index !== -1) {
            var start = Math.max(0, index - 90);
            var snippet = doc.body.slice(start, index + 160).replace(/\n+/g, " ⏎ ");
            results.push({ lesson: lesson, snippet: snippet });
          }
        }
        pending -= 1;
        if (pending === 0) {
          dom.docBody.innerHTML = results.length
            ? '<div class="doc">' + results.map(function (r) {
                return (
                  '<div class="callout"><a href="#" data-goto="' + esc(r.lesson.id) + '">' +
                  "<strong>" + esc(r.lesson.title) + "</strong></a><br>" +
                  '<span style="font-family:var(--font-mono);font-size:12px">' +
                  esc(r.snippet) + "</span></div>"
                );
              }).join("") + "</div>"
            : '<p class="diag__empty">نتیجه‌ای برای «' + esc(q) + "» پیدا نشد.</p>";

          dom.docBody.querySelectorAll("[data-goto]").forEach(function (link) {
            link.onclick = function (e) {
              e.preventDefault();
              openLesson(link.dataset.goto);
            };
          });
        }
      });
    });
  }

  /* ══════════════════════════════════════════════════════════
     پالت دستورها
     ══════════════════════════════════════════════════════════ */

  var COMMANDS = [
    { cat: "اجرا", label: "اجرای کد", hint: "Ctrl+Enter", action: function () { runCode("run"); } },
    { cat: "اجرا", label: "بررسی با تست‌ها", hint: "Ctrl+Shift+Enter", action: function () { runCode("check"); } },
    { cat: "اجرا", label: "پاک کردن کنسول", hint: "", action: function () { clearConsole(); } },
    { cat: "تمرین", label: "راهنمای مرحله‌ای", hint: "?", action: showHint },
    { cat: "تمرین", label: "نمایش راه‌حل", hint: "", action: showSolution },
    { cat: "تمرین", label: "بازنشانی کد تمرین", hint: "", action: resetCode },
    { cat: "تمرین", label: "کپی کد", hint: "", action: copyCode },
    { cat: "نمایش", label: "تغییر پوسته (کهربایی / سبز CRT)", hint: "Ctrl+Alt+T", action: toggleTheme },
    { cat: "نمایش", label: "بزرگ‌تر کردن فونت", hint: "Ctrl+Alt+↑", action: function () { changeFont(1); } },
    { cat: "نمایش", label: "کوچک‌تر کردن فونت", hint: "Ctrl+Alt+↓", action: function () { changeFont(-1); } },
    { cat: "نمایش", label: "باز کردن آزمون سریع", hint: "", action: openQuiz },
    { cat: "نمایش", label: "یادداشت آزاد", hint: "", action: openScratch },
    { cat: "نمایش", label: "جست‌وجو در همه‌ی جزوه‌ها", hint: "", action: function () { dom.searchInput.focus(); } },
    { cat: "نمایش", label: "راهنمای میان‌برها", hint: "F1", action: toggleHelp },
  ];

  function openPalette() {
    dom.palette.hidden = false;
    dom.paletteInput.value = "";
    filterPalette("");
    dom.paletteInput.focus();
  }

  function closePalette() { dom.palette.hidden = true; }

  function filterPalette(query) {
    var q = query.trim().toLowerCase();
    state.paletteItems = COMMANDS.filter(function (cmd) {
      if (!q) return true;
      return (cmd.label + " " + cmd.cat).toLowerCase().indexOf(q) !== -1;
    });
    state.paletteIndex = 0;
    renderPalette();
  }

  function renderPalette() {
    dom.paletteList.innerHTML = state.paletteItems.map(function (cmd, index) {
      return (
        '<li class="' + (index === state.paletteIndex ? "is-sel" : "") + '" data-index="' + index + '">' +
        '<span class="palette__cat">' + esc(cmd.cat) + "</span>" +
        "<span>" + esc(cmd.label) + "</span>" +
        (cmd.hint ? '<span class="palette__keys">' + esc(cmd.hint) + "</span>" : "") +
        "</li>"
      );
    }).join("");
  }

  function runPaletteSelection() {
    var cmd = state.paletteItems[state.paletteIndex];
    closePalette();
    if (cmd) cmd.action();
  }

  /* ══════════════════════════════════════════════════════════
     کنترل‌های کوچک
     ══════════════════════════════════════════════════════════ */

  function clearConsole() {
    dom.stdout.textContent = "(هنوز چیزی اجرا نشده)";
    dom.diag.innerHTML =
      '<p class="diag__empty">خطایی گزارش نشده. کدت را اجرا کن تا اگر مشکلی بود، ' +
      "دلیلش را فارسی برایت توضیح دهم.</p>";
    dom.tests.innerHTML = '<p class="diag__empty">تستی اجرا نشده. دکمه‌ی «بررسی» را بزن.</p>';
    state.errorLine = null;
    refreshEditor();
  }

  function resetCode() {
    if (!state.exercise) { toast("این یک یادداشت آزاد است.", "error"); return; }
    if (!confirm("کد به حالت اول برگردد؟ تغییراتت پاک می‌شود.")) return;
    dom.code.value = state.exercise.user_part || "";
    saveCode(state.exerciseId, dom.code.value);
    state.errorLine = null;
    markDirty(false);
    refreshEditor();
    clearConsole();
    toast("کد بازنشانی شد.");
  }

  function copyCode() {
    var text = dom.code.value;
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () {
        toast("کد کپی شد.", "ok");
      });
    } else {
      dom.code.select();
      document.execCommand("copy");
      toast("کد کپی شد.", "ok");
    }
  }

  function toggleTheme() {
    var root = document.documentElement;
    var next = root.getAttribute("data-theme") === "crt" ? "amber" : "crt";
    root.setAttribute("data-theme", next);
    post("/api/progress", { theme: next });
    toast(next === "crt" ? "پوسته‌ی سبز CRT" : "پوسته‌ی کهربایی");
  }

  function toggleLanguage() {
    var nextLang = state.lang === "fa" ? "en" : "fa";
    post("/api/set-language", { lang: nextLang })
      .then(function (data) {
        if (data.ok) {
          state.lang = nextLang;
          document.documentElement.setAttribute("lang", nextLang);
          document.documentElement.setAttribute("dir", nextLang === "fa" ? "rtl" : "ltr");
          var prev = state.docId, prevKind = state.docKind;
          api("/api/curriculum?lang=" + nextLang).then(function (curriculum) {
            if (curriculum.error) throw new Error(curriculum.error);
            state.curriculum = curriculum;
            renderSidebar(); renderDocSelect();
            if (prev) { if (prevKind === "lesson") openLesson(prev); else if (prevKind === "exercise") loadExercise(prev, false); else if (prevKind === "project") openProject(prev); else if (prevKind === "quiz") openQuiz(); }
            toast(getText ? (nextLang === "en" ? "langSwitchEn" : "langSwitchFa") : (nextLang === "en" ? "Language switched to English" : "زبان به فارسی تغییر کرد"));
          }).catch(function (e) { toast("Language switch failed: " + e.message, "error"); });
        }
      })
      .catch(function (err) {
        toast("Language switch failed: " + err.message, "error");
      });
  }

  function changeFont(delta) {
    var current = parseFloat(
      getComputedStyle(document.documentElement).getPropertyValue("--fs-code")
    ) || 14.5;
    var next = Math.max(11, Math.min(24, current + delta));
    document.documentElement.style.setProperty("--fs-code", next + "px");
    document.documentElement.style.setProperty("--fs-ui", next + "px");
    post("/api/progress", { font_size: next });
    refreshEditor();
    toast("اندازه‌ی فونت: " + faNumber(next) + " پیکسل");
  }

  function toggleHelp() {
    if (dom.helpModal.hidden) {
      dom.helpBody.innerHTML = helpHtml();
      dom.helpModal.hidden = false;
    } else {
      dom.helpModal.hidden = true;
    }
  }

  function helpHtml() {
    var rows = [
      ["Ctrl + Enter", "اجرای کد"],
      ["Ctrl + Shift + Enter", "بررسی کد با تست‌ها"],
      ["Tab", "چهار فاصله در کد"],
      ["Ctrl + K", "پالت دستورها"],
      ["Ctrl + B", "باز/بستن نوار کناری"],
      ["Ctrl + Alt + T", "تغییر پوسته"],
      ["Ctrl + Alt + ↑ / ↓", "بزرگ/کوچک کردن فونت"],
      ["F1", "این راهنما"],
      ["/", "جست‌وجو در جزوه‌ها"],
      ["Esc", "بستن پنجره‌ها"],
    ];
    return '<dl class="keys">' + rows.map(function (r) {
      return "<dt><kbd>" + esc(r[0]) + "</kbd></dt><dd>" + esc(r[1]) + "</dd>";
    }).join("") + "</dl>";
  }

  /* ══════════════════════════════════════════════════════════
     تایمر
     ══════════════════════════════════════════════════════════ */

  function startTimer() {
    stopTimer();
    state.timerStart = Date.now();
    state.timerHandle = setInterval(function () {
      var seconds = Math.floor((Date.now() - state.timerStart) / 1000);
      dom.stTimer.textContent = faPad(Math.floor(seconds / 60)) + ":" + faPad(seconds % 60);
    }, 1000);
    dom.stTimer.textContent = "00:00";
  }

  function stopTimer() {
    if (state.timerHandle) { clearInterval(state.timerHandle); state.timerHandle = null; }
  }

  /* ══════════════════════════════════════════════════════════
     جداکننده‌های قابل کشیدن
     ══════════════════════════════════════════════════════════ */

  function setupSplitters() {
    // جداکننده‌ی عمودی: کد | جزوه
    var h = dom.hsplit;
    h.addEventListener("pointerdown", function (e) {
      e.preventDefault();
      h.setPointerCapture(e.pointerId);
      h.classList.add("is-dragging");
      var workspace = document.getElementById("workspace");
      var total = workspace.getBoundingClientRect().width;
      var startX = e.clientX;
      var startRatio = state.splitRatio;

      function move(ev) {
        var delta = ((ev.clientX - startX) / total) * 100;
        state.splitRatio = Math.max(24, Math.min(74, startRatio + delta));
        document.documentElement.style.setProperty("--code-w", state.splitRatio + "%");
      }
      function up(ev) {
        h.classList.remove("is-dragging");
        h.releasePointerCapture(ev.pointerId);
        window.removeEventListener("pointermove", move);
        window.removeEventListener("pointerup", up);
      }
      window.addEventListener("pointermove", move);
      window.addEventListener("pointerup", up);
    });

    // جداکننده‌ی افقی: ویرایشگر | کنسول
    var v = dom.vsplit;
    v.addEventListener("pointerdown", function (e) {
      e.preventDefault();
      v.setPointerCapture(e.pointerId);
      v.classList.add("is-dragging");
      var pane = dom.console.parentElement.getBoundingClientRect();
      var startY = e.clientY;
      var startRatio = state.consoleRatio;

      function move(ev) {
        var delta = ((ev.clientY - startY) / pane.height) * 100;
        state.consoleRatio = Math.max(12, Math.min(72, startRatio - delta));
        document.documentElement.style.setProperty("--console-h", state.consoleRatio + "%");
      }
      function up(ev) {
        v.classList.remove("is-dragging");
        v.releasePointerCapture(ev.pointerId);
        window.removeEventListener("pointermove", move);
        window.removeEventListener("pointerup", up);
      }
      window.addEventListener("pointermove", move);
      window.addEventListener("pointerup", up);
    });
  }

  /* ══════════════════════════════════════════════════════════
     رویدادها
     ══════════════════════════════════════════════════════════ */

  function bindEvents() {
    // ناوبری
    document.addEventListener("click", function (e) {
      var nav = e.target.closest(".navitem[data-id]");
      if (nav) {
        if (nav.dataset.kind === "lesson") openLesson(nav.dataset.id);
        else if (nav.dataset.kind === "exercise") loadExercise(nav.dataset.id, false);
        else if (nav.dataset.kind === "project") openProject(nav.dataset.id);
        return;
      }
      var opt = e.target.closest(".quiz__opt");
      if (opt) {
        var siblings = opt.parentElement.querySelectorAll(".quiz__opt");
        siblings.forEach(function (s) { s.classList.remove("is-picked"); });
        opt.classList.add("is-picked");
        return;
      }
      var toc = e.target.closest("#docToc a");
      if (toc) {
        var target = document.getElementById(toc.dataset.target);
        if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });

    dom.navQuiz.onclick = openQuiz;
    dom.navScratch.onclick = openScratch;
    dom.navSearchAll.onclick = function () { dom.searchInput.focus(); dom.searchInput.select(); };

    dom.docSelect.onchange = function () {
      var value = dom.docSelect.value;
      if (!value) return;
      var parts = value.split(":");
      if (parts[0] === "lesson") openLesson(parts.slice(1).join(":"));
      else if (parts[0] === "exercise") loadExercise(parts.slice(1).join(":"), false);
      else if (parts[0] === "project") openProject(parts.slice(1).join(":"));
    };

    dom.btnDocDone.onclick = function () {
      var section = state.docKind === "lesson" ? "lessons" : "exercises";
      var item = state.docId;
      if (section === "exercises" && state.docKind !== "exercise") return;
      post("/api/progress", { section: section, item: item }).then(function (data) {
        state.progress = data.state;
        renderSidebar();
        updateDocDoneButton();
        toast(data.done ? "به‌عنوان انجام‌شده علامت خورد." : "علامت برداشته شد.");
      });
    };

    // ویرایشگر
    dom.code.addEventListener("input", function () {
      refreshEditor();
      markDirty(true);
      if (state.exerciseId) saveCode(state.exerciseId, dom.code.value);
      else saveCode("scratch", dom.code.value);
    });
    dom.code.addEventListener("scroll", syncScroll);
    dom.code.addEventListener("keydown", onEditorKeydown);

    dom.btnRun.onclick = function () { runCode("run"); };
    dom.btnCheck.onclick = function () { runCode("check"); };
    dom.btnHint.onclick = showHint;
    dom.btnSolution.onclick = showSolution;
    dom.btnCopy.onclick = copyCode;
    dom.btnReset.onclick = resetCode;
    dom.btnClearConsole.onclick = clearConsole;

    var tabs = document.querySelectorAll(".console__tab");
    for (var i = 0; i < tabs.length; i++) {
      tabs[i].onclick = function () { setConsoleTab(this.dataset.tab); };
    }

    // پالت
    dom.btnPalette.onclick = openPalette;
    dom.paletteInput.addEventListener("input", function () { filterPalette(this.value); });
    dom.paletteInput.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") {
        e.preventDefault();
        state.paletteIndex = Math.min(state.paletteItems.length - 1, state.paletteIndex + 1);
        renderPalette();
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        state.paletteIndex = Math.max(0, state.paletteIndex - 1);
        renderPalette();
      } else if (e.key === "Enter") {
        e.preventDefault();
        runPaletteSelection();
      } else if (e.key === "Escape") {
        closePalette();
      }
    });
    dom.paletteList.addEventListener("click", function (e) {
      var item = e.target.closest("li[data-index]");
      if (!item) return;
      state.paletteIndex = Number(item.dataset.index);
      runPaletteSelection();
    });
    dom.palette.addEventListener("click", function (e) {
      if (e.target === dom.palette) closePalette();
    });

    // راهنما
    dom.btnHelp.onclick = toggleHelp;
    dom.btnHelpClose.onclick = toggleHelp;
    dom.helpModal.addEventListener("click", function (e) {
      if (e.target === dom.helpModal) dom.helpModal.hidden = true;
    });

    // پنجره‌ی گوشی
    $("btnPhone").onclick = showPhoneDialog;
    $("btnPhoneClose").onclick = function () { $("phoneModal").hidden = true; };
    $("phoneModal").addEventListener("click", function (e) {
      if (e.target === $("phoneModal")) $("phoneModal").hidden = true;
    });

    // زبان
    $("btnLang").onclick = toggleLanguage;

    // پوسته و فونت
    dom.btnTheme.onclick = toggleTheme;
    dom.btnFont.onclick = function () { changeFont(-1); };

    // جست‌وجو
    dom.searchInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter") { searchAll(this.value); this.blur(); }
      if (e.key === "Escape") { this.value = ""; this.blur(); }
    });

    // میان‌برهای صفحه‌کلید
    document.addEventListener("keydown", function (e) {
      var inField = /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName);

      if (e.key === "Escape") {
        closePalette();
        dom.helpModal.hidden = true;
        return;
      }
      if (e.key === "F1") { e.preventDefault(); toggleHelp(); return; }
      if (e.ctrlKey && e.key.toLowerCase() === "k") { e.preventDefault(); openPalette(); return; }
      if (e.ctrlKey && e.altKey && e.key.toLowerCase() === "t") { e.preventDefault(); toggleTheme(); return; }
      if (e.ctrlKey && e.altKey && (e.key === "ArrowUp" || e.key === "ArrowDown")) {
        e.preventDefault();
        changeFont(e.key === "ArrowUp" ? 1 : -1);
        return;
      }
      if (e.ctrlKey && e.key.toLowerCase() === "b") {
        e.preventDefault();
        dom.sidebar.classList.toggle("is-collapsed");
        return;
      }
      if (e.ctrlKey && e.key.toLowerCase() === "d") {
        e.preventDefault();
        document.getElementById("workspace").classList.toggle("is-nodoc");
        return;
      }
      if (e.ctrlKey && e.shiftKey && e.key === "Enter") {
        e.preventDefault(); runCode("check"); return;
      }
      if (e.ctrlKey && e.key === "Enter") {
        e.preventDefault(); runCode("run"); return;
      }
      if (e.key === "/" && !inField) {
        e.preventDefault(); dom.searchInput.focus();
      }
    });
  }

  /* ── رفتار ویرایشگر: Tab و Enter هوشمند ── */
  function onEditorKeydown(e) {
    var ta = e.target;

    if (e.key === "Tab") {
      e.preventDefault();
      var start = ta.selectionStart;
      var end = ta.selectionEnd;
      var value = ta.value;
      ta.value = value.slice(0, start) + "    " + value.slice(end);
      ta.selectionStart = ta.selectionEnd = start + 4;
      ta.dispatchEvent(new Event("input"));
      return;
    }

    if (e.key === "Enter") {
      var pos = ta.selectionStart;
      var before = ta.value.slice(0, pos);
      var lineStart = before.lastIndexOf("\n") + 1;
      var currentLine = before.slice(lineStart);
      var indent = (currentLine.match(/^[ \t]*/) || [""])[0];
      var extra = /:\s*$/.test(currentLine) ? "    " : "";
      if (!indent && !extra) return;
      e.preventDefault();
      var insert = "\n" + indent + extra;
      ta.value = ta.value.slice(0, pos) + insert + ta.value.slice(ta.selectionEnd);
      ta.selectionStart = ta.selectionEnd = pos + insert.length;
      ta.dispatchEvent(new Event("input"));
    }
  }

  /* ══════════════════════════════════════════════════════════
     «باز کردن روی گوشی»
     ══════════════════════════════════════════════════════════ */

  function showPhoneDialog() {
    var body = $("phoneBody");

    if (window.__API__ && window.__API__.get) {
      // نسخه‌ی استاتیک: فایل را باید روی گوشی کپی کنی
      body.innerHTML =
        '<div class="callout"><strong>این نسخه یک فایل مستقل است.</strong><br>' +
        "برای باز کردن روی گوشی، فایل <code>PythonTerminal.html</code> را به گوشی منتقل کن " +
        "و با مرورگر باز کن." +
        "<br><br>• <b>اندروید:</b> فایل را در «دانلودها» بگذار و با Chrome باز کن." +
        "<br>• <b>آیفون:</b> فایل را در «Files» ذخیره کن، بعد در Safari باز کن " +
        "(روی فایل ضربه بزن → Share → Open in Safari). " +
        "<br><br>یا فایل را روی یک هاست استاتیک بگذار و آدرسش را روی گوشی باز کن." +
        "</div>";
      $("phoneModal").hidden = false;
      return;
    }

    api("/api/network").then(function (info) {
      if (!info.urls || !info.urls.length) {
        body.innerHTML =
          '<div class="callout callout--danger">آدرس شبکه پیدا نشد. ' +
          "احتمالاً به اینترنت یا وای‌فای وصل نیستی.</div>";
      } else {
        var links = info.urls
          .map(function (u) {
            return (
              '<div class="phonelink"><span class="phonelink__url">' + esc(u) + "</span>" +
              '<a class="btn btn--check" href="' + esc(u) + '" target="_blank" rel="noopener">باز کن</a></div>'
            );
          })
          .join("");
        body.innerHTML =
          '<div class="callout"><strong>گوشی باید روی همین وای‌فای باشد.</strong><br>' +
          "این آدرس را در مرورگر گوشی باز کن:" +
          "</div>" +
          links +
          '<div class="callout" style="margin-top:14px">' +
          "<b>اگر باز نشد:</b><br>" +
          "• فایروال ویندوز ممکن است جلوی اتصال را بگیرد — از تنظیمات ویندوز، " +
          "پایتون را برای شبکه‌ی خصوصی اجازه بده.<br>" +
          "• روی گوشی مطمئن شو به همان وای‌فای وصلی (نه داده‌ی موبایل).<br>" +
          "• بعضی شبکه‌های دانشگاه/هتل جلوی ارتباط دستگاه‌ها را می‌گیرند." +
          "</div>";
      }
      $("phoneModal").hidden = false;
    });
  }

  /* ══════════════════════════════════════════════════════════
     ناوبری موبایل
     ══════════════════════════════════════════════════════════ */

  function isMobile() {
    return window.matchMedia("(max-width: 760px)").matches;
  }

  function setMobileView(view) {
    document.body.dataset.mobileView = view;
    var buttons = document.querySelectorAll(".mobilenav__btn");
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].classList.toggle("is-active", buttons[i].dataset.view === view);
    }
    // وقتی کاربر یک درس/تمرین را انتخاب می‌کند، روی همان تب بمان
    if (view === "code") refreshEditor();
  }

  function setupMobileNav() {
    var nav = $("mobileNav");
    nav.addEventListener("click", function (e) {
      var btn = e.target.closest(".mobilenav__btn");
      if (!btn) return;
      setMobileView(btn.dataset.view);
    });

    // انتخاب درس/تمرین در حالت موبایل → برود به تب کد
    document.addEventListener("click", function (e) {
      if (!isMobile()) return;
      if (e.target.closest(".navitem[data-id]")) setMobileView("code");
    });

    // بستن کشو با کلیک بیرون از آن
    var workspace = $("workspace");
    var scrim = document.createElement("div");
    scrim.className = "sidebar-scrim";
    workspace.appendChild(scrim);
    scrim.addEventListener("click", function () { setMobileView("code"); });

    $("btnMenu").onclick = function () {
      setMobileView(document.body.dataset.mobileView === "menu" ? "code" : "menu");
    };

    // اگر پنجره بزرگ شد، نمای دسکتاپ برگردد
    window.addEventListener("resize", function () {
      if (!isMobile()) {
        document.body.dataset.mobileView = "";
        var buttons = document.querySelectorAll(".mobilenav__btn");
        for (var i = 0; i < buttons.length; i++) buttons[i].classList.remove("is-active");
      } else if (!document.body.dataset.mobileView) {
        setMobileView("code");
      }
    });

    if (isMobile()) setMobileView("code");
  }

  /* ══════════════════════════════════════════════════════════
     راه‌اندازی
     ══════════════════════════════════════════════════════════ */

  bindEvents();
  setupSplitters();
  setupMobileNav();
  boot();

  window.__pycourse = { state: state, runCode: runCode, refreshEditor: refreshEditor };
})();
