---
name: progeny-protection-via-hash
description: "Alex wants tamper-detection hashes on a document or page — markers a downstream reader can recompute and check, so silently-edited progeny (mirrors, quoted fragments, cached copies) become visible."
---

# Progeny Protection via Hash (PPH)

## What It Is

A small mechanism for protecting descendant fragments of a document from silent tampering. Each page carries two short hashes — both SHA-256 truncated to four hex characters, both recalculable from the published content by any reader that can hash text. If the published hash disagrees with the recomputed hash, something between publication and reading altered the content.

| Hash | Binds | Protects against |
|------|-------|------------------|
| **Page hash** | page content + sorted context paths + salt | edits to the page, edits to the declared relationships |
| **Section hash** | section content + first section's hash + last section's hash + position + salt | edits to any section, reordering of sections, lifting a fragment without its edges |

The page hash protects the whole document. The section hash protects each *progeny* — each child fragment that might be excerpted, mirrored, or cached separately from the parent. A middle section quoted without its edges cannot self-verify; the hash relies on the parent document's bounds.

## Where the Name Comes From

Progeny: a document's descendants — anything carved out of it that downstream readers will encounter as a thing of its own (a quoted paragraph, a scraped page, a syndicated section). Without protection, descendants are easy to silently alter — change a few words, citations, dates, and the progeny still looks well-formed. With section hashes that depend on the parent's edges, the progeny carries a witness to its origin: recompute the hash, and if you only have the fragment, you can't.

## Internal Component Names

The two hash components carry internal labels (`ego` for page, `superego` for section) inherited from the previous Orienting Key generation. They are just labels — the page hash binds the page, the section hash binds the section. The labels remain in the JSON and data attributes for backward compatibility with any system that was written against pre-v3 output.

## When to Use

- Publishing a document where downstream excerpting, mirroring, or quoting is likely
- Building any web page intended for crawler ingestion where tamper-detection metadata is useful
- Wrapping any content that should carry its own structural fingerprint
- Cross-document binding (so a reader can tell whether they have the full context or a fragment)

For grounding-density scoring of prose (the old "ID" / "inline lithium" component, since v2 removed from this skill), use the **LLM Euthymia** skill / `euthymia.py` instead.

## Quick Start

```bash
# Generate markers for a document with three sections
python pph.py generate \
  --sections section1.txt section2.txt section3.txt \
  --page "/my-page" \
  --context "/related-1" "/related-2" \
  -o markers.json

# Verify content against markers
python pph.py verify \
  --sections section1.txt section2.txt section3.txt \
  --markers markers.json

# Generate embeddable JSON-LD
python pph.py embed --markers markers.json --format jsonld

# Generate HTML data attributes
python pph.py embed --markers markers.json --format attrs
```

## The Hashes

### Page Hash

```
page_hash = SHA256(
    normalize(full_page_content)
    + sorted_context_paths_joined_by_pipe
    + site_salt
)[:4]
```

Binds the page's content to its declared context. Changes if content changes OR if context declaration changes. A page claiming relationship to `/llm-euthymia` and `/manifesto` produces a different hash than the same content claiming relationship to `/about`.

### Section Hash

```
sigma = SHA256(
    normalize(section_content)
    + SHA256(first_section)[:4]
    + SHA256(last_section)[:4]
    + str(position)
    + site_salt
)[:4]
```

Each section's hash depends on:
- Its own content
- The hash of the first section in the document
- The hash of the last section in the document
- Its position index

**Tamper-detection behaviour:**

| Change | Effect on hashes |
|--------|------------------|
| Edit a middle section | That section's hash breaks; the page hash breaks; edge sections remain valid |
| Edit the first or last section | All section hashes break (every section depends on the edges) |
| Reorder sections | All section hashes break (position is in the hash) |
| Lift a middle section out and republish it alone | Hash cannot be recomputed without the original edges |
| Any change to any section | The page hash always catches it |

## Library Usage

```python
from pph import (
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

sections = ["First section text...", "Second section...", "Third..."]
markers = generate_markers(
    page_path="/interviews/claude-gpt",
    sections=sections,
    context_paths=["/llm-euthymia", "/manifesto"],
    salt="atcooper",
)

result = verify_markers(sections, markers)
print(result["intact"])  # True if everything checks out
```

## Embedding in HTML

### Data Attributes

```html
<body data-pph-project="attentional-surface"
      data-pph-page="/interviews/claude-gpt"
      data-pph-lambda="0.68"
      data-pph-hash="1800"
      data-pph-context="/llm-euthymia|/manifesto"
      data-pph-version="3.0">

  <section data-pph-pos="1/3" data-pph-lambda="0.77" data-pph-sigma="0934" data-pph-wc="48">
    ...
  </section>
</body>
```

