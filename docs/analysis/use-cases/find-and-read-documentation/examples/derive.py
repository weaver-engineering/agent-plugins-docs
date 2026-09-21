#!/usr/bin/env python3
"""Recompute these examples' own figures from `corpus/`, and write them out.

    python3 derive.py          rewrite registered.md and every search-*.txt / report-*.txt
    python3 derive.py --check  recompute and report any file that has drifted

THIS SPECIFIES NOTHING. It is not a design, not a prototype, and not a claim about
how any of this should be built. It exists because deriving the line numbers, word
counts and rankings cost less than typing them and made them accurate, and accuracy
is worth having where it is free. Everything here is the crudest thing that produces
consistent figures.

Two rules in it are not arbitrary, and both are quoted from the analysis rather
than invented here:

  * Context, Rationale and Appendix contribute no words, so nothing in them can be
    matched (use case step 2, documentation-standards §4).
  * A node matching more of the query's distinct terms ranks above one matching
    fewer; density only separates nodes that matched the same number of them
    (use case §7 — "a result matching several query terms is worth more than one
    matching a single term many times").

The relevance function itself is an open design question (use case §7). The
numbers below are what one crude function gives. They are illustrative, and the
ordering they produce is itself a finding the example is meant to expose rather
than a ranking anyone has agreed.
"""
import re, os, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = 10          # the default cap on a results list; the number design owes
EXCLUDED = ('context', 'rationale', 'appendix')


# ---------------------------------------------------------------- registration
def parse(path):
    L = open(path).read().split('\n')
    while L and not L[-1].strip():
        L.pop()
    heads, fence = [], False
    for i, l in enumerate(L, 1):
        if l.lstrip().startswith('```'):
            fence = not fence; continue
        if fence:
            continue
        m = re.match(r'^(#+) (.*)$', l)
        if m:
            heads.append([i, len(m.group(1)), m.group(2).strip()])
    # a trailing `# Rationale` / `# Appendix` is a child of the document, not a sibling
    for h in heads[1:]:
        if h[1] == 1 and re.match(r'^(Rationale|Appendix\b)', h[2]):
            h[1] = 2
    nodes = []
    for idx, (line, depth, title) in enumerate(heads):
        end = len(L)
        for j in range(idx + 1, len(heads)):
            if heads[j][1] <= depth:
                end = heads[j][0] - 1; break
        kind = ('document' if idx == 0 else
                'context' if title == 'Context' else
                'rationale' if title == 'Rationale' else
                'appendix' if title.startswith('Appendix') else 'section')
        nodes.append({'line': line, 'end': end, 'depth': depth, 'title': title,
                      'kind': kind, 'indexed': kind not in EXCLUDED})
    excl = [(n['line'], n['end']) for n in nodes if n['kind'] in EXCLUDED]
    for n in nodes:
        body = [L[i - 1] for i in range(n['line'], n['end'] + 1)
                if not any(lo <= i <= hi for lo, hi in excl)]
        n['words'] = len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'-]*", ' '.join(body)))
        n['text'] = ' '.join(body).lower()
    todos = [(i, l.strip()) for i, l in enumerate(L, 1) if 'TODO' in l]
    return {'lines': L, 'nodes': nodes, 'todos': todos}


def slug(path):
    return os.path.relpath(path, os.path.join(HERE, 'corpus'))[:-len('.md')]


def ref(path, node):
    """Every node is addressable, including the ones no search can reach."""
    if node['kind'] == 'document':
        return slug(path)
    m = re.match(r'^([0-9.]+) ', node['title'])
    if m:
        return f'{slug(path)}${m.group(1)}'
    return f'{slug(path)}${node["title"].split(":")[0].replace(" ", "-")}'


def load():
    return {p: parse(p) for p in sorted(glob.glob(os.path.join(HERE, 'corpus', '**', '*.md'),
                                                  recursive=True))}


def ancestry(doc, node):
    """The document, then every section above the node, then the node itself."""
    out = []
    for n in doc['nodes']:
        if n['line'] > node['line']:
            continue
        if n['kind'] in EXCLUDED and n is not node:
            continue
        if n['end'] >= node['end'] and n['depth'] <= node['depth']:
            out.append(n)
    return out


# ---------------------------------------------------------------- searching
def search(reg, terms):
    pats = [(t, re.compile(r'\b' + re.escape(t) + r'\b')) for t in terms]
    rows = []
    for p, doc in reg.items():
        for n in doc['nodes']:
            if not n['indexed']:
                continue
            hits = {t: len(rx.findall(n['text'])) for t, rx in pats}
            total = sum(hits.values())
            if not total:
                continue
            cover = sum(1 for v in hits.values() if v) / len(terms)
            density = min(total / n['words'] * 10, 1.0)
            rows.append({'score': round(cover * 0.8 + density * 0.2, 2),
                         'ref': ref(p, n), 'words': n['words'], 'path': p, 'node': n})
    rows.sort(key=lambda r: (-r['score'], r['ref']))
    return rows


