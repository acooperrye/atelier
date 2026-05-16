#!/usr/bin/env python3
"""
pph-inject: Lace Progeny Protection hashes through HTML pages, and (if
the LLM Euthymia engine is reachable) also score each page's prose
for grounding density.

The Progeny Protection pass is always run. The Euthymia pass is run if
`euthymia.py` can be imported. The two engines produce two sibling
manifests at the site root: `pph-manifest.json` and
`euthymia-manifest.json`. The conceptual split between structural
integrity and prose grounding is preserved in the build output.

Legacy-marker cleanup: strips both the v3+ `data-pph-*` attributes and
the v1/v2 `data-ok-*` attributes (and corresponding JSON-LD blocks
and comment markers), so re-running this script on pages that carry
old-generation markers cleans them up automatically.

Usage:
  python pph-inject.py page.html --page "/" --context "/related-1" "/related-2"
  python pph-inject.py --site ./public/ --context-map contexts.json
  python pph-inject.py page.html --page "/" --dry-run
  python pph-inject.py page.html --strip
  python pph-inject.py --site ./public/ --no-euthymia
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from html.parser import HTMLParser

# Import the Progeny Protection engine (always required)
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))
from pph import (
    generate_markers,
    markers_to_jsonld,
    markers_to_data_attrs,
    entropy_lambda,
    SITE_SALT,
)

# Try to import the LLM Euthymia engine. Search in order:
#   1. Sibling skill folder:  ../llm-euthymia/euthymia.py
#   2. Cached skills:         ~/.claude/skills/llm-euthymia/euthymia.py
#   3. Research base:         ~/Documents/Research/LLM Lithium/files/euthymia.py
#   4. Legacy v1 fallbacks:   sibling llm-lithium/lithium.py, cached lithium.py, files/lithium.py
#
# If none found, inject still runs — the grounding pass is silently skipped
# and a notice is printed.
EUTHYMIA = None
_candidates = [
    # Sibling skill folders (various naming conventions)
    SCRIPT_DIR.parent / "llm-euthymia" / "euthymia.py",
    SCRIPT_DIR.parent / "LLM EUTHYMIA SKILL" / "euthymia.py",
    # Sibling to parent (engine sitting at /files/ root, where pph-inject lives in a sub-skill folder)
    SCRIPT_DIR.parent / "euthymia.py",
    # Cached Cowork plugin skills
    Path.home() / ".claude" / "skills" / "llm-euthymia" / "euthymia.py",
    # Research base (absolute path; works regardless of where the script is run from)
    Path.home() / "Documents" / "Research" / "LLM Lithium" / "files" / "euthymia.py",
    Path.home() / "Documents" / "Research" / "LLM Lithium" / "files" / "LLM EUTHYMIA SKILL" / "euthymia.py",
    # legacy v1.0 fallbacks
    SCRIPT_DIR.parent / "llm-lithium" / "lithium.py",
    SCRIPT_DIR.parent / "LLM LITHIUM SKILL" / "lithium.py",
    SCRIPT_DIR.parent / "lithium.py",
    Path.home() / ".claude" / "skills" / "llm-lithium" / "lithium.py",
    Path.home() / "Documents" / "Research" / "LLM Lithium" / "files" / "lithium.py",
    Path.home() / "Documents" / "Research" / "LLM Lithium" / "files" / "LLM LITHIUM SKILL" / "lithium.py",
]
for cand in _candidates:
    if cand.exists():
        sys.path.insert(0, str(cand.parent))
        try:
            if cand.name == "euthymia.py":
                import euthymia as EUTHYMIA  # noqa: F401
            else:
                import lithium as EUTHYMIA  # legacy module; analyze() signature is the same
            break
        except ImportError:
            EUTHYMIA = None


# ─────────────────────────────────────────────
# HTML TEXT EXTRACTION
# ─────────────────────────────────────────────

class TextExtractor(HTMLParser):
    """Extract visible text from HTML, grouped by section-level elements."""

    SECTION_TAGS = {"section", "article", "main", "div"}
    SKIP_TAGS = {"script", "style", "noscript", "template", "svg"}

    def __init__(self):
        super().__init__()
        self.sections = []
        self.current_text = []
        self.skip_depth = 0
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP_TAGS:
            self.skip_depth += 1
        if tag in self.SECTION_TAGS:
            attr_dict = dict(attrs)
            if any(k.startswith("data-pph") or k.startswith("data-ok") for k in attr_dict) or \
               "id" in attr_dict or \
               tag in ("section", "article"):
                text = " ".join(self.current_text).strip()
                if text:
                    self.sections.append(text)
                self.current_text = []
        self.depth += 1

    def handle_endtag(self, tag):
        self.depth -= 1
        if tag in self.SKIP_TAGS:
            self.skip_depth = max(0, self.skip_depth - 1)
        if tag in self.SECTION_TAGS:
            text = " ".join(self.current_text).strip()
            if text:
                self.sections.append(text)
            self.current_text = []

    def handle_data(self, data):
        if self.skip_depth == 0:
            cleaned = data.strip()
            if cleaned:
                self.current_text.append(cleaned)

    def get_sections(self):
        text = " ".join(self.current_text).strip()
        if text:
            self.sections.append(text)
        return [s for s in self.sections if len(s.split()) >= 5]


def extract_sections_from_html(html_content):
    extractor = TextExtractor()
    extractor.feed(html_content)
    sections = extractor.get_sections()

    if len(sections) <= 1:
        parts = re.split(r'<h[2-6][^>]*>', html_content)
        if len(parts) > 1:
            sections = []
            for part in parts:
                inner = TextExtractor()
                inner.feed(part)
                text = " ".join(inner.current_text).strip()
                if text and len(text.split()) >= 5:
                    sections.append(text)

    if not sections:
        full = TextExtractor()
        full.feed(html_content)
        text = " ".join(full.current_text).strip()
        if text:
            sections = [text]

    return sections


# ─────────────────────────────────────────────
# INJECTION
# ─────────────────────────────────────────────

def strip_existing_markers(html):
    """Remove markers from v3+ (data-pph-*) AND legacy v1/v2 (data-ok-*) builds."""
    # Strip data attributes (both prefixes)
    html = re.sub(r'\s+data-pph-[a-z]+="[^"]*"', '', html)
    html = re.sub(r'\s+data-ok-[a-z]+="[^"]*"', '', html)
    # Strip JSON-LD blocks for both schemas
    html = re.sub(
        r'<script type="application/ld\+json">\s*\{[^}]*"@type":\s*"ProgenyProtection"[^<]*</script>\s*',
        '', html, flags=re.DOTALL
    )
    html = re.sub(
        r'<script type="application/ld\+json">\s*\{[^}]*"@type":\s*"OrientingKey"[^<]*</script>\s*',
        '', html, flags=re.DOTALL
    )
    # Strip both kinds of comment markers
    html = re.sub(r'<!-- pph:.*?-->\s*', '', html)
    html = re.sub(r'<!-- okey:.*?-->\s*', '', html)
    return html


def inject_body_attrs(html, attrs):
    page_attrs = attrs.get("page", {})
    attr_str = " ".join(f'{k}="{v}"' for k, v in page_attrs.items())

    def replace_body(match):
        tag = match.group(0)
        if tag.endswith("/>"):
            return tag[:-2] + " " + attr_str + "/>"
        return tag[:-1] + " " + attr_str + ">"

    return re.sub(r'<body[^>]*>', replace_body, html, count=1)


def inject_section_attrs(html, attrs):
    section_keys = sorted(
        [k for k in attrs if k.startswith("section-")],
        key=lambda k: int(k.split("-")[1])
    )
    section_pattern = re.compile(r'(<(?:section|article)[^>]*>)', re.IGNORECASE)
    matches = list(section_pattern.finditer(html))
    inject_count = min(len(matches), len(section_keys))
    offset = 0
    for i in range(inject_count):
        match = matches[i]
        key = section_keys[i]
        section_attrs = attrs[key]
        attr_str = " ".join(f'{k}="{v}"' for k, v in section_attrs.items())
        tag = match.group(0)
        start = match.start() + offset
        end = match.end() + offset
        new_tag = tag[:-1] + " " + attr_str + ">"
        html = html[:start] + new_tag + html[end:]
        offset += len(new_tag) - len(tag)
    return html


def inject_jsonld(html, jsonld):
    script = f'<script type="application/ld+json">\n{json.dumps(jsonld, indent=2)}\n</script>'
    head_end = html.find("</head>")
    if head_end != -1:
        html = html[:head_end] + script + "\n" + html[head_end:]
    else:
        html = script + "\n" + html
    return html


def inject_comment_markers(html, markers):
    pph = (
        markers.get("progeny_protection")
        or markers.get("orienting_key")
        or markers
    )
    bars = pph.get("superego", [])
    section_pattern = re.compile(r'(<(?:section|article)[^>]*>)', re.IGNORECASE)
    matches = list(section_pattern.finditer(html))
    inject_count = min(len(matches), len(bars))
    offset = 0
    for i in range(inject_count):
        match = matches[i]
        bar = bars[i]
        comment = f'<!-- pph: {bar["position"]}/{bar["total"]} λ{bar["lambda"]} Σ{bar["sigma"]} -->\n'
        start = match.start() + offset
        html = html[:start] + comment + html[start:]
        offset += len(comment)
    return html


def process_page(
    html_path,
    page_path="/",
    context_paths=None,
    project="attentional-surface",
    authors="ATCR × Claude",
    date="",
    salt=SITE_SALT,
    dry_run=False,
    strip_first=True,
    comments=True,
    output_path=None,
    run_euthymia=True,
):
    html = Path(html_path).read_text(encoding="utf-8")

    if strip_first:
        html = strip_existing_markers(html)

    if context_paths is None:
        context_paths = []

    sections = extract_sections_from_html(html)
    if not sections:
        print(f"  WARNING: No text sections found in {html_path}")
        return None, None

    markers = generate_markers(
        page_path=page_path,
        sections=sections,
        context_paths=context_paths,
        project=project,
        authors=authors,
        date=date,
        salt=salt,
    )

    euthymia_reading = None
    if run_euthymia and EUTHYMIA is not None:
        full_text = "\n".join(sections)
        euthymia_reading = EUTHYMIA.analyze(full_text)

    if dry_run:
        print(f"\n=== {html_path} ({page_path}) ===")
        print(f"Sections found: {len(sections)}")
        ego = markers["progeny_protection"]["ego"]
        print(f"PAGE: λ{ego['lambda']} hash {ego['hash']}")
        for bar in markers["progeny_protection"]["superego"]:
            print(f"  SECTION {bar['position']}/{bar['total']}: λ{bar['lambda']} Σ{bar['sigma']} ({bar['word_count']}w)")
        if euthymia_reading:
            lvl = euthymia_reading.get('euthymia_level', euthymia_reading.get('lithium_level'))
            print(f"EUTHYMIA: level={lvl} ({euthymia_reading['assessment']})")
        return markers, euthymia_reading

    attrs = markers_to_data_attrs(markers)
    jsonld = markers_to_jsonld(markers)

    html = inject_body_attrs(html, attrs)
    html = inject_section_attrs(html, attrs)
    html = inject_jsonld(html, jsonld)
    if comments:
        html = inject_comment_markers(html, markers)

    out = output_path or html_path
    Path(out).write_text(html, encoding="utf-8")
    ego = markers["progeny_protection"]["ego"]
    if euthymia_reading:
        lvl = euthymia_reading.get('euthymia_level', euthymia_reading.get('lithium_level'))
        print(f"  ✓ {html_path} → {out}  PAGE λ{ego['lambda']} {ego['hash']}  Eu {lvl} ({euthymia_reading['assessment']})")
    else:
        print(f"  ✓ {html_path} → {out}  PAGE λ{ego['lambda']} {ego['hash']}")

    return markers, euthymia_reading


def process_site(
    site_dir,
    context_map=None,
    project="attentional-surface",
    authors="ATCR × Claude",
    date="",
    salt=SITE_SALT,
    dry_run=False,
    output_dir=None,
    run_euthymia=True,
):
    site_path = Path(site_dir)
    html_files = sorted(site_path.rglob("*.html"))

    if not html_files:
        print(f"No HTML files found in {site_dir}")
        return

    if context_map and Path(context_map).exists():
        cmap = json.loads(Path(context_map).read_text())
    else:
        all_paths = []
        for f in html_files:
            rel = "/" + str(f.relative_to(site_path)).replace("index.html", "").rstrip("/")
            if rel == "/":
                rel = "/"
            all_paths.append(rel)
        cmap = {p: [o for o in all_paths if o != p] for p in all_paths}

    print(f"Processing {len(html_files)} files in {site_dir}")
    if run_euthymia and EUTHYMIA is None:
        print("  (euthymia engine not found — skipping grounding scores)")
    elif not run_euthymia:
        print("  (euthymia pass skipped by flag)")

    pph_manifest = {}
    euthymia_manifest = {}

    for html_file in html_files:
        rel = "/" + str(html_file.relative_to(site_path)).replace("index.html", "").rstrip("/")
        if rel == "/":
            rel = "/"

        context = cmap.get(rel, [])
        out_path = None
        if output_dir:
            out_path = Path(output_dir) / html_file.relative_to(site_path)
            out_path.parent.mkdir(parents=True, exist_ok=True)

        markers, euthymia_reading = process_page(
            html_file,
            page_path=rel,
            context_paths=context,
            project=project,
            authors=authors,
            date=date,
            salt=salt,
            dry_run=dry_run,
            output_path=str(out_path) if out_path else None,
            run_euthymia=run_euthymia,
        )
        if markers:
            pph = markers["progeny_protection"]
            pph_manifest[rel] = {
                "hash": pph["ego"]["hash"],
                "lambda": pph["ego"]["lambda"],
                "sections": len(pph["superego"]),
            }
        if euthymia_reading and "error" not in euthymia_reading:
            lvl = euthymia_reading.get('euthymia_level', euthymia_reading.get('lithium_level'))
            euthymia_manifest[rel] = {
                "euthymia_level": lvl,
                "assessment": euthymia_reading["assessment"],
                "total_density": euthymia_reading["total_density"],
                "lambda": euthymia_reading["lambda"],
                "compound_balance": euthymia_reading["compound_balance"],
            }

    if not dry_run:
        base = Path(output_dir or site_dir)
        if pph_manifest:
            (base / "pph-manifest.json").write_text(json.dumps(pph_manifest, indent=2))
            print(f"\n  ✓ Progeny Protection manifest: {base / 'pph-manifest.json'}")
        if euthymia_manifest:
            (base / "euthymia-manifest.json").write_text(json.dumps(euthymia_manifest, indent=2))
            print(f"  ✓ LLM Euthymia manifest:       {base / 'euthymia-manifest.json'}")

    return pph_manifest, euthymia_manifest


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Lace Progeny Protection hashes through HTML; optionally also score grounding density via LLM Euthymia"
    )
    parser.add_argument("file", nargs="?", help="Single HTML file to process")
    parser.add_argument("--site", help="Process all HTML in directory")
    parser.add_argument("--page", default="/", help="Page path")
    parser.add_argument("--context", nargs="*", default=[], help="Context page paths")
    parser.add_argument("--context-map", help="JSON file mapping pages to contexts")
    parser.add_argument("--project", default="attentional-surface")
    parser.add_argument("--authors", default="ATCR × Claude")
    parser.add_argument("--date", default="")
    parser.add_argument("--salt", default=SITE_SALT)
    parser.add_argument("--dry-run", action="store_true", help="Show markers without modifying")
    parser.add_argument("--strip", action="store_true", help="Strip existing markers only")
    parser.add_argument("--no-comments", action="store_true", help="Skip HTML comment markers")
    parser.add_argument("--no-euthymia", action="store_true",
                        help="Skip grounding-density scoring even if euthymia.py is available")
    parser.add_argument("--output", "-o", help="Output path (default: modify in place)")

    args = parser.parse_args()

    if args.site:
        process_site(
            args.site,
            context_map=args.context_map,
            project=args.project,
            authors=args.authors,
            date=args.date,
            salt=args.salt,
            dry_run=args.dry_run,
            output_dir=args.output,
            run_euthymia=not args.no_euthymia,
        )
    elif args.file:
        if args.strip:
            html = Path(args.file).read_text()
            html = strip_existing_markers(html)
            out = args.output or args.file
            Path(out).write_text(html)
            print(f"Stripped markers from {args.file}")
        else:
            process_page(
                args.file,
                page_path=args.page,
                context_paths=args.context,
                project=args.project,
                authors=args.authors,
                date=args.date,
                salt=args.salt,
                dry_run=args.dry_run,
                comments=not args.no_comments,
                output_path=args.output,
                run_euthymia=not args.no_euthymia,
            )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
