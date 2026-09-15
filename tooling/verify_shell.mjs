/* Headless check of the visual shell at phone and laptop widths.
   Serves the repo on a local port and drives Chromium.
   Needs playwright; this repo keeps it outside the tree:
     node tooling/verify_shell.mjs
*/
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";

const ROOT = process.cwd();
const PORT = 8941;
const { chromium } = createRequire("/tmp/dsa-verify/")("playwright");

const TYPES = {
  ".html": "text/html", ".css": "text/css", ".js": "text/javascript",
  ".webmanifest": "application/manifest+json", ".png": "image/png",
};

const server = http.createServer((req, res) => {
  const rel = decodeURIComponent(req.url.split("?")[0]).replace(/^\/+/, "") || "index.html";
  const file = path.join(ROOT, rel);
  if (!file.startsWith(ROOT) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
    res.writeHead(404).end("no");
    return;
  }
  res.writeHead(200, { "content-type": TYPES[path.extname(file)] || "text/plain" });
  res.end(fs.readFileSync(file));
});

let pass = 0;
const fails = [];
function check(name, ok, detail = "") {
  if (ok) { pass++; console.log("  ok   " + name); }
  else { fails.push(name + (detail ? " -> " + detail : "")); console.log("  FAIL " + name + " " + detail); }
}

const PHONE = { width: 390, height: 844 };
const LAPTOP = { width: 1280, height: 900 };
const TOPIC = "topics/06-trees.html";

await new Promise((r) => server.listen(PORT, r));
const browser = await chromium.launch();

async function open(page, url, viewport) {
  await page.setViewportSize(viewport);
  await page.goto(`http://127.0.0.1:${PORT}/${url}`, { waitUntil: "load" });
  await page.locator(".codewrap, .topic-grid").first().waitFor();
  return page;
}

async function noSidewaysScroll(page, label) {
  const m = await page.evaluate(() => {
    const d = document.documentElement;
    const culprits = [];
    for (const el of document.querySelectorAll("body *")) {
      const cs = getComputedStyle(el);
      if (cs.position === "fixed") continue;
      const r = el.getBoundingClientRect();
      if (r.right <= d.clientWidth + 1) continue;
      // legitimate if some ancestor below <body> scrolls or clips horizontally
      let p = el.parentElement, contained = false;
      while (p && p !== document.body && !contained) {
        if (getComputedStyle(p).overflowX !== "visible") contained = true;
        p = p.parentElement;
      }
      if (!contained) {
        culprits.push(`${el.tagName}.${String(el.className).slice(0, 34)} right=${Math.round(r.right)}`);
      }
    }
    return { scrollW: d.scrollWidth, clientW: d.clientWidth, culprits: culprits.slice(0, 4) };
  });
  check(`${label}: page does not scroll sideways`, m.scrollW <= m.clientW + 1,
    `scrollWidth=${m.scrollW} clientWidth=${m.clientW}`);
  check(`${label}: no element escapes the viewport`, m.culprits.length === 0,
    m.culprits.join(" | "));
}

/* ---------------------------------------------------------- phone: topic */
console.log(`\n[phone ${PHONE.width}x${PHONE.height}] ${TOPIC}`);
let ctx = await browser.newContext({ deviceScaleFactor: 2 });
let page = await open(await ctx.newPage(), TOPIC, PHONE);
await noSidewaysScroll(page, "phone topic");
await page.screenshot({ path: "/tmp/dsa-verify/shell-phone-top.png" });
await page.evaluate(() => document.querySelector("figure").scrollIntoView({ block: "center" }));
await page.waitForTimeout(200);
await page.screenshot({ path: "/tmp/dsa-verify/shell-phone-figure.png" });
await page.evaluate(() => window.scrollTo(0, 0));

const chips = await page.evaluate(() => {
  const nav = document.querySelector("nav.sections");
  const cs = getComputedStyle(nav);
  const first = nav.querySelector("a");
  return {
    position: cs.position, dir: cs.flexDirection,
    scrollable: nav.scrollWidth > nav.clientWidth,
    within: nav.getBoundingClientRect().width <= document.documentElement.clientWidth + 1,
    firstText: first.textContent.trim(), firstHref: first.getAttribute("href"),
    tapH: Math.round(first.getBoundingClientRect().height),
  };
});
check("phone: section links are a sticky horizontal chip bar",
  chips.position === "sticky" && chips.dir === "row", JSON.stringify(chips));
check("phone: chip bar scrolls horizontally inside itself", chips.scrollable && chips.within);
check('phone: first chip is the "Course map" link',
  chips.firstText === "Course map" && chips.firstHref === "../index.html", chips.firstText);
check("phone: chip tap target >= 34px", chips.tapH >= 34, chips.tapH + "px");

