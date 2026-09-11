# DSA Field Notes - page writing guide

You are writing ONE topic page of a study-notes website for the NeetCode "DSA for Beginners" course. The reader is Krushal: MS CS grad, non-native English speaker (Gujarati first), visual learner, preparing for FAANG-style interviews in Python. Other learners will also read the site.

Read these three files before writing anything:
1. `tooling/TEMPLATE.html` - the page skeleton. Copy its structure exactly (head, shared SVG defs, site-head, top header, sections nav, sections, pager, footer).
2. `topics/02-linked-lists.html` - the finished reference page. Match its depth, tone, diagram style, and section pattern. Your page must look like it was written by the same person.
3. `lessons/<your topic>.md` - the NeetCode lesson text. Every fact, code snippet, complexity claim, example array, and "note" in that file MUST appear in your page. Do not skip anything from the lessons. You may ADD (patterns, Python idioms, more examples) but never drop.

## Page structure (in this order)

0. **Why** - analogy card first (`.analogy`), then the technical framing, then one diagram that shows the core mechanism.
1..N. **One section per lesson** (or per big idea if a lesson is small). Inside each: `h3` sub-ideas, code in `<pre><code>` with the `.k .s .c` spans for keywords/strings/comments, at least one `<figure>` with an SVG diagram per lesson, a trace table (`.tbl > table`) wherever the lesson walks through an example step by step, and `.callout` boxes for the things people get wrong (`.callout.keep` = "Keep in mind", plain `.callout` = warning with your own short label).
- **Patterns** - 2 to 4 interview "moves" for this topic, each with a tested Python template and a one-line "when to use". Examples: two pointers, sliding window (arrays); prev/cur/nxt (linked lists); dummy node; slow/fast; memo decorator (DP); directions array (grids); level-size loop (BFS).
- **Big-O summary** - one table. Use `class="big fast"` for good complexities and `class="big slow"` for bad ones. Explain any asterisk.
- **Mistakes to watch for** - 6 to 9 `.mistake` cards: real bugs beginners write, each with the fix. Then the `.cheat` block: 5-7 "Interview one-liners" the reader can say out loud.
- **Practice, in this order** - 8 to 12 LeetCode problems as a table (#, name, move it trains, level), ordered easy to medium, ending with "Your next step today: <one problem>". Use real LeetCode numbers you are certain of. If unsure of a number, omit the number rather than guess.
- **Self-check** - 10 to 12 `<details>` questions with hidden answers, including at least 2 "trace it" questions (given input, what is the state after each step).

## Diagrams (this is what makes the site worth having)

- Hand-write inline SVG. `viewBox` sized to content (typically 620-700 wide, 120-260 tall). No external images, no libraries, no `<style>` inside SVG.
- Use ONLY the CSS classes in `assets/style.css`: `.nd` (box), `.nd.dim` (faded), `.nd.newnd` (orange outline = new), `.cell` (divider line), `.t` (text), `.t.small`, `.t.mono`, `.t.ptrlab` (teal label), `.t.newlab` (orange label), `.t.nulltxt` (red, for None/∅), `.ptr` (teal pointer line), `.ptr.newp` (orange = changed), `.ptr.old` (dashed grey = old), `.ptr.prevp` (faded teal), `.cur` (ink cursor line), `.dot` / `.dot.newd`, `.mem` (dashed memory region).
- Arrowheads: `marker-end="url(#arr)"` teal, `url(#arrNew)` orange, `url(#arrOld)` grey, `url(#arrCur)` ink. The `<defs>` are already in the template; do not redefine them.
- **The one rule: orange marks what changed in this step.** Old state dashed grey, new state orange, everything else teal/ink. Number the steps ①②③ inside the drawing when order matters.
- Every figure: `role="img"` + `aria-label` on the svg, and a `<figcaption>` that starts with a bold claim (`<b>...</b>`) then one or two sentences of what to notice.
- Trees: draw nodes as circles (`<circle class="nd" r="18">`) with values centered; edges as `.ptr` lines; recursion order as small numbers in `.t.newlab` beside nodes. Arrays/grids: rows of `.nd` rects with index labels in `.t.small` underneath. Recursion: draw the call tree or a call-stack column. Heaps: draw BOTH the tree and the 1-indexed array under it. Graphs: nodes as circles with labeled directed edges.
- Align to a grid. Even spacing. Text 11-13px. Labels must not overlap boxes or each other (check coordinates).
- Aim for 5-9 diagrams per page. One per mechanism, not one per paragraph.

## Writing rules

- Simple English. Short sentences. Define each technical term the first time in `<dfn>`: e.g. `<dfn>amortized</dfn> means "averaged over many operations"`.
- Learning order inside each idea: real-world example -> technical explanation -> small parts -> practical use -> visual.
- Use hyphens, never em dashes. No emoji. No filler ("In this section we will..."). No "genuinely", "honestly", "straightforward".
- Trace examples with the SAME arrays/trees the NeetCode lesson uses, so the notes match the videos.
- Python is the only language. Use `None`, not `null`, in code; you may mention that NeetCode says `null`.
- Where NeetCode's code is pseudocode-ish, keep the NeetCode version AND add the idiomatic Python (e.g. `arr[j], arr[j+1] = arr[j+1], arr[j]`, `collections.deque`, `heapq`, `functools.lru_cache`, `Counter`).

## Code must run

Before writing the HTML, write `checks/<topic>.py` containing every function/class that will appear on the page, with `assert` tests on the lesson's own examples (e.g. `assert insertionSort([2,3,4,1,6]) == [1,2,3,4,6]`), and run it with `python3`. Fix until it prints `all checks passed`. Only then paste the code into the page, escaping `<` as `&lt;` and `>` as `&gt;` and `&` as `&amp;` inside `<pre><code>`.

## Files

- Write the page to `topics/<NN>-<slug>.html` (given in your task).
- Write the check script to `checks/<NN>-<slug>.py`.
- The pager links use the neighbor filenames given in your task. Index link is `../index.html`. Stylesheet is `../assets/style.css`.
- Do not modify `assets/style.css`, `tooling/TEMPLATE.html`, or any other page.

## Size

Roughly 700-1100 lines of HTML. If a topic has 4-6 lessons (Arrays, Trees, Graphs, Sorting) go longer, not shallower. Depth over polish: a correct trace table beats a decorative flourish.

## Done means

1. `python3 checks/<file>.py` prints `all checks passed`.
2. `python3 -c "import html.parser"`-style sanity: the file opens, every `<section>` in the nav exists, no `{{placeholders}}` remain (`grep -c '{{' file` is 0).
3. Every lesson fact from the `.md` is on the page.
4. Report back: file path, number of diagrams, number of code blocks, list of LeetCode problems used, and anything from the lesson you were unsure how to represent.
