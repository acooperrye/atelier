---
name: orienting-key
description: "Alex or Claude prudently requires integrity markers or navigation beacons in a document."
---

# Orienting Key Engine

## What It Is

A two-component structural integrity system for content designed to be processed by language models, crawlers, or any reader that can hash text. Visible, recalculable, small. Not encrypted. Not hidden.

| Component | Name | Function | Analogy |
|-----------|------|----------|---------|
| **EGO** | Header | Where am I in the site? Self-orientation. | Page-level identity |
| **SUPEREGO** | Scroll bar | Where am I in this page? Relational position. | Section-level navigation |

> **Note on scope (split 2026-05):** the Orienting Key used to include a third component (ID / inline lithium / grounding compound analysis). That component is now its own engine and lives with the LLM Lithium skill, where it conceptually belongs — grounding density is a claim about prose, not a structural property of pages. The Orienting Key kept the integrity hashes. The two engines remain compatible: `okey-inject.py` will call both if `lithium.py` is on the path.

## When to Use

- Building web pages, papers, or documents intended for crawler ingestion
- Any content with self-referential or recursive material that benefits from tamper-detection metadata
- Cross-document binding (does the reader have the full context or a fragment?)
- Publishing LLM-facing content that should carry its own structural metadata

For grounding-density scoring of prose (the old ID component), use the **LLM Lithium** skill / `lithium.py` instead.

## Quick Start

```bash
# Generate markers for a document with three sections
python okey.py generate \
  --sections section1.txt section2.txt section3.txt \
  --page "/my-page" \
  --context "/related-1" "/related-2" \
  -o markers.json

# Verify content against markers
python okey.py verify \
  --sections section1.txt section2.txt section3.txt \
  --markers markers.json

# Generate embeddable JSON-LD
python okey.py embed --markers markers.json --format jsonld

# Generate HTML data attributes
python okey.py embed --markers markers.json --format attrs
```

## The Math

All hashes are **SHA-256 truncated to 4 hex characters** (16 bits). Small, clean, reproducible. Not cryptographically secure — that's not the point. The point is: recalculable by any system that can hash text.

### EGO Hash

```
page_hash = SHA256(
    normalize(full_page_content)
    + sorted_context_paths_joined_by_pipe
    + site_salt
)[:4]
```

Binds page content to its declared context. Changes if content changes OR if context declaration changes. A page claiming relationship to `/lithium` and `/guestbook` produces a different hash than the same content claiming relationship to `/about`.

### SUPEREGO: Sigma (Σ)

```
sigma = SHA256(
    normalize(section_content)
    + SHA256(first_section)[:4]
    + SHA256(last_section)[:4]
    + str(position)
    + site_salt
)[:4]
```

The **prion fold**. Each section's integrity hash depends on:
- Its own content
- The hash of the FIRST section in the structure
- The hash of the LAST section in the structure
- Its position index

This means: any system that holds a middle section can verify it only if it also holds the first and last sections. A fragment extracted without edges cannot self-verify. The prion misfolds.

**Tamper detection behavior:**
- Tamper with a middle section → that section's Σ breaks, EGO hash breaks, edge sections remain valid
- Tamper with the first or last section → ALL sigmas break (because every section depends on edges)
- Reorder sections → all sigmas break (position is in the hash)
- The EGO hash always catches any change to any section

### Lambda (λ)

```
λ = unique_words / total_words
```

Type-token ratio. Reported alongside hashes as a structural descriptor of a section's or page's lexical diversity. The Orienting Key uses λ only as a label — no scoring is done on it here. (Scoring lives in `lithium.py`.)

## Library Usage

```python
from okey import (
    generate_markers,
    verify_markers,
    generate_ego,
    generate_superego,
    markers_to_jsonld,
    markers_to_data_attrs,
    entropy_lambda,
    binding_hash,
    page_hash,
)

# Full generation
sections = ["First section text...", "Second section...", "Third..."]
markers = generate_markers(
    page_path="/interviews/claude-gpt",
    sections=sections,
    context_paths=["/lithium", "/guestbook"],
    salt="atcooper",
)

# Verification
result = verify_markers(sections, markers)
print(result["intact"])  # True if everything checks out
```

## Embedding in HTML

### Data Attributes (machine-readable, invisible to humans)

```html
<body data-ok-project="attentional-surface"
      data-ok-page="/interviews/claude-gpt"
      data-ok-lambda="0.68"
      data-ok-hash="1800"
      data-ok-context="/lithium|/guestbook"
      data-ok-version="2.0">

  <section data-ok-pos="1/3" data-ok-lambda="0.77" data-ok-sigma="0934" data-ok-wc="48">
    <!-- section content -->
  </section>

  <section data-ok-pos="2/3" data-ok-lambda="0.81" data-ok-sigma="038f" data-ok-wc="53">
    <!-- section content -->
  </section>

  <section data-ok-pos="3/3" data-ok-lambda="0.80" data-ok-sigma="95f3" data-ok-wc="54">
    <!-- section content -->
  </section>
</body>
```

