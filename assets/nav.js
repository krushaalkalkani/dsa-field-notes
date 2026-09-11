/* Topic-page helpers: "[" / "]" pager shortcuts, and a Copy button on each code block. */
(function () {
  "use strict";

  /* ---- 1. keyboard paging via the existing .pager links ---- */
  function typing(el) {
    return !!el && (el.isContentEditable ||
      /^(INPUT|TEXTAREA|SELECT|OPTION)$/.test(el.tagName || ""));
  }

  document.addEventListener("keydown", function (e) {
    if (e.key !== "[" && e.key !== "]") return;
    if (e.metaKey || e.ctrlKey || e.altKey || typing(e.target)) return;
    var link = document.querySelector(e.key === "[" ? ".pager a.prev" : ".pager a.next");
    if (!link) return;
    e.preventDefault();
    window.location.href = link.href;
  });

  /* ---- 2. Copy button on every <pre> ---- */
  var CSS = [
    ".codewrap{position:relative}",
    ".codewrap .copy-btn{position:absolute;top:7px;right:7px;z-index:2;",
    "font:600 11px/1 'JetBrains Mono',ui-monospace,monospace;letter-spacing:.08em;",
    "text-transform:uppercase;color:var(--muted);background:var(--surface);",
    "border:1px solid var(--line);border-radius:6px;padding:5px 8px;cursor:pointer;",
    "opacity:0;transition:opacity .12s ease}",
    ".codewrap:hover .copy-btn,.codewrap .copy-btn:focus-visible{opacity:1}",
    ".codewrap .copy-btn:hover{color:var(--ptr);border-color:var(--ptr)}",
    ".codewrap .copy-btn.ok{color:var(--ptr);border-color:var(--ptr);opacity:1}",
    "@media (hover:none){.codewrap .copy-btn{opacity:1}}"
  ].join("");

  function copy(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      var ta = document.createElement("textarea");
      ta.value = text;
      ta.setAttribute("readonly", "");
      ta.style.cssText = "position:fixed;top:-9999px;opacity:0";
      document.body.appendChild(ta);
      ta.select();
      var ok = false;
      try { ok = document.execCommand("copy"); } catch (err) { ok = false; }
      document.body.removeChild(ta);
      ok ? resolve() : reject();
    });
  }

  function addButton(pre) {
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
      var node = pre.querySelector("code") || pre;
      copy(node.innerText).then(function () {
        btn.textContent = "Copied";
        btn.classList.add("ok");
        window.setTimeout(function () {
          btn.textContent = "Copy";
          btn.classList.remove("ok");
        }, 1000);
      }, function () {
        btn.textContent = "Press Ctrl+C";
        window.setTimeout(function () { btn.textContent = "Copy"; }, 1500);
      });
    });
    wrap.appendChild(btn);
  }

  var pres = document.querySelectorAll("pre");
  if (!pres.length) return;
  var style = document.createElement("style");
  style.textContent = CSS;
  document.head.appendChild(style);
  Array.prototype.forEach.call(pres, addButton);
})();