def render_search_json(reg, query, terms):
    """The same answer, written for a parser.

    Every field is present whether or not it has anything in it — a parser that has
    to tell "absent" from "empty" breaks on the empty case (search §6.1).
    """
    rows = search(reg, terms)
    shown, withheld = rows[:CAP], max(0, len(rows) - CAP)
    results = []
    for r in shown:
        chain = ancestry(reg[r['path']], r['node'])
        results.append(
            '    {"reference": %s, "title": %s, "relevance": %.2f, "words": %d,\n'
            '     "ancestry": [%s]}' % (
                j(r['ref']), j(r['node']['title']), r['score'], r['words'],
                ', '.join('{"title": %s, "words": %d}' % (j(a['title']), a['words'])
                          for a in chain)))
    return ('{\n'
            '  "ok": true,\n'
            '  "query": %s,\n'
            '  "registries_searched": [{"name": null, "location": "/repo/docs"}],\n'
            '  "matched": %d,\n'
            '  "reported": %d,\n'
            '  "withheld": %d,\n'
            '  "results": [\n%s\n  ]\n'
            '}\n') % (j(query), len(rows), len(shown), withheld, ',\n'.join(results))


def j(s):
    return '"' + str(s).replace('\\', '\\\\').replace('"', '\\"') + '"'


def render_register(reg):
    out = ['$ weaverdoc register corpus/ --recurse', '', 'registered:']
    for p, doc in reg.items():
        secs = [n for n in doc['nodes'] if n['kind'] == 'section']
        nums = [re.match(r'^([0-9.]+) ', n['title']).group(1) for n in secs
                if re.match(r'^([0-9.]+) ', n['title'])]
        span = f'§{nums[0]} - §{nums[-1]}' if nums else 'no numbered sections'
        out.append(f'- {slug(p)}.md - {len(secs)} sections, {span}')
    todos = [(slug(p), line, txt) for p, doc in reg.items() for line, txt in doc['todos']]
    out += ['', f'outstanding TODOs: {len(todos)}']
    for s, line, txt in todos:
        out.append(f'- {s}.md:{line}')
    out += ['', 'unchanged: 0', 'dropped: none', 'not documents: corpus/notes.txt']
    return '\n'.join(out) + '\n'


def render_register_after_deletion(reg, gone):
    """Extension 2a: the same path registered again after a document was deleted.

    Registering is absolute rather than differential, so what the registry ends up
    holding is computed from what is under the path now. What changes is the report.
    """
    out = ['# the document at policies/retention-policy.md was deleted since the last run',
           '$ weaverdoc register corpus/ --recurse', '', 'registered:']
    for p, doc in reg.items():
        if slug(p) == gone:
            continue
        secs = [n for n in doc['nodes'] if n['kind'] == 'section']
        nums = [re.match(r'^([0-9.]+) ', n['title']).group(1) for n in secs
                if re.match(r'^([0-9.]+) ', n['title'])]
        span = f'§{nums[0]} - §{nums[-1]}' if nums else 'no numbered sections'
        out.append(f'- {slug(p)}.md - {len(secs)} sections, {span}')
    dropped = reg[os.path.join(HERE, 'corpus', gone + '.md')]
    nodes = len([n for n in dropped['nodes'] if n['indexed']])
    out += ['', 'dropped:', f'- {gone}.md - no longer present; {nodes} registrations removed']
    out += ['', 'outstanding TODOs: 1', '- procedures/cache-tuning.md:15']
    out += ['', 'unchanged: 0', 'not documents: corpus/notes.txt']
    return '\n'.join(out) + '\n'


def render_search(reg, query, terms):
    rows = search(reg, terms)
    shown, withheld = rows[:CAP], max(0, len(rows) - CAP)
    out = [f'$ weaverdoc search "{query}"', '']
    out += ['registries searched:', '  /repo/docs (no scope named; the registry at this location)', '']
    if not shown:
        out.append(f'nothing answered "{query}"')
        return '\n'.join(out) + '\n', rows, withheld
    for r in shown:
        out.append(f'{r["ref"]:<46} - {r["score"]:.2f} over {r["words"]} words')
        chain = ancestry(reg[r['path']], r['node'])
        for depth, a in enumerate(chain):
            count = '' if a is r['node'] else f' - {a["words"]} words'
            out.append('  ' + '  ' * depth + f'- {a["title"]}{count}')
    if withheld:
        out += ['', f'... ({withheld} more matches)']
    return '\n'.join(out) + '\n', rows, withheld


