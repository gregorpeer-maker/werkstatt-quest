#!/usr/bin/env python3
"""Hilfsskript: zeigt die MC-Fragen einer Datei nummeriert an bzw. ersetzt ihre falschen Antworten.
  python3 haerten.py zeigen kfz_lf1.txt
  python3 haerten.py setzen kfz_lf1.txt patch.txt     (patch: Nummer | falsch | falsch | falsch)
"""
import sys
mode, f = sys.argv[1], sys.argv[2]
L = open(f, encoding='utf-8').read().split('\n')
idx = [i for i, l in enumerate(L) if l.startswith('M ')]
if mode == 'zeigen':
    for n, i in enumerate(idx, 1):
        body = L[i][2:].split('||')[0].split('>>')[0]
        p = [x.strip() for x in body.split('|')]
        print('%d %s => %s' % (n, p[0], p[1]))
else:
    done = set()
    for raw in open(sys.argv[3], encoding='utf-8'):
        raw = raw.strip()
        if not raw or raw.startswith('#'):
            continue
        p = [x.strip() for x in raw.split('|')]
        n = int(p[0]); assert len(p) == 4, raw
        assert n not in done, 'doppelt %d' % n
        done.add(n)
        i = idx[n - 1]
        rest = L[i][2:]
        tail = ''
        for sep in ('||', '>>'):
            if sep in rest:
                k = rest.index(sep); tail = ' ' + rest[k:] ; rest = rest[:k]; break
        q = [x.strip() for x in rest.split('|')]
        L[i] = 'M ' + ' | '.join([q[0], q[1]] + p[1:]) + tail.rstrip()
    print('%d von %d MC-Fragen ersetzt, offen: %s' % (len(done), len(idx), sorted(set(range(1, len(idx) + 1)) - done)[:20]))
    open(f, 'w', encoding='utf-8').write('\n'.join(L))
