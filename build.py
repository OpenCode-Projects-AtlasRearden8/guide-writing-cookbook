#!/usr/bin/env python3
"""Build the Guide-Writing Cookbook static site.

Converts docs/*.md into static HTML pages in site/ plus one print-ready
print.html for making a PDF with the browser's "Print -> Save as PDF".

Local-first: pure Python plus the `markdown` package (3.x). No network calls.
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

try:
    import markdown as md
except ImportError:
    sys.stderr.write(
        "error: the 'markdown' package is required.\n"
        "Install it with: python3 -m pip install --user markdown\n"
    )
    sys.exit(1)

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"
CARDS = DOCS / "cards"

TITLE = "The Guide-Writing Cookbook"
SUBTITLE = "Plain-friendly manuals, the Asdale way"
FOOTER = (
    "The Guide-Writing Cookbook &middot; by Dylan Asdale, "
    "Asdale Dynamics, LLC &middot; MIT License"
)

CHAPTER_FILES = [
    "00-introduction.md",
    "01-pick-a-bleeding-topic.md",
    "02-scope-first-edition.md",
    "03-plain-english-rules.md",
    "04-lesson-rhythms.md",
    "05-edit-for-dignity.md",
    "06-printables-and-tools.md",
    "07-verify-every-claim.md",
    "08-ship-docs-site-pdf.md",
]

TOC_LABELS = {
    "00-introduction": "Introduction",
    "01-pick-a-bleeding-topic": "1. A Topic That Hurts",
    "02-scope-first-edition": "2. Scope a First Edition",
    "03-plain-english-rules": "3. Plain-English Rules",
    "04-lesson-rhythms": "4. Lesson Rhythms",
    "05-edit-for-dignity": "5. Dignity &amp; Warmth",
    "06-printables-and-tools": "6. Printables &amp; Tools",
    "07-verify-every-claim": "7. Verify Every Claim",
    "08-ship-docs-site-pdf": "8. Ship It",
}


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9\s-]", "", text.lower().strip())
    return re.sub(r"[\s_-]+", "-", s).strip("-") or "section"


def add_heading_ids(body_html: str) -> str:
    """Give h2/h3 elements ids so intra-page anchors resolve."""

    def repl(m: re.Match) -> str:
        tag, attrs, inner = m.group(1), m.group(2), m.group(3)
        if "id=" in attrs:
            return m.group(0)
        plain = re.sub(r"<[^>]+>", "", inner)
        return f'<{tag}{attrs} id="{slugify(html.unescape(plain))}">{inner}</{tag}>'

    return re.sub(r"<(h[23])([^>]*)>(.*?)</\1>", repl, body_html, flags=re.S)


def render_markdown(text: str) -> str:
    return add_heading_ids(md.markdown(text, extensions=["tables", "fenced_code", "sane_lists"]))


def first_h1(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "Untitled"


PAGE_CSS = """
:root {
  --ink: #1f2430; --muted: #5c6472; --paper: #fdfcf8; --card: #f4f1ea;
  --accent: #205e61; --accent-soft: #e3efee; --rule: #ddd6c8;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--paper); color: var(--ink);
  font: 16px/1.65 Georgia, "Times New Roman", serif; }
.shell { display: flex; min-height: 100vh; }
nav.toc { width: 220px; flex: 0 0 220px; padding: 1.5rem 1rem; font-size: 0.85rem;
  border-right: 1px solid var(--rule); background: var(--card);
  font-family: system-ui, sans-serif; position: sticky; top: 0;
  height: 100vh; overflow-y: auto; }
nav.toc .logo { font-weight: 700; color: var(--accent); margin-bottom: 1rem;
  line-height: 1.3; }
nav.toc a { display: block; padding: 0.28rem 0.25rem; color: var(--ink);
  text-decoration: none; border-radius: 4px; }
nav.toc a:hover { background: var(--accent-soft); color: var(--accent); }
nav.toc a.active { background: var(--accent-soft); color: var(--accent);
  font-weight: 600; }
