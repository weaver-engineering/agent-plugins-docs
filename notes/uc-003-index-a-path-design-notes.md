# UC-003 (Index A Path) — Design Notes

Free-form, `notes/` — not a spec, not indexed, not reviewed for correctness. This is the throwaway tooling used
to hand-generate every `.index/` file this session, kept here as a starting point for whoever designs UC-003's
real implementation, rather than letting it evaporate at the end of the conversation that produced it.

## Status: what's actually scripted vs. done by hand

**Scripted, and reasonably mature**: word extraction/tokenization/stemming/stopword-filtering (§1 below). Used
as-is (with small fixes along the way) to generate every `.words.yaml` from UC-002 onward.

**Not scripted at all — done by manually reading `cat -n` output each time**:
- Section-boundary detection (`start_line`/`end_line` per heading, including the rule that a parent section's
  range extends to cover its nested children). No heading parser was written; every `.sections.yaml` this
  session was hand-computed by eyeballing line numbers.
- `//TODO`-marker extraction and `ref` pulling. Every `.todo.yaml` entry so far was found by visually scanning
  for `//TODO` and copying out the task ref by hand.

A real implementation needs both of those built, not just the word tokenizer. The word tokenizer is the
furthest along of the three because it was iterated on the most (see bugs found, below) — that's an accident of
which part got exercised most during elicitation, not a signal that it's more important.

## 1 Word tokenizer (Python, current state)

```python
import re

STOPWORDS = set("""
a an the and or but if then than so such from into each every any all some most other
which who whom what when where why how do does did doing can could should would will
shall must may might there here this that these those it be is are was were been being
have has had having of to in on with as at by for not no i we you they he she them my
your our their his her its also just still yet own same both either neither more less
many much one two above below between during after before out about over under again
further once only very get see document
""".split())

def stem(word):
    w = word.lower()
    if w.endswith("'s"):
        w = w[:-2]
    if w in ("plus",):
        return "plus"
    if w in ("architects", "architect's"):
        return "architect"
    if w in ("documents", "documented", "documentation", "docs", "doc"):
        return "document"
    if w in ("indexed", "indexing", "indexes", "index's"):
        return "index"
    if w in ("numbering", "numbered", "numbers"):
        return "number"
    # ... more hardcoded irregular/domain mappings, added reactively as
    # each new document surfaced a new word needing one. Not a general
    # solution - see "Known problems" below.
    if w.endswith("ies") and len(w) > 4:
        return w[:-3] + "y"
    if w.endswith("es") and len(w) > 4:
        return w[:-2]
    if w.endswith("s") and not w.endswith("ss") and not w.endswith("us") and len(w) > 3:
        return w[:-1]
    return w

def strip_md_link_to_url(text):
    def repl(m):
        url = m.group(2)
        url = url.split('?')[0].split('#')[0]
        return ' ' + url + ' '
    return re.sub(r'\[([^\]]*)\]\(([^)]*)\)', repl, text)

def tokenize(text):
    text = strip_md_link_to_url(text)
    # drop Cockburn-style extension labels like **5a.** so they don't get
    # tokenized as content - a hack, see "Known problems"
    text = re.sub(r'\*\*\d+[a-z]\.\*\*', ' ', text)
    words = re.findall(r"[a-zA-Z0-9@][a-zA-Z0-9@'/.:_-]*[a-zA-Z0-9]|[a-zA-Z]", text)
    out = []
    for w in words:
        wl = w.lower().strip("'\"/.:_-")
        if not wl:
            continue
        if wl.startswith('@'):
            out.append(wl)  # verbatim external-ref token, never decomposed
            continue
        if re.match(r'^[0-9.]+[a-z]?$', wl) and re.match(r'^[0-9]', wl):
            continue  # bare numbers / section-number-shaped tokens
        root = stem(wl)
        if not root or root in STOPWORDS or len(root) <= 1:
            continue
        out.append(root)
    return out
```

This was run per-section over a manually-sliced `lines[start-1:end]` range (the section boundaries themselves
already having been hand-computed) — the script never parsed a whole document end to end.

## Known problems, found while using it

* **Stemming is a hand-maintained lookup table, not a real algorithm.** Every irregular form (`architects` →
  `architect`, `indexed`/`indexing` → `index`, etc.) was added reactively, one word at a time, as each new
  document happened to use it. This will not generalize — a real implementation needs an actual stemmer (Porter
  or similar) rather than a growing `if` chain.
* **The generic suffix-stripping rule is unsound.** `endswith("s")` → strip trailing `s` incorrectly turned
  `plus` into `plu` before it got special-cased. There are certainly other false positives lurking (any word
  ending in `s` that isn't a plural).
* **Irregular verb forms aren't reachable from their root by this stemmer at all.** `is`/`are`/`was`/`were`
  /`been`/`being` don't reduce to `be` via suffix-stripping — this was only caught because a real word index for
  UC-003 surfaced them leaking through as if they were content words. Fixed by listing the irregular forms
  directly in `stopwords.yaml` rather than fixing the stemmer (see that file's own comment). The same gap
  likely exists for other irregular content words the stopword list doesn't cover.
* **The extension-label strip (`**5a.**`) is a one-off regex**, not a principled distinction between "structural
  label" and "content" — it only catches the exact bold-Cockburn-label format used in these use cases.
* **URL query/anchor stripping (`split('?')[0].split('#')[0]`) is untested against real edge cases** — e.g. a
  path that legitimately contains a literal `#` or `?` character.

## Not attempted at all

* Section/figure boundary computation (the actual heading→line-range algorithm).
* `//TODO` recognition and `ref` extraction as code, rather than by eye.
* Anything to do with `sections.yaml`'s `number` attribute — deriving it, or the UC-002 auto-numbering behavior
  it depends on.
