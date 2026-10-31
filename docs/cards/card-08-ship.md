# Recipe Card 8: Ship — Docs to Site to PDF

**Use when:** chapters exist and edition one should become a thing.

## The loop (should take minutes, not days)

1. [ ] Draft in `docs/` as Markdown, one numbered file per chapter.
2. [ ] Build: script converts Markdown → HTML pages with shared layout, index
       ("Start here"), cards page, glossary, and one `print.html` (everything,
       in order, print stylesheet, page breaks between chapters).
3. [ ] Test: script checks chapters present, no broken internal links, no
       placeholder leaks, cards cover every chapter, print page complete.
4. [ ] Commit. Plain message.

## Build hygiene (the build obeys the book's own advice)

- [ ] No external calls: no web fonts, no analytics, no CDNs.
- [ ] System font stacks. Works offline. Static files only.
- [ ] Nothing hand-maintained that could be derived (chapters list, cards page, glossary page all generated).

## PDF without a PDF service

- Open `print.html` in the browser → File → Print → Save as PDF.
- Spot-check page breaks fall between chapters, never mid-step.

## Release checklist

- [ ] Build passes clean (zero warnings, zero errors).
- [ ] Test suite passes: links, placeholders, cards, glossary, print page.
- [ ] Print preview spot-checked on 3 pages.
- [ ] No placeholder text leaked into any output page.
- [ ] `claims.md` reviewed; volatile claims dated.
- [ ] Honest version label on the index: "Edition 1.0," dated.
- [ ] One friend completed the book's first project successfully.
- [ ] Committed, plain message. Nothing published if you don't want it yet.

## Editions finish; projects continue

Corrections from `claims.md` go back into this edition. Everything else waits
for edition two, scoped with Card 2 from the start.