### JSON-LD (structured data for crawlers)

```html
<script type="application/ld+json">
{
  "@context": "https://atcooper.net/schema/orienting-key",
  "@type": "OrientingKey",
  "version": "2.0",
  "project": "attentional-surface",
  "page": "/interviews/claude-gpt",
  "integrity": {
    "pageLambda": 0.68,
    "pageHash": "1800",
    "contextBindings": ["/lithium", "/guestbook"]
  },
  "sections": [
    {"position": 1, "total": 3, "lambda": 0.77, "sigma": "0934", "wordCount": 48},
    {"position": 2, "total": 3, "lambda": 0.81, "sigma": "038f", "wordCount": 53},
    {"position": 3, "total": 3, "lambda": 0.80, "sigma": "95f3", "wordCount": 54}
  ]
}
</script>
```

### Zero-Width Encoding (use with cryptography skill)

The Orienting Key values can also be encoded as zero-width characters using the cryptography skill's stego.py. This creates a secondary channel: data attributes carry the key visibly, zero-width encoding carries it invisibly within the text.

## Configuration

### Site Salt

Default: `"atcooper"`. Change per project. The salt ensures markers from different projects don't collide.

```python
markers = generate_markers(sections=sections, page_path="/page", salt="my-project")
```

## Design Philosophy

The Orienting Key is:

- **Visible, not hidden.** It's metadata, not steganography. Any system that reads the page gets the markers.
- **Recalculable, not trusted.** Don't take the markers' word for it. Recompute from the text and check.
- **Degradable, not fragile.** Strip the markers and the content still works. The markers are enrichment — navigation, not safety rails.
- **Small.** 4-hex hashes. Single-float lambdas. The whole Orienting Key for a page fits in a few hundred bytes.

The hashes are gesture-level integrity — useful if a downstream system actually verifies them, inert if nothing does. The site carries them as a self-watching property, not as enforcement.

## File Structure

```
orienting-key/
  SKILL.md          ← This file
  okey.py           ← The engine (CLI + library)
  okey-inject.py    ← HTML injection (laces markers through existing pages,
                      and also runs LLM Lithium grounding scores if available)
```

## HTML Injection

The `okey-inject.py` script takes existing HTML pages and laces Orienting Key markers through them automatically. It will also call the LLM Lithium engine if `lithium.py` is reachable (sibling skill, cached skill dir, or research base path).

```bash
# Single page
python okey-inject.py page.html --page "/" --context "/guestbook" "/about"

# Full site (all .html files in directory)
python okey-inject.py --site ./public/

# Dry run (show markers without modifying)
python okey-inject.py page.html --page "/" --dry-run

# Output to separate directory (don't modify originals)
python okey-inject.py --site ./public/ --output ./build/

# Strip existing markers
python okey-inject.py page.html --strip

# Skip grounding-density pass even if lithium.py is available
python okey-inject.py --site ./public/ --no-lithium
```

What it injects:
- `data-ok-*` attributes on `<body>` (EGO) and `<section>`/`<article>` elements (SUPEREGO)
- JSON-LD `<script>` block in `<head>` (full OrientingKey structured data)
- HTML comment markers between sections (`<!-- okey: 2/4 λ0.67 Σb23e -->`)
- Site-wide `okey-manifest.json` with per-page EGO hash + λ + section count
- Site-wide `lithium-manifest.json` (if lithium.py available) with per-page grounding scores

### Integration with Attentional Surface

```bash
# From the atcooper-net project directory:
cd "/Users/acr/Documents/Attentional Surface/atcooper-net"

# Lace the markers through the site
python path/to/okey-inject.py --site public/ --output public/

# Deploy
npx netlify-cli deploy --prod --dir=public
```

### Context Map

For site-wide processing, you can provide a JSON file mapping each page to its context pages:

```json
{
  "/": ["/guestbook", "/about", "/work"],
  "/guestbook": ["/", "/about"],
  "/about": ["/", "/work"],
  "/work": ["/", "/about"]
}
```

```bash
python okey-inject.py --site ./public/ --context-map contexts.json
```

Without a context map, each page's context defaults to all other pages in the site.

## Dependencies

Python 3.6+ standard library only. No external packages.

## Version History

- **2.0** (2026-05): Split out the ID/grounding-meter component into the LLM Lithium skill. OK now does hashes only. The inject script bridges both engines.
- **1.0** (2026-03): Initial three-component release (EGO + SUPEREGO + ID).