main { max-width: 46rem; padding: 2.5rem 2rem 4rem; }
main.paged { max-width: 52rem; }
h1 { font-size: 1.9rem; line-height: 1.25; color: var(--accent); }
h2 { font-size: 1.35rem; margin-top: 2.2rem;
  border-bottom: 1px solid var(--rule); padding-bottom: 0.3rem; }
h1, h2, h3 { font-family: "Iowan Old Style", Palatino, Georgia, serif; }
code { background: var(--card); padding: 0.1em 0.35em; border-radius: 3px;
  font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace; font-size: 0.92em; }
pre { background: var(--card); padding: 0.8rem 1rem; overflow-x: auto;
  border: 1px solid var(--rule); border-radius: 6px; }
pre code { padding: 0; background: none; }
blockquote { margin: 1rem 0; padding: 0.4rem 1.1rem;
  border-left: 3px solid var(--accent); background: var(--accent-soft);
  border-radius: 0 6px 6px 0; }
table { border-collapse: collapse; width: 100%; margin: 1rem 0;
  font-family: system-ui, sans-serif; font-size: 0.88rem; }
th, td { border: 1px solid var(--rule); padding: 0.45rem 0.6rem;
  text-align: left; vertical-align: top; }
th { background: var(--card); }
li { margin: 0.15rem 0; }
header.site { background: var(--accent); color: #fff; padding: 0.75rem 1.5rem;
  font-family: system-ui, sans-serif; display: flex;
  justify-content: space-between; align-items: baseline; flex-wrap: wrap;
  gap: 0.4rem; }
header.site b { font-size: 1.05rem; }
header.site span { font-size: 0.8rem; opacity: 0.85; }
footer.site { font-family: system-ui, sans-serif; font-size: 0.78rem;
  color: var(--muted); text-align: center; padding: 1.2rem; }
.cardgrid { display: grid; gap: 1rem; margin-top: 1.5rem; }
.cardgrid article, article.card { background: var(--card);
  border: 1px solid var(--rule); border-radius: 8px;
  padding: 1rem 1.2rem; }
article.card + article.card { margin-top: 1rem; }
.cardgrid h1 { display: none; }
.cardgrid h2 { font-size: 1.1rem; margin-top: 0.6rem; border: none; }
a { color: var(--accent); }
@media (max-width: 760px) { .shell { display: block; }
  nav.toc { position: static; width: auto; height: auto; border-right: 0;
    border-bottom: 1px solid var(--rule); } }
