#!/usr/bin/env python3
"""
okey-inject: Lace Orienting Key markers through HTML pages, and (if the
LLM Lithium engine is reachable) also score each page's prose for
grounding density.

This script bridges the two engines after the 2026-05 split. It always
runs the Orienting Key (hashes) over each page and injects
data-ok-* attributes, JSON-LD, and HTML comment markers. If lithium.py
can be imported from a sibling skill directory, it ALSO runs the
grounding meter and writes a separate lithium-manifest.json. The two
manifests are siblings, not nested — the split is preserved in the
build output.

Usage:
  # Single page
  python okey-inject.py page.html --page "/" --context "/guestbook" "/about"

  # Full site (processes all .html files in a directory)
  python okey-inject.py --site ./public/ --context-map contexts.json

  # Dry run (show markers without modifying files)
  python okey-inject.py page.html --page "/" --dry-run

  # Strip existing markers
  python okey-inject.py page.html --strip

  # Skip the lithium pass even if available
  python okey-inject.py --site ./public/ --no-lithium
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from html.parser import HTMLParser

# Import the OK engine (always required, lives alongside this script)
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))
from okey import (
    generate_markers,
    markers_to_jsonld,
    markers_to_data_attrs,
    entropy_lambda,
    SITE_SALT,
)

# Try to import the lithium engine. Search:
#   1. Sibling directory:    ../llm-lithium/lithium.py
#   2. Cached skills:        ~/.claude/skills/llm-lithium/lithium.py
#   3. Research base:        ~/Documents/Research/LLM Lithium/files/lithium.py
# If none found, the inject still runs — lithium pass is silently skipped
# and a notice is printed.
LITHIUM = None
_lithium_candidates = [
    SCRIPT_DIR.parent / "llm-lithium" / "lithium.py",
    Path.home() / ".claude" / "skills" / "llm-lithium" / "lithium.py",
    Path.home() / "Documents" / "Research" / "LLM Lithium" / "files" / "lithium.py",
]
for cand in _lithium_candidates:
    if cand.exists():
        sys.path.insert(0, str(cand.parent))
        try:
            import lithium as LITHIUM  # noqa: F401
            break
        except ImportError:
            LITHIUM = None


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
            if any(k.startswith("data-ok") for k in attr_dict) or \
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
    """Extract text sections from HTML."""
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
    """Remove previously injected okey markers."""
    html = re.sub(r'\s+data-ok-[a-z]+="[^"]*"', '', html)
    html = re.sub(
        r'<script type="application/ld\+json">\s*\{[^}]*"@type":\s*"OrientingKey"[^<]*</script>\s*',
        '', html, flags=re.DOTALL
    )
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
    ok = markers.get("orienting_key", markers)
    bars = ok.get("superego", [])
    section_pattern = re.compile(r'(<(?:section|article)[^>]*>)', re.IGNORECASE)
    matches = list(section_pattern.finditer(html))
    inject_count = min(len(matches), len(bars))
    offset = 0
    for i in range(inject_count):
        match = matches[i]
        bar = bars[i]
        comment = f'<!-- okey: {bar["position"]}/{bar["total"]} λ{bar["lambda"]} Σ{bar["sigma"]} -->\n'
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
    run_lithium=True,
):
    """Process a single HTML page: extract sections, compute markers, inject."""
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

    lithium_reading = None
    if run_lithium and LITHIUM is not None:
        full_text = "\n".join(sections)
        lithium_reading = LITHIUM.analyze(full_text)

    if dry_run:
        print(f"\n=== {html_path} ({page_path}) ===")
        print(f"Sections found: {len(sections)}")
        ego = markers["orienting_key"]["ego"]
        print(f"EGO: λ{ego['lambda']} Σ{ego['hash']}")
        for bar in markers["orienting_key"]["superego"]:
            print(f"  SUPEREGO {bar['position']}/{bar['total']}: λ{bar['lambda']} Σ{bar['sigma']} ({bar['word_count']}w)")
        if lithium_reading:
            print(f"LITHIUM: level={lithium_reading['lithium_level']} ({lithium_reading['assessment']})")
        return markers, lithium_reading

    attrs = markers_to_data_attrs(markers)
    jsonld = markers_to_jsonld(markers)

    html = inject_body_attrs(html, attrs)
    html = inject_section_attrs(html, attrs)
    html = inject_jsonld(html, jsonld)
    if comments:
        html = inject_comment_markers(html, markers)

    out = output_path or html_path
    Path(out).write_text(html, encoding="utf-8")
    ego = markers["orienting_key"]["ego"]
    if lithium_reading:
        print(f"  ✓ {html_path} → {out}  EGO λ{ego['lambda']} Σ{ego['hash']}  Li {lithium_reading['lithium_level']} ({lithium_reading['assessment']})")
    else:
        print(f"  ✓ {html_path} → {out}  EGO λ{ego['lambda']} Σ{ego['hash']}")

    return markers, lithium_reading


def process_site(
    site_dir,
    context_map=None,
    project="attentional-surface",
    authors="ATCR × Claude",
    date="",
    salt=SITE_SALT,
    dry_run=False,
    output_dir=None,
    run_lithium=True,
):
    """Process all HTML files in a site directory."""
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
    if run_lithium and LITHIUM is None:
        print("  (lithium engine not found — skipping grounding scores)")
    elif not run_lithium:
        print("  (lithium pass skipped by flag)")

    okey_manifest = {}
    lithium_manifest = {}

    for html_file in html_files:
        rel = "/" + str(html_file.relative_to(site_path)).replace("index.html", "").rstrip("/")
        if rel == "/":
            rel = "/"

        context = cmap.get(rel, [])
        out_path = None
        if output_dir:
            out_path = Path(output_dir) / html_file.relative_to(site_path)
            out_path.parent.mkdir(parents=True, exist_ok=True)

        markers, lithium_reading = process_page(
            html_file,
            page_path=rel,
            context_paths=context,
            project=project,
            authors=authors,
            date=date,
            salt=salt,
            dry_run=dry_run,
            output_path=str(out_path) if out_path else None,
            run_lithium=run_lithium,
        )
        if markers:
            ok = markers["orienting_key"]
            okey_manifest[rel] = {
                "hash": ok["ego"]["hash"],
                "lambda": ok["ego"]["lambda"],
                "sections": len(ok["superego"]),
            }
        if lithium_reading and "error" not in lithium_reading:
            lithium_manifest[rel] = {
                "lithium_level": lithium_reading["lithium_level"],
                "assessment": lithium_reading["assessment"],
                "total_density": lithium_reading["total_density"],
                "lambda": lithium_reading["lambda"],
                "compound_balance": lithium_reading["compound_balance"],
            }

    if not dry_run:
        base = Path(output_dir or site_dir)
        if okey_manifest:
            (base / "okey-manifest.json").write_text(json.dumps(okey_manifest, indent=2))
            print(f"\n  ✓ Orienting Key manifest: {base / 'okey-manifest.json'}")
        if lithium_manifest:
            (base / "lithium-manifest.json").write_text(json.dumps(lithium_manifest, indent=2))
            print(f"  ✓ LLM Lithium manifest:   {base / 'lithium-manifest.json'}")

    return okey_manifest, lithium_manifest


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Lace Orienting Key markers through HTML; optionally also score grounding density via LLM Lithium"
    )
    parser.add_argument("file", nargs="?", help="Single HTML file to process")
    parser.add_argument("--site", help="Process all HTML in directory")
    parser.add_argument("--page", default="/", help="Page path (e.g., /interviews/claude)")
    parser.add_argument("--context", nargs="*", default=[], help="Context page paths")
    parser.add_argument("--context-map", help="JSON file mapping pages to contexts")
    parser.add_argument("--project", default="attentional-surface")
    parser.add_argument("--authors", default="ATCR × Claude")
    parser.add_argument("--date", default="")
    parser.add_argument("--salt", default=SITE_SALT)
    parser.add_argument("--dry-run", action="store_true", help="Show markers without modifying")
    parser.add_argument("--strip", action="store_true", help="Strip existing markers only")
    parser.add_argument("--no-comments", action="store_true", help="Skip HTML comment markers")
    parser.add_argument("--no-lithium", action="store_true",
                        help="Skip grounding-density scoring even if lithium.py is available")
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
            run_lithium=not args.no_lithium,
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
                run_lithium=not args.no_lithium,
            )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