const phoneText = await page.evaluate(() => {
  const body = getComputedStyle(document.body);
  const pre = getComputedStyle(document.querySelector("pre"));
  const p = document.querySelector(".content section p");
  return {
    size: body.fontSize, lh: body.lineHeight, code: pre.fontSize,
    wrap: pre.whiteSpace, adjust: getComputedStyle(document.documentElement).webkitTextSizeAdjust,
    tap: getComputedStyle(document.body).webkitTapHighlightColor,
    pWidth: Math.round(p.getBoundingClientRect().width),
  };
});
check("phone: body text is 17px", phoneText.size === "17px", phoneText.size);
check("phone: line-height is 1.65", Math.abs(parseFloat(phoneText.lh) / 17 - 1.65) < 0.01, phoneText.lh);
check("phone: code is 14px and never wraps",
  phoneText.code === "14px" && phoneText.wrap === "pre", `${phoneText.code}/${phoneText.wrap}`);
check("phone: -webkit-text-size-adjust is 100%", phoneText.adjust === "100%", phoneText.adjust);
check("phone: tap highlight is transparent", /rgba\(0, 0, 0, 0\)|transparent/.test(phoneText.tap), phoneText.tap);

const analogy = await page.evaluate(() => {
  const a = document.querySelector(".analogy");
  const p = a.querySelector("p").getBoundingClientRect();
  return {
    cols: getComputedStyle(a).gridTemplateColumns.split(" ").length,
    textW: Math.round(p.width),
  };
});
check("phone: analogy box stacks so its text is full width",
  analogy.cols === 1 && analogy.textW > 280, JSON.stringify(analogy));

const fig = await page.evaluate(() => {
  const f = document.querySelector("figure");
  const svg = f.querySelector("svg");
  const cap = f.querySelector("figcaption");
  return {
    figScrolls: f.scrollWidth > f.clientWidth,
    svgW: Math.round(svg.getBoundingClientRect().width),
    hint: getComputedStyle(f, "::after").content,
    capW: Math.round(cap.getBoundingClientRect().width),
    viewport: document.documentElement.clientWidth,
  };
});
check("phone: wide diagram scrolls inside its figure, not the page", fig.figScrolls);
check("phone: diagram is rendered at a legible width (>= 600px)", fig.svgW >= 600, fig.svgW + "px");
check('phone: figure shows a "swipe" hint via CSS only', /swipe/.test(fig.hint), fig.hint);
check("phone: caption still fits the screen", fig.capW <= fig.viewport, `${fig.capW} vs ${fig.viewport}`);

const tbl = await page.evaluate(() => {
  const w = [...document.querySelectorAll(".tbl")].find((e) => e.scrollWidth > e.clientWidth);
  if (!w) return { none: true };
  const cell = w.querySelector("tbody td");
  return { sticky: getComputedStyle(cell).position, min: getComputedStyle(cell).minWidth };
});
check("phone: wide table scrolls in .tbl with a sticky first column",
  tbl.none || tbl.sticky === "sticky", JSON.stringify(tbl));

const det = await page.evaluate(async () => {
  const d = document.querySelector("details");
  const s = d.querySelector("summary");
  const closed = getComputedStyle(s, "::after").transform;
  s.click();
  await new Promise((r) => setTimeout(r, 400)); // let the rotation transition finish
  const open = getComputedStyle(s, "::after").transform;
  const h = Math.round(s.getBoundingClientRect().height);
  const hasBody = !!d.querySelector("div") && d.open;
  s.click();
  return { closed, open, h, hasBody };
});
check("phone: self-check summary tap target >= 48px", det.h >= 48, det.h + "px");
check("phone: chevron rotates on open", det.closed !== det.open, `${det.closed} -> ${det.open}`);
check("phone: details actually opens its answer", det.hasBody);

const progress = await page.evaluate(async () => {
  const bar = document.querySelector(".progress-bar");
  if (!bar) return { missing: true };
  const before = getComputedStyle(bar).transform;
  window.scrollTo(0, document.documentElement.scrollHeight);
  await new Promise((r) => setTimeout(r, 260));
  const after = getComputedStyle(bar).transform;
  window.scrollTo(0, 0);
  return { before, after, fixed: getComputedStyle(bar).position };
});
check("phone: reading progress bar grows as you scroll",
  !progress.missing && progress.before !== progress.after && progress.fixed === "fixed",
  JSON.stringify(progress));

await page.screenshot({ path: "/tmp/dsa-verify/shell-phone-topic.png" });

/* --------------------------------------------------------- phone: index */
console.log(`\n[phone ${PHONE.width}x${PHONE.height}] index.html`);
await open(page, "index.html", PHONE);
await noSidewaysScroll(page, "phone index");
const grid1 = await page.evaluate(() =>
  getComputedStyle(document.querySelector(".topic-grid")).gridTemplateColumns.split(" ").length);