@media print {
  nav.toc, header.site, footer.site { display: none; }
  .shell { display: block; }
  body { background: #fff; font-size: 11pt; }
  main { max-width: none; padding: 0; }
  h2 { break-after: avoid; }
  table, pre, blockquote { break-inside: avoid; }
  article.card { break-inside: avoid; page-break-inside: avoid;
    border: 1px solid #999; }
  section.chapter { break-before: page; }
  section.chapter:first-child { break-before: auto; }
}
"""


def wrap_page(title: str, body: str, toc_html: str, active: str) -> str:
    header = (
        f'<header class="site"><b>{html.escape(TITLE)}</b>'
        f"<span>{html.escape(SUBTITLE)}</span></header>"
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} — {html.escape(TITLE)}</title>
<style>{PAGE_CSS}</style>
</head>
<body>
{header}
<div class="shell">
{toc_html}
<main class="{"paged" if toc_html else ""}">{body}</main>
</div>
<footer class="site">{FOOTER}</footer>
</body>
</html>"""


TOC_LINKS = [
    ("index.html", "Start Here"),
    *((stem + ".html", TOC_LABELS.get(stem, stem)) for stem in
      [p.removesuffix(".md") for p in CHAPTER_FILES[1:]]),
    ("cards.html", "Recipe Cards"),
    ("checklist-tone.html", "Tone Checklist"),
    ("glossary.html", "Glossary"),
    ("print.html", "Printable Book (PDF)"),
]


def build_toc(active: str) -> str:
    items = [
        f'<a href="{href}"{" class=\"active\"" if href == active else ""}>'
        f"{label}</a>"
        for href, label in TOC_LINKS
    ]
    return (
        f'<nav class="toc"><div class="logo">{html.escape(TITLE)}'
        f"<br><small>{html.escape(SUBTITLE)}</small></div>"
        + "\n".join(items)
        + "</nav>"
    )


def main() -> int:
    missing = [f for f in CHAPTER_FILES if not (DOCS / f).is_file()]
    if missing:
        sys.stderr.write(f"error: docs/ is missing chapter files: {missing}\n")
        return 1
    SITE.mkdir(exist_ok=True)

    card_files = sorted(CARDS.glob("card-*.md")) if CARDS.is_dir() else []

    text_by_stem: dict[str, str] = {}
    for name in CHAPTER_FILES:
        path = DOCS / name
        text_by_stem[path.stem] = path.read_text(encoding="utf-8")
    for extra in ("checklist-tone.md", "glossary.md"):
        path = DOCS / extra
        if path.is_file():
            text_by_stem[path.stem] = path.read_text(encoding="utf-8")
    card_text_by_stem = {p.stem: p.read_text(encoding="utf-8") for p in card_files}

    # Per-chapter pages plus the two special pages.
    for stem, text in text_by_stem.items():
        title = first_h1(text)
        page = wrap_page(
            title,
            f'<section class="chapter">{render_markdown(text)}</section>',
            build_toc(stem + ".html"),
            stem + ".html",
        )
        (SITE / f"{stem}.html").write_text(page, encoding="utf-8")

    # Cards: each card gets a page, plus a combined page.
    for stem, text in card_text_by_stem.items():
        page = wrap_page(
            first_h1(text),
            f'<section class="chapter"><article class="card">'
            f"{render_markdown(text)}</article></section>",
            build_toc("cards.html"),
            "cards.html",
        )
        (SITE / f"{stem}.html").write_text(page, encoding="utf-8")

    card_articles = [
        f'<article class="card">{render_markdown(text)}</article>'
        for text in card_text_by_stem.values()
    ]
    cards_body = (
        '<section class="chapter"><h1>Chapter-Recipe Cards</h1>'
        "<p>One-page checklists for each chapter: grab the card when you start "
        "the phase, and keep the "
        '<a href="checklist-tone.html">tone checklist</a> beside your keyboard. '
        "The gathered, print-ready version of everything is on the "
        '<a href="print.html">printable book</a> page.</p>'
        f'<div class="cardgrid">{"".join(card_articles)}</div></section>'
    )
    (SITE / "cards.html").write_text(
        wrap_page("Recipe Cards", cards_body, build_toc("cards.html"), "cards.html"),
        encoding="utf-8",
    )

    # Index: the introduction, plus a clear "begin here" pointer.
    intro = text_by_stem["00-introduction"]
    index_body = (
        f'{render_markdown(intro)}'
        '<p><a href="01-pick-a-bleeding-topic.html">Begin with Chapter 1 &#8594;</a></p>'
    )
    (SITE / "index.html").write_text(
        wrap_page("Start Here", index_body, build_toc("index.html"), "index.html"),
        encoding="utf-8",
    )

    # Print page: every chapter, the checklist, the glossary, the cards —
    # in order, in one file, with print CSS. Browser -> Print -> Save as PDF.
    print_sources = [text_by_stem[s] for s in
                     (p.removesuffix(".md") for p in CHAPTER_FILES)]
    print_sources.append(text_by_stem["checklist-tone"])
    print_sources.append(text_by_stem["glossary"])
    if card_text_by_stem:
        print_sources.append(
            "<h1>Chapter-Recipe Cards</h1>\n\n"
            "<p>The one-page checklists for each chapter, gathered for printing.</p>\n\n"
            + "\n\n".join(card_text_by_stem.values())
        )
    print_body = "\n\n".join(
        f'<section class="chapter">{render_markdown(t)}</section>' for t in print_sources
    )
    (SITE / "print.html").write_text(
        wrap_page("Printable Book", print_body, build_toc("print.html"), "print.html"),
        encoding="utf-8",
    )

    n_pages = len(text_by_stem) + len(card_text_by_stem) + 2
    print(f"built site/: {len(text_by_stem)} chapter/special pages, "
          f"{len(card_text_by_stem)} card pages, cards.html, index.html, print.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