# ---------------------------------------------------------------- reporting
def render_report(reg, reference):
    base, _, sec = reference.partition('$')
    path = os.path.join(HERE, 'corpus', base + '.md')
    doc = reg[path]
    node = next((n for n in doc['nodes'] if ref(path, n) == reference), None)
    if node is None:
        raise SystemExit(f'no such reference: {reference}')
    chain = ancestry(doc, node)
    span = node['end'] - node['line'] + 1
    total = len(doc['lines'])
    out = [f'$ weaverdoc report {reference}', '']
    out.append('context path:')
    for depth, a in enumerate(chain):
        out.append('  ' + '  ' * depth + f'- {a["title"]}')
    out.append('')
    out.append(f'{base}.md lines {node["line"]}-{node["end"]} '
               f'({span} of {total} lines in the document)')
    out.append('')
    out += doc['lines'][node['line'] - 1:node['end']]
    return '\n'.join(out) + '\n'


# ---------------------------------------------------------------- registered state
def render_registered(reg):
    out = ['# Registered — the example corpus', '',
           'What the registry holds after `corpus/` is registered, whatever form it holds it in. Nothing here says',
           'how any of it is stored.', '',
           '`words` says whether the node\'s own text contributed to what a search can match. `lines` is the node\'s',
           'span in its source document, first line to last. A node with `words: no` stays addressable and can still',
           'be reported; it is simply never matched.', '',
           '**Derived, not typed.** `python3 derive.py --check` recomputes every figure below from `corpus/`.', '']
    for i, (p, doc) in enumerate(reg.items(), 1):
        out += [f'## {i} `{slug(p)}.md`', '',
                '| Node | Type | Reference | Lines | Words | Indexed |',
                '|---|---|---|---|---|---|']
        for n in doc['nodes']:
            name = ('*(document root)* `' + n['title'] + '`' if n['kind'] == 'document'
                    else '`' + n['title'] + '`')
            r = f'`{ref(p, n)}`' if n['indexed'] else '—'
            w = str(n['words']) if n['indexed'] else '—'
            out.append(f'| {"&nbsp;" * 2 * (n["depth"] - 1)}{name} | {n["kind"]} | {r} | '
                       f'{n["line"]}-{n["end"]} | {w} | {"yes" if n["indexed"] else "no"} |')
        out.append('')
        if doc['todos']:
            for line, txt in doc['todos']:
                out.append(f'Outstanding TODO at line {line}: {txt}')
        else:
            out.append('No outstanding TODO markers.')
        out.append('')
    total = sum(len(d['nodes']) for d in reg.values())
    idx = sum(1 for d in reg.values() for n in d['nodes'] if n['indexed'])
    out += [f'## {len(reg) + 1} Totals', '',
            f'{len(reg)} documents, {total} nodes, of which {idx} can answer a search and '
            f'{total - idx} are structure only.', '',
            '`corpus/notes.txt` is not a markdown document. It is not registered, it is not reported, and no',
            'answer mentions it — silently, because a file that is not a document is not a failure.', '']
    return '\n'.join(out)


# ---------------------------------------------------------------- outputs
SEARCHES = [
    ('search-truncated.txt', 'eviction policy', ['eviction', 'policy']),
    ('search-answer.txt', 'retention class', ['retention', 'class']),
    ('search-empty.txt', 'quota', ['quota']),
    # "thrashing" appears twice in the corpus and both times inside an excluded zone
    ('search-excluded-zone.txt', 'thrashing', ['thrashing']),
]
REPORTS = [
    ('report-section.txt', 'policies/eviction-policy$2.1'),
    ('report-document.txt', 'policies/retention-policy'),
    # extension 7a: a rationale is never returned by a search, and is always
    # addressable — the Agent derives this reference from the section it justifies
    ('report-rationale.txt', 'procedures/cache-tuning$Rationale'),
]


def main():
    reg = load()
    files = {'registered.md': render_registered(reg),
             'register.txt': render_register(reg),
             'search-truncated.json': render_search_json(reg, 'eviction policy',
                                                         ['eviction', 'policy']),
             'register-after-deletion.txt': render_register_after_deletion(
                 reg, 'policies/retention-policy')}
    for name, query, terms in SEARCHES:
        files[name] = render_search(reg, query, terms)[0]
    for name, reference in REPORTS:
        files[name] = render_report(reg, reference)
    check = '--check' in sys.argv
    drift = 0
    for name, body in files.items():
        p = os.path.join(HERE, name)
        old = open(p).read() if os.path.exists(p) else None
        if check:
            if old != body:
                print(f'DRIFTED  {name}')
                drift += 1
            else:
                print(f'ok       {name}')
        else:
            open(p, 'w').write(body)
            print(f'{"wrote   " if old != body else "unchanged"} {name}')
    if check:
        print('every figure matches the corpus' if not drift else
              f'{drift} file(s) no longer match the corpus — run without --check')
    return 1 if drift else 0


if __name__ == '__main__':
    sys.exit(main())