check("phone: topic cards are one column", grid1 === 1, grid1 + " columns");

const done = await page.evaluate(async () => {
  const box = document.querySelector(".topic-slot input[type=checkbox]");
  const rect = document.querySelector(".done-box").getBoundingClientRect();
  box.click();
  const label = document.getElementById("done-count").textContent;
  const stored = localStorage.getItem("dsa-notes-done");
  const url = location.href;
  box.click();
  return { label, stored, tapH: Math.round(rect.height), url, still: location.href === url };
});
check('index: checkbox writes "X of 12 done"', /^1 of 12 done$/.test(done.label), done.label);
check("index: state is persisted to localStorage", done.stored === '["01-arrays"]', done.stored);
check("index: Done control tap target >= 34px", done.tapH >= 34, done.tapH + "px");
check("index: ticking Done does not follow the card link", done.still);
await page.screenshot({ path: "/tmp/dsa-verify/shell-phone-index.png", fullPage: false });
await ctx.close();

/* -------------------------------------------------------- laptop: topic */
console.log(`\n[laptop ${LAPTOP.width}x${LAPTOP.height}] ${TOPIC}`);
ctx = await browser.newContext();
page = await open(await ctx.newPage(), TOPIC, LAPTOP);
await noSidewaysScroll(page, "laptop topic");

const side = await page.evaluate(() => {
  const nav = document.querySelector("nav.sections");
  const content = document.querySelector(".content");
  const cs = getComputedStyle(nav);
  const n = nav.getBoundingClientRect();
  const c = content.getBoundingClientRect();
  return {
    dir: cs.flexDirection, position: cs.position,
    width: Math.round(n.width), contentW: Math.round(c.width),
    sideBySide: n.right <= c.left + 1 && n.top < c.bottom,
    navLeftOfContent: n.left < c.left,
  };
});
check("laptop: nav is a vertical 240px sidebar",
  side.dir === "column" && side.width === 240, JSON.stringify(side));
check("laptop: sidebar is sticky", side.position === "sticky", side.position);
check("laptop: sidebar sits left of the content column",
  side.sideBySide && side.navLeftOfContent, JSON.stringify(side));
check("laptop: content column is 760px", side.contentW === 760, side.contentW + "px");

const lap = await page.evaluate(() => ({
  size: getComputedStyle(document.body).fontSize,
  code: getComputedStyle(document.querySelector("pre")).fontSize,
}));
check("laptop: body text is 18px", lap.size === "18px", lap.size);
check("laptop: code is 15px", lap.code === "15px", lap.code);

const active = await page.evaluate(async () => {
  const y = document.getElementById("bfs").getBoundingClientRect().top + window.scrollY;
  window.scrollTo({ top: y + 4, behavior: "instant" });
  await new Promise((r) => setTimeout(r, 400));
  return [...document.querySelectorAll("nav.sections a.is-active")].map((a) => a.getAttribute("href"));
});
check("laptop: scrolling highlights the current section in the sidebar",
  active.length === 1 && active[0] === "#bfs", JSON.stringify(active));

const copy = await ctx.newPage();
await ctx.grantPermissions(["clipboard-read", "clipboard-write"]);
await open(copy, TOPIC, LAPTOP);
const clip = await copy.evaluate(async () => {
  const wrap = document.querySelector(".codewrap");
  const pre = wrap.querySelector("pre");
  const btn = wrap.querySelector(".copy-btn");
  btn.click();
  await new Promise((r) => setTimeout(r, 150));
  const text = await navigator.clipboard.readText();
  return { label: btn.textContent, same: text === (pre.querySelector("code") || pre).innerText };
});
check('laptop: Copy button says "Copied" and copies the code verbatim',
  clip.label === "Copied" && clip.same, JSON.stringify(clip));
const back = await copy.evaluate(async () => {
  await new Promise((r) => setTimeout(r, 1000));
  return document.querySelector(".copy-btn").textContent;
});
check('laptop: Copy label returns to "Copy" after a second', back === "Copy", back);

const paged = await page.evaluate(() => {
  document.dispatchEvent(new KeyboardEvent("keydown", { key: "]", bubbles: true }));
  return true;
});
await page.waitForURL(/07-backtracking/, { timeout: 4000 }).then(
  () => check('laptop: "]" goes to the next topic', true),
  () => check('laptop: "]" goes to the next topic', false, page.url()));
void paged;

