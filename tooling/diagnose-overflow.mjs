/* Prints every element that overflows the viewport, with its ancestor chain.
   node tooling/diagnose-overflow.mjs [page] [width] */
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";

const ROOT = process.cwd();
const PORT = 8942;
const PAGE = process.argv[2] || "topics/06-trees.html";
const WIDTH = Number(process.argv[3] || 390);
const { chromium } = createRequire("/tmp/dsa-verify/")("playwright");

const server = http.createServer((req, res) => {
  const rel = decodeURIComponent(req.url.split("?")[0]).replace(/^\/+/, "") || "index.html";
  const file = path.join(ROOT, rel);
  if (!file.startsWith(ROOT) || !fs.existsSync(file)) return res.writeHead(404).end("no");
  const ext = path.extname(file);
  const type = ext === ".css" ? "text/css" : ext === ".js" ? "text/javascript" : "text/html";
  res.writeHead(200, { "content-type": type });
  res.end(fs.readFileSync(file));
});
await new Promise((r) => server.listen(PORT, r));

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: WIDTH, height: 900 } });
await page.goto(`http://127.0.0.1:${PORT}/${PAGE}`, { waitUntil: "load" });
await page.locator(".codewrap, .topic-grid").first().waitFor();

const report = await page.evaluate(() => {
  const d = document.documentElement;
  const rows = [];
  const chain = (el) => {
    const parts = [];
    for (let p = el; p && p !== document.body; p = p.parentElement) {
      parts.unshift(p.tagName.toLowerCase() +
        (p.className && typeof p.className === "string" ? "." + p.className.split(" ")[0] : "") +
        ":" + getComputedStyle(p).overflowX[0]);
    }
    return parts.join(" > ");
  };
  for (const el of document.querySelectorAll("body *")) {
    if (getComputedStyle(el).position === "fixed") continue;
    const r = el.getBoundingClientRect();
    if (r.right <= d.clientWidth + 1) continue;
    let p = el.parentElement, contained = false;
    while (p && p !== document.body && !contained) {
      if (getComputedStyle(p).overflowX !== "visible") contained = true;
      p = p.parentElement;
    }
    if (contained) continue;
    rows.push({
      right: Math.round(r.right), width: Math.round(r.width),
      text: (el.textContent || "").trim().slice(0, 70),
      chain: chain(el),
    });
  }
  return { scrollW: d.scrollWidth, clientW: d.clientWidth, rows };
});

console.log(`${PAGE} at ${WIDTH}px: scrollWidth=${report.scrollW} clientWidth=${report.clientW}\n`);
for (const r of report.rows) {
  console.log(`right=${r.right} width=${r.width}`);
  console.log(`  chain: ${r.chain}`);
  console.log(`  text : ${JSON.stringify(r.text)}\n`);
}
if (!report.rows.length) console.log("no uncontained overflow");

await browser.close();
server.close();
