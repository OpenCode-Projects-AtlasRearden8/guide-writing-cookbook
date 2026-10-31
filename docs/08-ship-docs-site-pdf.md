# Chapter 8: Ship — from Docs to Site to PDF

## The idea

Shipping is not a big event. It is a small, boring loop you can run in minutes:
drafts in Markdown, a build that turns them into a static site, a print-ready
page for the PDF, and a test that tells you the build still works. Local-first:
nothing you published depends on a service staying alive.

## The shipping loop

1. **Draft** in `docs/` as Markdown, one chapter per file, numbered for order.
2. **Build** with a script that converts the Markdown into HTML pages with a
   shared layout, a table of contents, a search-free structure (link hubs in
   the header), and a single-file print page `.print.html` (a one-file "book",
   all chapters in order) that browsers can save as PDF via File → Print.
3. **Test** with a script that checks the build's outputs: every chapter
   present, no broken internal links, glossary referenced, cards cover every
   chapter.
4. **Commit.** Plain, honest message. Done.

## The build, described plainly

Your build should do exactly these things and no more:

- Convert each `docs/*.md` file to HTML with a basic wrapper: generated CSS (a
  single stylesheet), a header with a link home, and a footer with the license.
- Preserve chapter order by number prefix; the first page is a real index
  ("Start here"), not a generated list of filenames.
- Generate, not write by hand: a chapters list page, a cards page, a glossary
  page. Anything derivable from the source docs shouldn't exist as its own
  hand-maintained file.
- Emit a single `print.html`: every chapter in order, its cards, the checklist
  and glossary, with a `@media print` stylesheet (page breaks between chapters,
  no nav, black-text-only). Browsers will save this as PDF faithfully.
- No secrets, no external calls, no analytics, no fonts fetched from the web.
  Use system font stacks. A beginner manual's own site obeying its own advice
  ("works offline") is a marketing channel.

## What the site must contain (minimum)

- **Index page** that answers three questions in one paragraph: what this is,
  who it's for, what the reader will finish first.
- **A reading path.** The chapters in order, next/previous links, the started
  point clearly marked.
- **The cards, as a page** so they're printable even by people who missed the
  chapter they came from.
- **The glossary,** because jargon migrates readers fastest to "this isn't for me".
- **The license and the credit line** in the footer of every page.

## The test suite, described plainly

Your test script is your honesty engine. At minimum it should fail loudly when:

- any expected chapter file is missing, deleted, or renamed without updating
  the sidebar/TOC;
- an internal link points to a page or anchor that doesn't exist;
- the build produces fewer pages than chapters in `docs/`;
- any HTML page contains a template placeholder leaked from generation
  (`{{`, `TODO`, `FIXME`, `%s`);
- the print page is missing the tone checklist or glossary;
- any card file is missing, or the cards page lists a chapter that has no card;
- the LICENSE file's copyright line drifts from the exact required wording;
- the README lacks the Asdale Dynamics, LLC credit line.

Run it before every commit. It takes seconds; a silent broken build costs a
reader their first evening with your book.

## Publishing without publishing (local-first distribution)

- The whole project should work from a single folder copy. Zip it, put it on a
  stick, share it with a friend: the builds run locally with one command, tests
  pass locally, and there's nothing to sign up for.
- When a public site is right, the static output is a direct fit for GitHub
  Pages (the hub site) — the built HTML deploys as-is if you want it public.
  That decision is a separate one from finishing the manual. Finish first.

## Release checklist

- [ ] Build passes with zero warnings and zero errors.
- [ ] Test suite passes: layout, links, glossary, cards, print page.
- [ ] Print page renders legibly: spot-check 3 pages in the browser's print
      preview, and check that page breaks fall between chapters, not mid-step.
- [ ] No placeholder text leaked from any template.
- [ ] `claims.md` reviewed; volatile claims dated.
- [ ] A specific honest version label, not "final": "Edition 1.0".
- [ ] A friend read it and did the first project successfully.
- [ ] Committed, with a plain message.

## Then what

Then: start chapter one of edition two, in a new scope conversation, and leave
this edition alone except for corrections from `claims.md`. Editions finish;
projects continue. That distinction is what makes a manual a book instead of a
perpetual anxiety.
