"""Parser for the content files in src/content/.

The files keep the approved copy exactly as supplied, in a small line-based format:

    # Page title
    ~ Tagline (the italic line under a title or section heading)
    ## Section heading
    ### Sub-heading
    - list item            (**Name** — description for service lists)
    -> Button or link label →
    Plain lines are paragraphs. **bold**, *italic*, and " \\\\ " for a line break.
"""
import html
import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Block:
    kind: str                      # p | ul | cta | h3 | note
    text: str = ""
    items: list = field(default_factory=list)


@dataclass
class Section:
    heading: str
    tagline: str = None
    blocks: list = field(default_factory=list)


@dataclass
class Doc:
    title: str
    tagline: str = None
    intro: list = field(default_factory=list)
    sections: list = field(default_factory=list)

    def section(self, heading):
        for s in self.sections:
            if s.heading == heading:
                return s
        raise KeyError(f"{self.title}: no section {heading!r}")

    def has(self, heading):
        return any(s.heading == heading for s in self.sections)


def parse(path):
    doc = None
    cur_blocks = None
    last = None            # what the previous non-blank line was: 'title' | 'section' | 'h3' | 'other'
    current_section = None
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if not line:
            if cur_blocks and cur_blocks[-1].kind == "ul":
                cur_blocks.append(Block("break"))
            continue
        if line.startswith("# "):
            doc = Doc(title=line[2:].strip())
            cur_blocks = doc.intro
            last = "title"
            continue
        if line.startswith("## "):
            current_section = Section(heading=line[3:].strip())
            doc.sections.append(current_section)
            cur_blocks = current_section.blocks
            last = "section"
            continue
        if line.startswith("### "):
            cur_blocks.append(Block("h3", line[4:].strip()))
            last = "h3"
            continue
        if line.startswith("~ "):
            text = line[2:].strip()
            if last == "title" and doc.tagline is None and not doc.intro:
                doc.tagline = text
            elif last == "section" and current_section.tagline is None and not current_section.blocks:
                current_section.tagline = text
            else:
                cur_blocks.append(Block("note", text))     # an italic line that is not a tagline
            last = "other"
            continue
        if line.startswith("-> "):
            cur_blocks.append(Block("cta", line[3:].strip()))
            last = "other"
            continue
        if line.startswith("- "):
            item = line[2:].strip()
            if cur_blocks and cur_blocks[-1].kind == "ul":
                cur_blocks[-1].items.append(item)
            else:
                cur_blocks.append(Block("ul", items=[item]))
            last = "other"
            continue
        cur_blocks.append(Block("p", line.strip()))
        last = "other"
    # Drop blank-line markers. Two lists separated only by a blank line are one list
    # that a page break split in the supplied PDF, so they are joined again.
    for blocks in [doc.intro] + [s.blocks for s in doc.sections]:
        merged = []
        for b in blocks:
            if b.kind == "break":
                continue
            if b.kind == "ul" and merged and merged[-1].kind == "ul":
                merged[-1].items.extend(b.items)
                continue
            merged.append(b)
        blocks[:] = merged
    return doc


# ---------------------------------------------------------------- inline rendering

_BOLD = re.compile(r"\*\*(.+?)\*\*")
_ITAL = re.compile(r"(?<![\*\w])\*(?!\*)(.+?)(?<!\*)\*(?![\*\w])")


def inline(text, links=None):
    """Escape and render **bold**, *italic* and line breaks.

    `links` maps an exact phrase to an HTML snippet that replaces it (used to turn
    phrases such as "Privacy Policy" or an email address into links without
    changing the wording).
    """
    out = html.escape(text, quote=False)
    out = _BOLD.sub(r"<strong>\1</strong>", out)
    out = _ITAL.sub(r"<em>\1</em>", out)
    out = out.replace(" \\\\ ", "<br>")
    out = nowrap(out)
    if links:
        for phrase, snippet in links.items():
            esc = html.escape(phrase, quote=False)
            if esc not in out:
                raise ValueError(f"link phrase not found: {phrase!r} in {text!r}")
            out = out.replace(esc, snippet, 1)
    return out


# Words that must not break at their hyphen (e.g. "Al-" / "Iskan").
NOWRAP = ("Al-Iskan",)


def nowrap(html_text):
    for w in NOWRAP:
        html_text = html_text.replace(w, f'<span class="nowrap">{w}</span>')
    return html_text


def plain(text):
    """Text without markup (for alt text, titles and comparisons)."""
    t = text.replace(" \\\\ ", " ")
    t = _BOLD.sub(r"\1", t)
    t = _ITAL.sub(r"\1", t)
    return t


def strip_arrow(label):
    return re.sub(r"\s*→\s*$", "", label).strip()


def split_lead(item):
    """'**Name** — description' -> ('Name', 'description'); otherwise (None, item)."""
    m = re.match(r"^\*\*(.+?)\*\*\s+—\s+(.*)$", item)
    if m:
        return m.group(1), m.group(2)
    return None, item


def split_bold_lead(par):
    """'**Lead.** rest' -> ('Lead.', 'rest'); otherwise (None, par)."""
    m = re.match(r"^\*\*(.+?)\*\*\s+(.*)$", par)
    if m:
        return m.group(1), m.group(2)
    return None, par
