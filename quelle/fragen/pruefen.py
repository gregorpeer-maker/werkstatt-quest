#!/usr/bin/env python3
"""Liest die Fragen-Dateien (fragen/*.txt) und prüft sie.

Format je Zeile:
  M Frage | richtig | falsch | falsch | falsch || Erklärung >> Tipp
  R Aussage (richtig) || Erklärung >> Tipp
  F Aussage (falsch)  || Erklärung >> Tipp
  N Frage | Wert | Einheit | Toleranz || Erklärung >> Tipp
  Z Frage | links = rechts | links = rechts | ...
Zeilen mit # sind Kommentare.
"""
import sys, os, re, json, glob, collections


def parse(path, world, level, prefix):
    out, n = [], 0
    for ln, raw in enumerate(open(path, encoding='utf-8'), 1):
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        n += 1
        kind, rest = line[0], line[1:].strip()
        hint = ''
        if '>>' in rest:
            rest, hint = [x.strip() for x in rest.split('>>', 1)]
        explain = ''
        if '||' in rest:
            rest, explain = [x.strip() for x in rest.split('||', 1)]
        parts = [x.strip() for x in rest.split('|')]
        q = {'id': '%s_%03d' % (prefix, n), 'world': world, 'level': level, 'text': parts[0], 'explain': explain}
        if hint:
            q['hint'] = hint
        where = '%s:%d' % (os.path.basename(path), ln)
        if kind == 'M':
            assert len(parts) == 5, where + ' braucht 4 Antworten'
            assert len(set(parts[1:])) == 4, where + ' doppelte Antwort'
            q.update(type='mc', options=parts[1:], answer=0)
        elif kind in 'RF':
            assert len(parts) == 1, where + ' R/F ohne |'
            q.update(type='tf', answer=kind == 'R')
        elif kind == 'N':
            assert len(parts) in (3, 4), where + ' N braucht Wert | Einheit | Toleranz'
            q.update(type='num', answer=float(parts[1].replace(',', '.')), unit=parts[2],
                     tol=float(parts[3].replace(',', '.')) if len(parts) == 4 else 0.0)
        elif kind == 'Z':
            pairs = [[a.strip() for a in p.split(' = ', 1)] for p in parts[1:]]
            assert 2 <= len(pairs) <= 6 and all(len(p) == 2 and p[0] and p[1] for p in pairs), where + ' Z-Paare'
            assert len({p[1] for p in pairs}) == len(pairs), where + ' doppelte Zuordnung'
            q.update(type='match', pairs=pairs)
        else:
            raise AssertionError(where + ' unbekannter Typ ' + kind)
        assert q['text'], where
        out.append(q)
    return out


WELTEN = ['et', 'fr', 'edv', 'it', 'en']


def dateien(folder):
    """(Dateiname ohne Endung, Welt, Level, ID-Präfix) für alle vorhandenen Fragen-Dateien."""
    out = []
    for n in range(1, 9):
        out.append(('kfz_lf%d' % n, 'kfz', n - 1, 'k%d' % n))
    for w in WELTEN:
        for l in range(5):
            out.append(('%s_%d' % (w, l), w, l, '%s%d' % (w, l)))
    return [x for x in out if os.path.exists(os.path.join(folder, x[0] + '.txt'))]


def load_all(folder):
    qs = []
    for name, w, lvl, pre in dateien(folder):
        qs += parse(os.path.join(folder, name + '.txt'), w, lvl, pre)
    return qs


if __name__ == '__main__':
    folder = os.path.dirname(os.path.abspath(__file__))
    qs = load_all(folder)
    seen = collections.Counter((q['world'], q['text']) for q in qs)
    for t, c in seen.items():
        if c > 1:
            print('DOPPELT:', t)
    for name, w, lvl in [(x[0], x[1], x[2]) for x in dateien(folder)]:
        L = [q for q in qs if q['world'] == w and q['level'] == lvl]
        c = collections.Counter(q['type'] for q in L)
        tf = [q for q in L if q['type'] == 'tf']
        print('%s: %d Fragen %s, R/F richtig=%d falsch=%d' % (name, len(L), dict(c), sum(q['answer'] for q in tf), sum(not q['answer'] for q in tf)))
        longest = max((max(len(o) for o in q['options']) for q in L if q['type'] == 'mc'), default=0)
        # Hinweis, falls die richtige Antwort auffällig oft die längste ist
        mc = [q for q in L if q['type'] == 'mc']
        longest_right = sum(1 for q in mc if len(q['options'][0]) == max(len(o) for o in q['options']))
        print('   richtige Antwort ist die längste bei %d von %d MC-Fragen' % (longest_right, len(mc)))
