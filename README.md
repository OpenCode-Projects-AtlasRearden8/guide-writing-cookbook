The Guide-Writing Cookbook
===========================

Plain-friendly manuals, the Asdale way — a working cookbook for writing manuals
that people actually finish and actually use. Pick a topic that hurts someone
today, scope a first edition you can finish, draft in plain English, teach in
steady step-by-step rhythms, edit for dignity and warmth without ever
condescending, turn chapters into printables and tool ideas, verify every claim,
and ship from docs to a static site to a print-ready PDF.

**By Dylan Asdale and Asdale Dynamics, LLC.** Licensed MIT.

Contents
--------

- `docs/` — the book itself: an introduction, eight chapters, the tone
  checklist, a glossary, and `cards/` with one-page chapter-recipe cards.
- `build.py` — turns `docs/` into a static site in `site/` (11 chapter pages,
  9 card pages, a cards index, and one print-ready `print.html`).
- `tests/test.py` — a verification suite for the build (links, badges, cards,
  print page, license wording, secret-pattern scan).

Read it
-------

Open `docs/00-introduction.md`, or build the site and read it there:

    python3 build.py
    # then open site/index.html in your browser

Companion project
-----------------

This cookbook is the writing manual; the **open-book-starter-template** is the
scaffold it plugs into (folder layout, build setup, conventions). The starter
answers *"what do my folders look like?"*; this book answers *"what do my
sentences sound like?"*. They complement each other and deliberately don't
repeat each other.

Print a PDF without any service
-------------------------------

1. `python3 build.py`
2. Open `site/print.html` in a browser
3. File → Print → Save as PDF

The print page contains the complete book — all chapters, the tone checklist,
the glossary, and the recipe cards — with page breaks between chapters and
styles that print cleanly in black and white.

Run the tests
-------------

    python3 tests/test.py

The suite checks that the build runs clean, every generated page exists and its
internal links and anchors resolve, no placeholder text leaks into the output,
the print page contains the whole book, the LICENSE copyright line is exact,
the README credit is present, and no obvious token/key patterns appear in any
repo file.

Local-first
-----------

Everything here works from files you own. No accounts, no servers, no analytics,
no external fonts or scripts. Copy the folder anywhere and it still builds,
tests, and reads.

License
-------

MIT — see [LICENSE](LICENSE). © Asdale Dynamics, LLC