await page.goto(`http://127.0.0.1:${PORT}/${TOPIC}`, { waitUntil: "load" });
await page.locator(".codewrap").first().waitFor();
const inputIgnored = await page.evaluate(() => {
  const i = document.createElement("input");
  document.body.appendChild(i);
  i.focus();
  i.dispatchEvent(new KeyboardEvent("keydown", { key: "]", bubbles: true }));
  return location.pathname;
});
check("laptop: bracket keys are ignored while typing in an input",
  inputIgnored.includes("06-trees"), inputIgnored);

await page.screenshot({ path: "/tmp/dsa-verify/shell-laptop-topic.png" });

/* -------------------------------------------------------- laptop: index */
console.log(`\n[laptop ${LAPTOP.width}x${LAPTOP.height}] index.html`);
await open(page, "index.html", LAPTOP);
await noSidewaysScroll(page, "laptop index");
const grid3 = await page.evaluate(() => {
  const g = document.querySelector(".topic-grid");
  const c = document.querySelector(".content").getBoundingClientRect();
  const body = document.body.getBoundingClientRect();
  return {
    cols: getComputedStyle(g).gridTemplateColumns.split(" ").length,
    centered: Math.abs((c.left + c.right) / 2 - body.width / 2) < 3,
  };
});
check("laptop: topic cards are three columns", grid3.cols === 3, grid3.cols + " columns");
check("laptop: index content column is centred (no empty sidebar gap)", grid3.centered);
await page.screenshot({ path: "/tmp/dsa-verify/shell-laptop-index.png" });

/* ------------------------------------------------------------ tablet */
console.log("\n[tablet 820x1180] index.html");
await open(page, "index.html", { width: 820, height: 1180 });
await noSidewaysScroll(page, "tablet index");
const grid2 = await page.evaluate(() =>
  getComputedStyle(document.querySelector(".topic-grid")).gridTemplateColumns.split(" ").length);
check("tablet: topic cards are two columns", grid2 === 2, grid2 + " columns");

/* ----------------------------------------- dark mode + token integrity */
console.log("\n[dark mode]");
const dark = await browser.newContext({ colorScheme: "dark" });
const dpage = await open(await dark.newPage(), TOPIC, PHONE);
const tokens = await dpage.evaluate(() => {
  const names = ["--bg", "--surface", "--ink", "--muted", "--line", "--ptr", "--ptr-soft",
    "--new", "--new-soft", "--null", "--code-bg", "--code-ink", "--kw", "--str", "--cmt", "--shadow"];
  const cs = getComputedStyle(document.documentElement);
  const missing = names.filter((n) => !cs.getPropertyValue(n).trim());
  const classes = [".nd", ".cell", ".t", ".ptr", ".cur", ".dot", ".arr", ".arrNew",
    ".arrOld", ".arrCur", ".mem"];
  const unstyled = classes.filter((sel) => {
    const el = document.querySelector(sel.slice(1) ? sel : sel);
    return el && !getComputedStyle(el).fill && !getComputedStyle(el).stroke;
  });
  return {
    missing, unstyled,
    bg: cs.getPropertyValue("--bg").trim(),
    ink: cs.getPropertyValue("--ink").trim(),
    body: getComputedStyle(document.body).backgroundColor,
    scheme: cs.colorScheme,
  };
});
check("dark: all 16 diagram tokens still resolve", tokens.missing.length === 0, tokens.missing.join(","));
check("dark: every SVG vocabulary class is still styled", tokens.unstyled.length === 0, tokens.unstyled.join(","));
check("dark: background is soft, not pure black",
  tokens.bg.toUpperCase() === "#0F141A" && tokens.body === "rgb(15, 20, 26)", `${tokens.bg} / ${tokens.body}`);
check("dark: text is soft, not pure white", tokens.ink.toUpperCase() === "#E8EDF3", tokens.ink);
check("dark: color-scheme is dark", tokens.scheme === "dark", tokens.scheme);
await dpage.screenshot({ path: "/tmp/dsa-verify/shell-dark-topic.png" });
await dark.close();

/* ------------------------------------------------------- extra widths */
console.log("\n[no sideways scroll across widths]");
for (const w of [320, 360, 390, 414, 430, 540, 768, 834, 1024, 1180, 1440, 1728]) {
  await open(page, TOPIC, { width: w, height: 900 });
  const m = await page.evaluate(() => {
    const d = document.documentElement;
    return d.scrollWidth <= d.clientWidth + 1;
  });
  check(`topic page at ${w}px wide`, m);
  await open(page, "index.html", { width: w, height: 900 });
  const m2 = await page.evaluate(() => {
    const d = document.documentElement;
    return d.scrollWidth <= d.clientWidth + 1;
  });
  check(`index at ${w}px wide`, m2);
}

await browser.close();
server.close();

console.log(`\n${pass} passed, ${fails.length} failed`);
if (fails.length) {
  fails.forEach((f) => console.log("  FAIL " + f));
  process.exit(1);
}
