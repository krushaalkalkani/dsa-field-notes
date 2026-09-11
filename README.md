# DSA Field Notes

Visual study notes for the NeetCode **Algorithms and Data Structures for Beginners** course.
12 topic pages, 34 lessons, Python only. Static HTML, no build step, works on GitHub Pages as-is.

Live site: https://krushaalkalkani.github.io/dsa-field-notes/

## What is on every page

| Section | What it gives you |
|---|---|
| Why | A real-world analogy, the technical idea, one diagram of the core mechanism |
| One section per lesson | Every fact, example and code snippet from the NeetCode lesson, with trace tables and diagrams |
| Patterns | The 2-4 "moves" interviews test on this topic, each with a tested Python template |
| Big-O | One table, asterisks explained |
| Mistakes | Real beginner bugs with the fix, plus interview one-liners |
| Practice | 8-12 LeetCode problems in order, tagged with the move each trains |
| Self-check | 10-13 questions with hidden answers |

Diagram convention: teal = existing link, **orange = what changed in this step**, dashed grey = old link, faded = unreachable or unvisited, red ∅ = None.

## Layout

```
index.html                  course map
assets/style.css            shared styles (light + dark, phone-friendly)
assets/nav.js               topic-page helpers: pager shortcuts and code-copy buttons
topics/01-arrays.html ...   one page per topic
topics/12-bit-manipulation.html
checks/                     every code block on the pages, as runnable Python with asserts
tooling/TEMPLATE.html       skeleton for a new topic page
tooling/STYLE_GUIDE.md      writing and diagram rules for new pages
tooling/verify_pages.py     structural check for every page (closed tags, nav anchors, dead links)
```

## Reading shortcuts

- On the course map, tick **Done** on a card to track progress. The count sits under the heading and is kept in `localStorage`, on your machine only.
- On a topic page, press `[` for the previous topic and `]` for the next.
- Hover a code block and press **Copy** to take the Python without the line noise.

## Verify the code

```bash
for f in checks/*.py; do python3 "$f" | tail -1; done   # each prints "all checks passed"
```

## Deploy on GitHub Pages

1. Push this folder to a repository (the site root is the repo root).
2. Settings -> Pages -> Source: "Deploy from a branch", branch `main`, folder `/ (root)`.
3. Wait a minute, open `https://<user>.github.io/<repo>/`.

## Adding a topic (e.g. from the NeetCode Advanced course)

Copy `tooling/TEMPLATE.html` to `topics/13-<slug>.html`, follow `tooling/STYLE_GUIDE.md`, add a card to `index.html`, and fix the prev/next links on the neighbors. Write `checks/13-<slug>.py` first and make it pass before writing the page.

## Credits

Course structure and lesson content: [NeetCode](https://neetcode.io/courses/dsa-for-beginners/0). Diagrams, trace tables, patterns, mistakes and quizzes are original study material by Krushal Kalkani, built with Claude.
