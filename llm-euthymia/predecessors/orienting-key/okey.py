#!/usr/bin/env python3
"""
Orienting Key Engine (okey)
===========================
A structural integrity system for content designed to be processed by
language models or other automated readers. Two components:

  EGO      - Header: page-level self-orientation (where am I in the site?)
  SUPEREGO - Scroll bar: relational position within structure (where am I
             in this page?)

Hashes are SHA-256 truncated to 4 hex characters. Not cryptographically
secure — recalculable, format-agnostic, recoverable by any reader that
can hash text.

Note on scope (2026-05): the third component (ID / inline lithium /
grounding compound analysis) lives in the LLM Lithium engine. The
grounding meter is part of the LLM Lithium framework's claim about how
language model substrates should be evaluated; the integrity hashes are
a structural property of documents. The two were originally bundled
under one name. They have been split.

Usage:
  python okey.py generate  --sections file1.txt file2.txt ...
  python okey.py generate  --document doc.txt --split "---"
  python okey.py verify    --sections file1.txt file2.txt ... --markers markers.json
  python okey.py embed     --markers markers.json --format jsonld
  python okey.py embed     --markers markers.json --format attrs

All commands also work as library imports.
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────

HASH_LENGTH = 4          # hex chars (2 bytes, 65536 possible values)
SITE_SALT = "atcooper"   # default site salt, override per-project
VERSION = "2.0"          # bumped at 2026-05 split


# ─────────────────────────────────────────────
# CORE MATH
# ─────────────────────────────────────────────

def _clean(text: str) -> str:
    """Normalize text for hashing: collapse whitespace, lowercase."""
    return re.sub(r'\s+', ' ', text.strip().lower())


def _hash(text: str, length: int = HASH_LENGTH) -> str:
    """SHA-256 of text, truncated to `length` hex characters."""
    h = hashlib.sha256(_clean(text).encode('utf-8')).hexdigest()
    return h[:length]


def _words(text: str) -> list:
    """Extract word tokens from text."""
    return re.findall(r"[a-zA-Z']+", text.lower())


def entropy_lambda(text: str) -> float:
    """
    Type-token ratio (TTR) as entropy measure.
    λ = unique_words / total_words, rounded to 2 decimal places.
    Range: 0.0 (all identical) to 1.0 (all unique).
    Used here only as a structural descriptor of a page's lexical
    bandwidth — it does NOT feed any scoring. (Scoring moved to lithium.py.)
    """
    words = _words(text)
    if not words:
        return 0.0
    return round(len(set(words)) / len(words), 2)


def binding_hash(
    section_text: str,
    first_section_text: str,
    last_section_text: str,
    position: int,
    salt: str = SITE_SALT
) -> str:
    """
    Compute integrity hash that binds a section to the whole structure.
    Hash of: section_content + hash(first) + hash(last) + position + salt.
    If you don't have first and last sections, you can't verify — the
    middle fragment cannot self-verify without the edges. ("Prion fold.")
    """
    payload = (
        _clean(section_text)
        + _hash(first_section_text)
        + _hash(last_section_text)
        + str(position)
        + salt
    )
    return _hash(payload)


def page_hash(page_content: str, context_paths: list, salt: str = SITE_SALT) -> str:
    """
    EGO hash: binds page content to its declared context.
    Hash of: page_content + sorted_context_paths + salt.
    Changes if content changes OR if context declaration changes.
    """
    context_str = "|".join(sorted(context_paths))
    payload = _clean(page_content) + context_str + salt
    return _hash(payload)


# ─────────────────────────────────────────────
# EGO - HEADER
# ─────────────────────────────────────────────

def generate_ego(
    page_path: str,
    page_content: str,
    context_paths: list,
    project: str = "attentional-surface",
    authors: str = "ATCR × Claude",
    date: str = "",
    version: str = VERSION,
    salt: str = SITE_SALT,
) -> dict:
    """
    Generate EGO header: page-level self-orientation.

    Returns dict with all header fields + computed hash.
    """
    ph = page_hash(page_content, context_paths, salt)
    lam = entropy_lambda(page_content)

    return {
        "component": "ego",
        "project": project,
        "authors": authors,
        "date": date,
        "version": version,
        "page": page_path,
        "context": context_paths,
        "lambda": lam,
        "hash": ph,
    }


# ─────────────────────────────────────────────
# SUPEREGO - SCROLL BAR
# ─────────────────────────────────────────────

def generate_superego(sections: list, salt: str = SITE_SALT) -> list:
    """
    Generate SUPEREGO scroll bars for a list of section texts.

    Each section gets:
      - position (n/N)
      - λ (section entropy descriptor)
      - Σ (binding hash: ties this section to first + last + position)
      - word_count

    Returns list of dicts, one per section.
    """
    n_total = len(sections)
    if n_total == 0:
        return []

    first = sections[0]
    last = sections[-1]
    bars = []

    for i, section in enumerate(sections):
        pos = i + 1
        lam = entropy_lambda(section)
        sigma = binding_hash(section, first, last, pos, salt)
        wc = len(_words(section))

        bars.append({
            "component": "superego",
            "position": pos,
            "total": n_total,
            "lambda": lam,
            "sigma": sigma,
            "word_count": wc,
        })

    return bars


# ─────────────────────────────────────────────
# FULL GENERATION
# ─────────────────────────────────────────────

def generate_markers(
    page_path: str,
    sections: list,
    context_paths: list = None,
    project: str = "attentional-surface",
    authors: str = "ATCR × Claude",
    date: str = "",
    salt: str = SITE_SALT,
) -> dict:
    """
    Generate complete Orienting Key for a page.
    Returns EGO header + SUPEREGO bars for each section.

    No ID / grounding analysis — that lives in lithium.py now.
    """
    if context_paths is None:
        context_paths = []

    full_content = "\n".join(sections)

    ego = generate_ego(
        page_path, full_content, context_paths,
        project, authors, date,
        salt=salt,
    )
    superego = generate_superego(sections, salt)

    return {
        "orienting_key": {
            "ego": ego,
            "superego": superego,
        }
    }


# ─────────────────────────────────────────────
# VERIFICATION
# ─────────────────────────────────────────────

def verify_markers(sections: list, markers: dict, salt: str = SITE_SALT) -> dict:
    """
    Verify an Orienting Key against actual content.
    Returns pass/fail for each component with details.
    """
    results = {"ego": {}, "superego": [], "intact": True}
    ok = markers.get("orienting_key", markers)

    # Verify EGO
    ego = ok.get("ego", {})
    full_content = "\n".join(sections)
    expected_lambda = entropy_lambda(full_content)
    expected_hash = page_hash(full_content, ego.get("context", []), salt)

    results["ego"]["lambda_match"] = ego.get("lambda") == expected_lambda
    results["ego"]["hash_match"] = ego.get("hash") == expected_hash
    results["ego"]["expected_lambda"] = expected_lambda
    results["ego"]["expected_hash"] = expected_hash

    if not results["ego"]["lambda_match"] or not results["ego"]["hash_match"]:
        results["intact"] = False

    # Verify SUPEREGO
    expected_bars = generate_superego(sections, salt)
    for i, (expected, actual) in enumerate(
        zip(expected_bars, ok.get("superego", []))
    ):
        section_ok = (
            expected["lambda"] == actual.get("lambda")
            and expected["sigma"] == actual.get("sigma")
            and expected["word_count"] == actual.get("word_count")
        )
        results["superego"].append({
            "section": i + 1,
            "valid": section_ok,
            "expected_sigma": expected["sigma"],
            "got_sigma": actual.get("sigma"),
        })
        if not section_ok:
            results["intact"] = False

    return results


# ─────────────────────────────────────────────
# HTML EMBEDDING
# ─────────────────────────────────────────────

def markers_to_data_attrs(markers: dict) -> dict:
    """
    Convert markers to HTML data-attribute format.
    Returns dict of {element_selector: {attr: value}} mappings.
    """
    ok = markers.get("orienting_key", markers)
    ego = ok["ego"]
    attrs = {}

    # Page-level attrs (for <body>)
    attrs["page"] = {
        "data-ok-project": ego["project"],
        "data-ok-page": ego["page"],
        "data-ok-lambda": str(ego["lambda"]),
        "data-ok-hash": ego["hash"],
        "data-ok-context": "|".join(ego["context"]),
        "data-ok-version": ego.get("version", VERSION),
    }

    # Section-level attrs
    for bar in ok["superego"]:
        key = f"section-{bar['position']}"
        attrs[key] = {
            "data-ok-pos": f"{bar['position']}/{bar['total']}",
            "data-ok-lambda": str(bar["lambda"]),
            "data-ok-sigma": bar["sigma"],
            "data-ok-wc": str(bar["word_count"]),
        }

    return attrs


def markers_to_jsonld(markers: dict) -> dict:
    """
    Convert markers to JSON-LD structured data for
    <script type="application/ld+json">.
    """
    ok = markers.get("orienting_key", markers)
    ego = ok["ego"]

    return {
        "@context": "https://atcooper.net/schema/orienting-key",
        "@type": "OrientingKey",
        "version": ego.get("version", VERSION),
        "project": ego["project"],
        "page": ego["page"],
        "authors": ego["authors"],
        "date": ego.get("date", ""),
        "integrity": {
            "pageLambda": ego["lambda"],
            "pageHash": ego["hash"],
            "contextBindings": ego["context"],
        },
        "sections": [
            {
                "position": bar["position"],
                "total": bar["total"],
                "lambda": bar["lambda"],
                "sigma": bar["sigma"],
                "wordCount": bar["word_count"],
            }
            for bar in ok["superego"]
        ],
    }


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Orienting Key Engine — structural integrity for machine-processed content"
    )
    sub = parser.add_subparsers(dest="command")

    # generate
    gen = sub.add_parser("generate", help="Generate markers for content sections")
    gen.add_argument("--sections", nargs="+", help="Section files (one file per section)")
    gen.add_argument("--document", help="Single document, split by --split delimiter")
    gen.add_argument("--split", default="---", help="Section delimiter (default: ---)")
    gen.add_argument("--page", default="/", help="Page path")
    gen.add_argument("--context", nargs="*", default=[], help="Context page paths")
    gen.add_argument("--project", default="attentional-surface")
    gen.add_argument("--authors", default="ATCR × Claude")
    gen.add_argument("--date", default="")
    gen.add_argument("--salt", default=SITE_SALT)
    gen.add_argument("--output", "-o", help="Output JSON file")
    gen.add_argument("--format", choices=["json", "jsonld", "attrs"], default="json")

    # verify
    ver = sub.add_parser("verify", help="Verify markers against content")
    ver.add_argument("--sections", nargs="+", required=True)
    ver.add_argument("--markers", required=True, help="Markers JSON file")
    ver.add_argument("--salt", default=SITE_SALT)

    # embed (outputs data attributes or JSON-LD)
    emb = sub.add_parser("embed", help="Output embeddable markers")
    emb.add_argument("--markers", required=True, help="Markers JSON file")
    emb.add_argument("--format", choices=["attrs", "jsonld"], default="attrs")

    args = parser.parse_args()

    if args.command == "generate":
        if args.sections:
            sections = [Path(f).read_text() for f in args.sections]
        elif args.document:
            doc = Path(args.document).read_text()
            sections = [s.strip() for s in doc.split(args.split) if s.strip()]
        else:
            parser.error("Provide --sections or --document")

        result = generate_markers(
            args.page, sections, args.context,
            args.project, args.authors, args.date, args.salt,
        )

        if args.format == "jsonld":
            output = markers_to_jsonld(result)
        elif args.format == "attrs":
            output = markers_to_data_attrs(result)
        else:
            output = result

        out = json.dumps(output, indent=2)
        if args.output:
            Path(args.output).write_text(out)
            print(f"Written to {args.output}")
        else:
            print(out)

    elif args.command == "verify":
        sections = [Path(f).read_text() for f in args.sections]
        markers = json.loads(Path(args.markers).read_text())
        result = verify_markers(sections, markers, args.salt)
        print(json.dumps(result, indent=2))
        sys.exit(0 if result["intact"] else 1)

    elif args.command == "embed":
        markers = json.loads(Path(args.markers).read_text())
        if args.format == "jsonld":
            output = markers_to_jsonld(markers)
        else:
            output = markers_to_data_attrs(markers)
        print(json.dumps(output, indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
