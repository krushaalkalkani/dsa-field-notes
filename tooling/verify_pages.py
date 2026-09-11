"""Structural check for every HTML page. Run: python3 tooling/verify_pages.py"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["index.html"] + sorted(
    os.path.join("topics", n) for n in os.listdir(os.path.join(ROOT, "topics"))
    if n.endswith(".html")
)

NAV_RE = re.compile(r'<nav[^>]*class="sections"[^>]*>(.*?)</nav>', re.S)
HREF_RE = re.compile(r'href="([^"]+)"')
SRC_RE = re.compile(r'src="([^"]+)"')
SECTION_ID_RE = re.compile(r'<section[^>]*\sid="([^"]+)"')
ANY_ID_RE = re.compile(r'\sid="([^"]+)"')


def check(rel):
    path = os.path.join(ROOT, rel)
    with open(path, encoding="utf-8") as fh:
        html = fh.read()

    problems = []

    if html.rstrip().endswith("</html>"):
        closed = "closed"
    else:
        closed = "NOT CLOSED"
        problems.append("does not end with </html>")

    braces = html.count("{{")
    if braces:
        problems.append(f"{braces} '{{{{' placeholder(s)")

    section_ids = set(SECTION_ID_RE.findall(html))
    all_ids = set(ANY_ID_RE.findall(html))

    nav = NAV_RE.search(html)
    nav_links = HREF_RE.findall(nav.group(1)) if nav else []
    nav_anchors = [h[1:] for h in nav_links if h.startswith("#")]
    for anchor in nav_anchors:
        if anchor not in section_ids:
            where = "non-section element" if anchor in all_ids else "MISSING"
            problems.append(f"nav #{anchor} -> {where}")

    rel_links = 0
    for href in HREF_RE.findall(html) + SRC_RE.findall(html):
        if href.startswith(("#", "http://", "https://", "mailto:", "//", "data:")):
            continue
        rel_links += 1
        target = href.split("#")[0].split("?")[0]
        if not target:
            continue
        if not os.path.exists(os.path.join(os.path.dirname(path), target)):
            problems.append(f"dead link {href}")

    sections = len(SECTION_ID_RE.findall(html))
    pres = len(re.findall(r"<pre[ >]", html))
    status = "OK" if not problems else "FAIL: " + "; ".join(problems)
    print(
        f"{rel:36s} {closed:10s} braces={braces}  "
        f"nav={len(nav_anchors):2d}/{sections:2d} sections  "
        f"rel-links={rel_links:2d}  pre={pres:2d}  {status}"
    )
    return not problems


if __name__ == "__main__":
    results = [check(p) for p in PAGES]
    print()
    if all(results):
        print(f"all {len(results)} pages OK")
    else:
        print(f"{results.count(False)} of {len(results)} pages FAILED")
        sys.exit(1)
