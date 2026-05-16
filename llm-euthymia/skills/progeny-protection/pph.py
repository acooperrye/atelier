#!/usr/bin/env python3
"""
Progeny Protection via Hash (pph)
=================================
A small mechanism for protecting descendant fragments of a document
from silent tampering. Every page carries two short hashes:

  PAGE hash    — binds the whole page's content to the list of pages
                 it claims to be related to (its declared context).
  SECTION hash — binds each section's content to the FIRST section,
                 the LAST section, and the section's position. A
                 middle fragment lifted out without its edges cannot
                 self-verify.

Hashes are SHA-256 truncated to 4 hex characters. Not cryptographically
secure — small, recalculable, recoverable by any reader that can hash
text. The point is that a downstream reader can recompute the hash
from the published content and check it. If the published hash and
the recomputed hash disagree, something between publication and
reading altered the content. The progeny (the quoted section, the
mirrored page, the cached copy) was modified.

Internal component names (`ego`, `superego`) are preserved from the
previous Orienting Key generation for backward compatibility with
data attributes already deployed across the site. They are simply
labels for "page" and "section" respectively.

Version 3.0 (2026-05): renamed from Orienting Key → Progeny Protection
via Hash. The grounding-meter component (formerly "ID" / inline
lithium) has been gone since v2.0 and lives with the LLM Euthymia skill.

Usage:
  python pph.py generate  --sections file1.txt file2.txt ...
  python pph.py generate  --document doc.txt --split "---"
  python pph.py verify    --sections file1.txt file2.txt ... --markers markers.json
  python pph.py embed     --markers markers.json --format jsonld
  python pph.py embed     --markers markers.json --format attrs

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

HASH_LENGTH = 4
SITE_SALT = "atcooper"
VERSION = "3.0"
SCHEMA_URL = "https://atcooper.net/schema/progeny-protection"
SCHEMA_TYPE = "ProgenyProtection"


# ─────────────────────────────────────────────
# CORE
# ─────────────────────────────────────────────

def _clean(text: str) -> str:
    return re.sub(r'\s+', ' ', text.strip().lower())


def _hash(text: str, length: int = HASH_LENGTH) -> str:
    h = hashlib.sha256(_clean(text).encode('utf-8')).hexdigest()
    return h[:length]


def _words(text: str) -> list:
    return re.findall(r"[a-zA-Z']+", text.lower())


def entropy_lambda(text: str) -> float:
    """Type-token ratio. Reported as a structural descriptor; no scoring."""
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
    Hash of section + hash(first) + hash(last) + position + salt.
    A section cannot self-verify without the edges of its containing
    document. The fragment carries its parent's signature.
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
    Hash of page_content + sorted_context_paths + salt.
    Binds the page to the network of pages it declares relationship with.
    Changes if content changes OR if context declaration changes.
    """
    context_str = "|".join(sorted(context_paths))
    payload = _clean(page_content) + context_str + salt
    return _hash(payload)


# ─────────────────────────────────────────────
# PAGE — internal label: ego
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
    """Page-level header: identity + context + page hash."""
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
# SECTION — internal label: superego
# ─────────────────────────────────────────────

def generate_superego(sections: list, salt: str = SITE_SALT) -> list:
    """Per-section records: position, lambda, sigma (binding hash), word count."""
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
    """Generate the complete Progeny Protection record for a page."""
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
        "progeny_protection": {
            "ego": ego,
            "superego": superego,
        }
    }


# ─────────────────────────────────────────────
# VERIFICATION
# ─────────────────────────────────────────────

def verify_markers(sections: list, markers: dict, salt: str = SITE_SALT) -> dict:
    """Recompute the hashes against actual content and report pass/fail."""
    results = {"ego": {}, "superego": [], "intact": True}
    # Accept both new ("progeny_protection") and legacy ("orienting_key") keys
    pph = (
        markers.get("progeny_protection")
        or markers.get("orienting_key")
        or markers
    )

    ego = pph.get("ego", {})
    full_content = "\n".join(sections)
    expected_lambda = entropy_lambda(full_content)
    expected_hash = page_hash(full_content, ego.get("context", []), salt)

    results["ego"]["lambda_match"] = ego.get("lambda") == expected_lambda
    results["ego"]["hash_match"] = ego.get("hash") == expected_hash
    results["ego"]["expected_lambda"] = expected_lambda
    results["ego"]["expected_hash"] = expected_hash

    if not results["ego"]["lambda_match"] or not results["ego"]["hash_match"]:
        results["intact"] = False

    expected_bars = generate_superego(sections, salt)
    for i, (expected, actual) in enumerate(
        zip(expected_bars, pph.get("superego", []))
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
    Render as HTML data-attribute mappings.
    Attribute prefix is data-pph-* (was data-ok-* in pre-v3 builds).
    """
    pph = (
        markers.get("progeny_protection")
        or markers.get("orienting_key")
        or markers
    )
    ego = pph["ego"]
    attrs = {}

    attrs["page"] = {
        "data-pph-project": ego["project"],
        "data-pph-page": ego["page"],
        "data-pph-lambda": str(ego["lambda"]),
        "data-pph-hash": ego["hash"],
        "data-pph-context": "|".join(ego["context"]),
        "data-pph-version": ego.get("version", VERSION),
    }

    for bar in pph["superego"]:
        key = f"section-{bar['position']}"
        attrs[key] = {
            "data-pph-pos": f"{bar['position']}/{bar['total']}",
            "data-pph-lambda": str(bar["lambda"]),
            "data-pph-sigma": bar["sigma"],
            "data-pph-wc": str(bar["word_count"]),
        }

    return attrs


def markers_to_jsonld(markers: dict) -> dict:
    """Render as JSON-LD structured data."""
    pph = (
        markers.get("progeny_protection")
        or markers.get("orienting_key")
        or markers
    )
    ego = pph["ego"]

    return {
        "@context": SCHEMA_URL,
        "@type": SCHEMA_TYPE,
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
            for bar in pph["superego"]
        ],
    }


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Progeny Protection via Hash — structural integrity for descendant fragments"
    )
    sub = parser.add_subparsers(dest="command")

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

    ver = sub.add_parser("verify", help="Verify markers against content")
    ver.add_argument("--sections", nargs="+", required=True)
    ver.add_argument("--markers", required=True, help="Markers JSON file")
    ver.add_argument("--salt", default=SITE_SALT)

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