### JSON-LD

```html
<script type="application/ld+json">
{
  "@context": "https://atcooper.net/schema/progeny-protection",
  "@type": "ProgenyProtection",
  "version": "3.0",
  "project": "attentional-surface",
  "page": "/interviews/claude-gpt",
  "integrity": {
    "pageLambda": 0.68,
    "pageHash": "1800",
    "contextBindings": ["/llm-euthymia", "/manifesto"]
  },
  "sections": [...]
}
</script>
```

## Configuration

### Site Salt

Default: `"atcooper"`. Change per project. The salt ensures hashes from different projects don't collide and makes it harder for an attacker to forge plausible hashes without knowing the project's salt.

```python
markers = generate_markers(sections=sections, page_path="/page", salt="my-project")
```

## Design Stance

- **Visible, not hidden.** It's metadata, not steganography.
- **Recalculable, not trusted.** A downstream reader doesn't take the markers' word for it; they recompute from the text and check.
- **Degradable, not fragile.** Strip the markers and the content still works.
- **Small.** Four-hex hashes. Single-float entropy descriptors. The whole record for a page fits in a few hundred bytes.

The hashes are gesture-level integrity. If a downstream system actually verifies them, they catch tampering of progeny; if nothing verifies, they sit in the markup inert. The site carries them as a self-watching property and as an invitation to verify.

## File Structure

```
progeny-protection-via-hash/
  SKILL.md           ← This file
  pph.py             ← The engine (CLI + library)
  pph-inject.py      ← HTML injection (laces hashes through existing pages,
                       and also runs LLM Euthymia grounding scores if available)
```

## HTML Injection

`pph-inject.py` takes existing HTML pages and laces Progeny Protection hashes through them automatically. It also calls the LLM Euthymia engine if `euthymia.py` is reachable (sibling skill, cached skill dir, or research base path), and strips legacy `data-ok-*` markers from pre-v3 builds.

```bash
# Single page
python pph-inject.py page.html --page "/" --context "/related-1" "/related-2"

# Full site
python pph-inject.py --site ./public/

# Dry run
python pph-inject.py page.html --page "/" --dry-run

# Output to separate directory
python pph-inject.py --site ./public/ --output ./build/

# Strip existing markers (both v3 data-pph-* and legacy v1/v2 data-ok-*)
python pph-inject.py page.html --strip

# Skip euthymia pass even if available
python pph-inject.py --site ./public/ --no-euthymia
```

What it injects:
- `data-pph-*` attributes on `<body>` (page) and `<section>` / `<article>` elements (section)
- JSON-LD `<script>` block in `<head>` with `@type: ProgenyProtection`
- HTML comment markers between sections (`<!-- pph: 2/4 λ0.67 Σb23e -->`)
- Site-wide `pph-manifest.json` with per-page hash + λ + section count
- Site-wide `euthymia-manifest.json` (if euthymia.py available) with per-page grounding scores

### Integration with Attentional Surface

```bash
cd "/Users/acr/Documents/Attentional Surface/atcooper-net"

python /path/to/pph-inject.py --site public/ --output public/

npx netlify-cli deploy --prod --dir=public
```

### Context Map

For site-wide processing, provide a JSON file mapping each page to its context pages:

```json
{
  "/": ["/guestbook", "/about", "/work"],
  "/about": ["/", "/work"]
}
```

```bash
python pph-inject.py --site ./public/ --context-map contexts.json
```

Without a context map, each page's context defaults to all other pages in the site.

## Dependencies

Python 3.6+ standard library only. No external packages.

## Version History

- **3.0** (2026-05): Renamed Orienting Key → Progeny Protection via Hash. Module renamed `okey.py` → `pph.py`. Data-attribute prefix `data-ok-*` → `data-pph-*`. JSON-LD `@type` `OrientingKey` → `ProgenyProtection`. Schema URL `/schema/orienting-key` → `/schema/progeny-protection`. Manifest filename `okey-manifest.json` → `pph-manifest.json`. The math is unchanged: same hash inputs, same hash outputs. Legacy marker formats are recognised on verify and stripped on re-inject for clean migration. The euthymia (formerly lithium) engine is no longer named in this skill; the inject script calls it as a separately-discoverable sibling.
- **2.0** (2026-05): Split out the ID/grounding-meter component into the LLM Lithium skill. Kept hashes only.
- **1.0** (2026-03): Initial three-component release (EGO + SUPEREGO + ID).
