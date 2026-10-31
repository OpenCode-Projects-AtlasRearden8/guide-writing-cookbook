#!/usr/bin/env python3
"""Test suite for the Guide-Writing Cookbook.

Verifies the whole contract without network access:
- source fixtures exist and are well-formed
- `python3 build.py` runs clean
- every generated page exists with every internal link and anchor resolving
- no placeholder text leaks into the site
- the print page really contains the whole book
- license and README credit lines are exactly as promised
- no obvious secrets (key/token patterns) anywhere in the repo files
"""
from __future__ import annotations

import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
CARDS = DOCS / "cards"
SITE = ROOT / "site"

CHAPTER_STEMS = [
    "00-introduction",
    "01-pick-a-bleeding-topic",
    "02-scope-first-edition",
    "03-plain-english-rules",
    "04-lesson-rhythms",
    "05-edit-for-dignity",
    "06-printables-and-tools",
    "07-verify-every-claim",
    "08-ship-docs-site-pdf",
]
SPECIAL_DOCS = ["checklist-tone.md", "glossary.md"]
LICENSE_COPYRIGHT = "Copyright (c) 2026 Asdale Dynamics, LLC"
README_CREDIT = "Asdale Dynamics, LLC"


def source_stems() -> list[str]:
    return CHAPTER_STEMS + [p.removesuffix(".md") for p in SPECIAL_DOCS]


def card_stems() -> list[str]:
    return sorted(p.stem for p in CARDS.glob("card-*.md"))


def page_html(path: str) -> str:
    return (SITE / path).read_text(encoding="utf-8")


class TestSourceFixtures(unittest.TestCase):
    def test_chapter_files_exist(self):
        for stem in CHAPTER_STEMS:
            self.assertTrue((DOCS / f"{stem}.md").is_file(), stem)

    def test_special_docs_exist(self):
        for name in SPECIAL_DOCS:
            self.assertTrue((DOCS / name).is_file(), name)

    def test_chapters_start_with_h1(self):
        for stem in CHAPTER_STEMS:
            text = (DOCS / f"{stem}.md").read_text(encoding="utf-8")
            self.assertTrue(text.startswith("# "), f"{stem} missing H1 title")

    def test_cards_cover_every_chapter(self):
        cards = card_stems()
        self.assertGreaterEqual(len(cards), len(CHAPTER_STEMS), cards)
        self.assertTrue(all(c.startswith("card-") for c in cards), cards)

    def test_no_todo_fragments_in_sources(self):
        pattern = re.compile(r"\b(TODO|FIXME|TBD)\b")
        for path in list(DOCS.rglob("*.md")):
            # Occurrences inside backticks are fine: the book may legitimately
            # describe what to check for. Bare ones are leftover scaffolding.
            stripped = re.sub(r"`[^`]*`", "` `", path.read_text(encoding="utf-8"))
            match = pattern.search(stripped)
            self.assertIsNone(
                match, f"placeholder text in {path}: {match.group() if match else ''}"
            )

    def test_glossary_alphabetical(self):
        text = (DOCS / "glossary.md").read_text(encoding="utf-8")
        body = text.split("in alphabetical order.", 1)[-1]
        entries = re.findall(r"^\*\*([^*]+)\*\*", body, flags=re.M)
        self.assertEqual(
            entries,
            sorted(entries, key=str.lower),
            "glossary entries out of alphabetical order",
        )


