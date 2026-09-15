"""Prove the redesign did not touch note content.

For every topics/*.html, compares the committed version against the working
tree on the parts that are content: code blocks, SVG diagrams, captions,
table cells, quiz details, and every heading/paragraph/list item.

Usage:  python3 tooling/verify_content.py [git-ref]     (default: HEAD)
"""
import re
import subprocess
import sys

REF = sys.argv[1] if len(sys.argv) > 1 else "HEAD"

PARTS = [
    ("pre blocks", re.compile(r"<pre\b.*?</pre>", re.S)),
    ("svg diagrams", re.compile(r"<svg\b.*?</svg>", re.S)),
    ("figcaptions", re.compile(r"<figcaption\b.*?</figcaption>", re.S)),
    ("table cells", re.compile(r"<t[dh]\b.*?</t[dh]>", re.S)),
    ("details blocks", re.compile(r"<details\b.*?</details>", re.S)),
    ("headings", re.compile(r"<h[123]\b.*?</h[123]>", re.S)),
    ("paragraphs", re.compile(r"<p\b.*?</p>", re.S)),
    ("list items", re.compile(r"<li\b.*?</li>", re.S)),
    ("callouts", re.compile(r'<div class="callout.*?</div>', re.S)),
]


def files():
    out = subprocess.run(
        ["git", "ls-tree", "--name-only", REF, "topics/"],
        capture_output=True, text=True, check=True,
    ).stdout.split()
    return [f for f in out if f.endswith(".html")]


def old(path):
    return subprocess.run(
        ["git", "show", "%s:%s" % (REF, path)],
        capture_output=True, text=True, check=True,
    ).stdout


def main():
    bad = 0
    totals = {}
    for path in files():
        before, after = old(path), open(path, encoding="utf-8").read()
        row = []
        for label, rx in PARTS:
            a, b = rx.findall(before), rx.findall(after)
            totals[label] = totals.get(label, 0) + len(a)
            if a == b:
                row.append("%s=%d ok" % (label.split()[0], len(a)))
            else:
                row.append("%s MISMATCH (%d -> %d)" % (label, len(a), len(b)))
                bad += 1
                for x, y in zip(a, b):
                    if x != y:
                        print("  first differing %s in %s:" % (label, path))
                        print("   before: %s" % x[:160].replace("\n", " "))
                        print("   after : %s" % y[:160].replace("\n", " "))
                        break
        print("%-36s %s" % (path, "  ".join(row)))

    print()
    for label, n in sorted(totals.items()):
        print("  %-16s %d compared, all identical" % (label, n))
    print()
    if bad:
        sys.exit("%d content mismatches" % bad)
    print("CONTENT IDENTICAL in all %d topic pages" % len(files()))


if __name__ == "__main__":
    main()
