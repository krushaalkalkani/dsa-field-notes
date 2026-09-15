/* DSA Field Notes UI. No dependencies. Five things only:
   reading progress, active section, code Copy buttons, done checkboxes, [ ] paging. */
(function () {
  "use strict";

  /* --------------------------------------------- 1. reading progress bar */
  (function () {
    var bar = document.createElement("div");
    bar.className = "progress-bar";
    document.body.appendChild(bar);
    var queued = 0;
    function draw() {
      queued = 0;
      var doc = document.documentElement;
      var span = doc.scrollHeight - doc.clientHeight;
      var at = span > 0 ? doc.scrollTop / span : 0;
      bar.style.transform = "scaleX(" + Math.max(0, Math.min(1, at)) + ")";
    }
    function queue() { if (!queued) queued = window.requestAnimationFrame(draw); }
    window.addEventListener("scroll", queue, { passive: true });
    window.addEventListener("resize", queue, { passive: true });
    draw();
  })();

  /* ------------------------------------------ 2. active section in the nav */
  (function () {
    var nav = document.querySelector("nav.sections");
    if (!nav || !("IntersectionObserver" in window)) return;

    var links = {};
    var targets = [];
    Array.prototype.forEach.call(nav.querySelectorAll('a[href^="#"]'), function (a) {
      var el = document.getElementById(a.getAttribute("href").slice(1));
      if (!el) return;
      links[el.id] = a;
      targets.push(el);
    });
    if (!targets.length) return;

    var last = null;
    function highlight() {
      // the current section is the last one whose heading has passed the top
      var current = targets[0].id;
      targets.forEach(function (el) {
        if (el.getBoundingClientRect().top <= 90) current = el.id;
      });
      if (current === last) return;
      last = current;
      Object.keys(links).forEach(function (id) {
        links[id].classList.toggle("is-active", id === current);
      });
      // while the nav is a horizontal chip bar, keep the active chip in view
      if (nav.scrollWidth > nav.clientWidth + 4) {
        links[current].scrollIntoView({ block: "nearest", inline: "nearest" });
      }
    }

    // the observer is only the trigger; it fires exactly when the answer can change
    var io = new IntersectionObserver(highlight, { rootMargin: "-88px 0px -60% 0px" });
    targets.forEach(function (el) { io.observe(el); });
  })();

  /* ---------------------------------------------- 3. Copy on code blocks */
  Array.prototype.forEach.call(document.querySelectorAll("pre"), function (pre) {
    var wrap = document.createElement("div");
    wrap.className = "codewrap";
    pre.parentNode.insertBefore(wrap, pre);
    wrap.appendChild(pre);

    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "copy-btn";
    btn.textContent = "Copy";
    btn.setAttribute("aria-label", "Copy this code block");
    btn.addEventListener("click", function () {
      var text = (pre.querySelector("code") || pre).innerText;
      var can = navigator.clipboard && window.isSecureContext;
      (can ? navigator.clipboard.writeText(text) : Promise.reject()).then(function () {
        btn.textContent = "Copied";
        btn.classList.add("ok");
      }, function () {
        btn.textContent = "Select it";
      });
      window.setTimeout(function () {
        btn.textContent = "Copy";
        btn.classList.remove("ok");
      }, 1000);
    });
    wrap.appendChild(btn);
  });

  /* --------------------------------------- 4. "Done" checkbox persistence */
  (function () {
    var KEY = "dsa-notes-done";
    var slots = Array.prototype.slice.call(document.querySelectorAll(".topic-slot"));
    var counter = document.getElementById("done-count");
    if (!slots.length) return;

    function read() {
      try {
        var saved = JSON.parse(localStorage.getItem(KEY) || "[]");
        if (!Array.isArray(saved)) return [];
        return saved.filter(function (id) { return typeof id === "string"; });
      } catch (err) { return []; }
    }
    function write(list) {
      /* private mode or full storage must not break the page */
      try { localStorage.setItem(KEY, JSON.stringify(list)); } catch (err) {}
    }
    function paint() {
      slots.forEach(function (slot) {
        var on = done.indexOf(slot.getAttribute("data-topic")) !== -1;
        slot.querySelector("input[type=checkbox]").checked = on;
        slot.classList.toggle("is-done", on);
      });
      if (!counter) return;
      counter.textContent = done.length + " of " + slots.length + " done";
      counter.hidden = false;
    }

    var ids = slots.map(function (slot) { return slot.getAttribute("data-topic"); });
    var done = read().filter(function (id) { return ids.indexOf(id) !== -1; });
    paint();

    slots.forEach(function (slot) {
      slot.querySelector("input[type=checkbox]").addEventListener("change", function () {
        var id = slot.getAttribute("data-topic");
        var at = done.indexOf(id);
        if (this.checked && at === -1) done.push(id);
        if (!this.checked && at !== -1) done.splice(at, 1);
        write(done);
        paint();
      });
    });
  })();

  /* ---------------------------------------------- 5. "[" and "]" paging */
  document.addEventListener("keydown", function (e) {
    if (e.key !== "[" && e.key !== "]") return;
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    var el = e.target;
    if (el && (el.isContentEditable ||
        /^(INPUT|TEXTAREA|SELECT|OPTION)$/.test(el.tagName || ""))) return;
    var link = document.querySelector(e.key === "[" ? ".pager a.prev" : ".pager a.next");
    if (!link) return;
    e.preventDefault();
    window.location.href = link.href;
  });
})();