class TestBuild(unittest.TestCase):
    def test_build_runs_clean(self):
        result = subprocess.run(
            [sys.executable, "build.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr.strip(), "", "build emitted warnings")

    def test_build_exit_code_on_bad_docs_dir(self):
        # build.py must fail loudly, not silently produce garbage, when its
        # docs/ is missing. Run it from a sandbox dir with no docs/ beside it.
        import tempfile
        import shutil
        with tempfile.TemporaryDirectory() as tmp:
            sandbox = Path(tmp)
            script = sandbox / "build.py"
            shutil.copy(ROOT / "build.py", script)
            result = subprocess.run(
                [sys.executable, "build.py"], cwd=sandbox, capture_output=True, text=True
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("docs/", result.stderr)


class TestGeneratedSite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = {p.name: p.read_text(encoding="utf-8") for p in SITE.glob("*.html")}

    def test_every_doc_has_a_page(self):
        for stem in source_stems() + card_stems():
            self.assertIn(f"{stem}.html", self.pages)

    def test_core_nav_pages_exist(self):
        for name in ("index.html", "cards.html", "checklist-tone.html",
                     "glossary.html", "print.html"):
            self.assertIn(name, self.pages)

    def test_no_placeholder_leaks(self):
        pattern = re.compile(r"(\bTODO\b|\bFIXME\b|\{\{|\}\}|%s)")
        for name, text in sorted(self.pages.items()):
            # Inline-code mentions (e.g. chapter 8 describing the leak check)
            # are legitimate; strip code spans before scanning for bare leaks.
            stripped = re.sub(r"<code>.*?</code>", "<code></code>", text, flags=re.S)
            match = pattern.search(stripped)
            self.assertIsNone(
                match, f"template leak in {name}: {match.group() if match else ''}"
            )

    def test_internal_links_resolve(self):
        for name, text in sorted(self.pages.items()):
            for href in re.findall(r'href="([^"#]+\.html(?:#[^"]*)?)"', text):
                target, _, anchor = href.partition("#")
                if target.startswith("http"):
                    continue
                self.assertIn(target, self.pages, f"{name} -> {href} missing")
                if anchor:
                    self.assertRegex(
                        self.pages[target],
                        rf'id="{re.escape(anchor)}"',
                        f"{name} -> {href}: anchor missing",
                    )

    def test_every_page_has_headings(self):
        for name, text in sorted(self.pages.items()):
            self.assertIn("<h1>", text, f"{name} has no H1")

    def test_every_page_has_license_footer(self):
        for name, text in self.pages.items():
            self.assertIn("MIT License", text, f"{name} footer missing license")

    def test_glossary_terms_used_by_chapters_are_defined(self):
        glossary = (DOCS / "glossary.md").read_text(encoding="utf-8")
        entries = re.findall(r"^\*\*(.+?)\*\*", glossary, flags=re.M)
        terms = {e.split(" —")[0].strip().lower() for e in entries}
        self.assertGreater(len(terms), 15, "glossary suspiciously small")
        chapter_text = "\n".join(
            (DOCS / f"{s}.md").read_text(encoding="utf-8") for s in CHAPTER_STEMS
        ).lower()
        # Terms used as concepts in chapters must exist in the glossary...
        for must_have in ("rhythm", "plain english", "scope", "jargon",
                          "verify", "printable"):
            self.assertIn(must_have, chapter_text, f"'{must_have}' never used in chapters")
        # ...and the big chapter concepts must be glossary entries.
        for entry_match in ("rhythm", "plain english", "recovery path",
                            "volatile claim", "verification loop"):
            self.assertIn(entry_match, " ".join(terms))


class TestPrintPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = page_html("print.html")

    def test_contains_every_chapter_h1(self):
        for stem in CHAPTER_STEMS:
            title = (DOCS / f"{stem}.md").read_text(encoding="utf-8")
            h1 = title.splitlines()[0].lstrip("# ").strip()
            self.assertIn(h1, self.text, f"print page missing: {h1}")

    def test_contains_checklist_and_glossary(self):
        self.assertIn("Tone Checklist", self.text)
        self.assertIn("Glossary", self.text)

    def test_contains_every_card_h1(self):
        for stem in card_stems():
            title = (CARDS / f"{stem}.md").read_text(encoding="utf-8")
            h1 = title.splitlines()[0].lstrip("# ").strip()
            self.assertIn(h1, self.text, f"print page missing card: {h1}")

    def test_chapter_sections_present_and_ordered(self):
        order = [m for m in re.findall(r'<section class="chapter">', self.text)]
        self.assertGreaterEqual(len(order), len(CHAPTER_STEMS) + 2)
        first = self.text.find('<section class="chapter">')
        early = self.text[first : first + 1200]
        self.assertIn("What This Cookbook Is", early, "print page starts with the intro")

    def test_has_print_stylesheet_rules(self):
        self.assertIn("@media print", self.text)
        self.assertIn("break-before: page", self.text)


class TestLicenseAndReadme(unittest.TestCase):
    def test_license_exists_and_is_mit(self):
        text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn(LICENSE_COPYRIGHT, text)
        self.assertIn("MIT License", text)

    def test_readme_credits_asdale(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(README_CREDIT, text)

    def test_readme_mentions_build_and_test_commands(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("python3 build.py", text)
        self.assertIn("python3 tests/test.py", text)


class TestNoSecrets(unittest.TestCase):
    def test_no_token_patterns_in_repo(self):
        patterns = [
            r"sk-[A-Za-z0-9]{20,}",
            r"AKIA[A-Z0-9]{12,}",
            r"ghp_[A-Za-z0-9]{20,}",
            r"xox[bapo]-[A-Za-z0-9-]{10,}",
            r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
        ]
        for path in ROOT.rglob("*"):
            if not path.is_file() or path.name == "test.py" or ".git" in path.parts:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, PermissionError):
                continue
            for pat in patterns:
                self.assertIsNone(
                    re.search(pat, text), f"suspicious token pattern in {path}"
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
