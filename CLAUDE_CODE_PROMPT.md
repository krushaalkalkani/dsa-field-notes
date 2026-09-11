# Claude Code prompt: launch the DSA Field Notes site

Copy everything inside the code block below and paste it into Claude Code, run from inside the unzipped `dsa-field-notes` folder. It takes the finished site, checks it, adds three small features, and deploys it to GitHub Pages. Do the two manual steps at the top first.

Before you paste:
1. Unzip `dsa-field-notes.zip` and `cd` into the folder.
2. Make sure `gh auth status` works (GitHub CLI logged in).

```text
You are working inside a finished static website: "DSA Field Notes", visual study notes for the NeetCode "Algorithms and Data Structures for Beginners" course. Read README.md and tooling/STYLE_GUIDE.md first. Do not rewrite content, do not change the visual design, do not touch topics/*.html except where a task below says so.

Goal: verify, add three small features, publish on GitHub Pages, and give me a working URL.

Step 1 - Verify what exists (report before changing anything)
- List the files. Confirm index.html, assets/style.css, topics/01-arrays.html through topics/12-bit-manipulation.html, checks/*.py, tooling/.
- Run every check script: for f in checks/*.py; do python3 "$f" | tail -1; done. All 12 must print "all checks passed". If one fails, show me the error and stop.
- Open each HTML file and confirm: it ends with </html>, contains no "{{" placeholders, every href="#..." in the sections nav has a matching <section id="...">, and every relative href points to a file that exists. Print a one-line summary per page.

Step 2 - Three small features (keep each under 60 lines; inline JS at the bottom of the file, no libraries, no build step)
a) Progress tracking on index.html: add a small "Done" checkbox to each topic card (top-right corner, keyboard accessible). Persist to localStorage under the key "dsa-notes-done" (wrap every localStorage call in try/catch). Show "X of 12 done" under the Course map heading. Style it with the existing CSS tokens (var(--ptr), var(--line)) so it works in dark mode.
b) Keyboard navigation on topic pages: pressing "[" goes to the previous topic and "]" goes to the next, using the existing .pager links. Ignore keypresses inside inputs. Add this as a tiny shared file assets/nav.js and include it with <script src="../assets/nav.js" defer></script> before </body> on all 12 topic pages.
c) A "Copy" button on every <pre> code block on topic pages (also in assets/nav.js): a small button at the top-right of the block that copies the block's plain text and reads "Copied" for one second. Keep the code text unchanged.
After adding these, re-run Step 1's HTML checks.

Step 3 - Repository and deploy
- git init if needed, add a .nojekyll file at the root, commit everything with the message "DSA Field Notes: 12 topic pages, checks, progress tracking, keyboard nav".
- Create a public GitHub repository named dsa-field-notes with gh repo create (ask me before creating if a repo with that name already exists), push main.
- Enable GitHub Pages from the main branch, root folder, using: gh api -X POST repos/{owner}/dsa-field-notes/pages -f "source[branch]=main" -f "source[path]=/" (if it returns "already exists", use PUT instead).
- Poll gh api repos/{owner}/dsa-field-notes/pages until status is "built" (max 3 minutes), then curl the URL and confirm the index and one topic page return 200.
- Replace the "Live site:" placeholder line in README.md with the real URL, commit, push.

Step 4 - Report
Give me: the live URL, the repo URL, the output of the check-script loop, and a 5-line summary of what you changed. Then give me exactly one next action: "Open <URL>/topics/02-linked-lists.html, then solve LeetCode 206 with the page closed."

Rules: prefer small, reversible edits. Never delete or overwrite topic content. If anything is ambiguous, pick the option that keeps the site static and dependency-free.
```

## Later: adding the NeetCode Advanced course (separate prompt, run only after you have finished the beginner practice lists)

```text
Read tooling/STYLE_GUIDE.md, tooling/TEMPLATE.html and topics/02-linked-lists.html (the reference page). I will paste the text of one NeetCode Advanced Algorithms lesson group. Write checks/13-<slug>.py first with asserts on the lesson's own examples and make it pass, then write topics/13-<slug>.html following the guide exactly (analogy, one section per lesson with SVG diagrams where orange marks what changed, patterns, Big-O table, mistakes, practice list with LeetCode numbers you are sure of, self-check). Add a card to index.html and fix the prev/next pager on the neighbor pages. Do not change any other page.
```
