#!/usr/bin/env python3
"""Erzeugt it_0..4.txt und en_0..4.txt (je 100 Fragen) aus vokabeln.txt und den Sätzen in it_saetze.txt / en_saetze.txt.
Falsche Antworten stammen aus derselben Themengruppe, damit sie nicht offensichtlich sind.
Neu erzeugen:  python3 gen_sprache.py
"""
import os, random
here = os.path.dirname(os.path.abspath(__file__))


def lies_vokabeln():
    lv, cur, thema = {}, None, None
    for raw in open(os.path.join(here, 'vokabeln.txt'), encoding='utf-8'):
        s = raw.strip()
        if not s:
            continue
        if s.startswith('## '):
            cur = int(s[3:]); lv[cur] = []
        elif s.startswith('# ') and cur is not None:
            thema = s[2:]; lv[cur].append((thema, []))
        elif cur is not None and '|' in s:
            p = [x.strip() for x in s.split('|')]
            assert len(p) == 3, s
            lv[cur][-1][1].append(p)
    return lv


def lies_saetze(sp):
    out, cur = {}, None
    for raw in open(os.path.join(here, sp + '_saetze.txt'), encoding='utf-8'):
        s = raw.rstrip('\n')
        if s.startswith('## '):
            cur = int(s[3:]); out[cur] = []
        elif s.strip() and not s.startswith('#') and cur is not None:
            out[cur].append(s)
    return out


def baue(sp, name, col):
    lv, saetze = lies_vokabeln(), lies_saetze(sp)
    for l in sorted(lv):
        r = random.Random(100 * col + l)
        themen = lv[l]
        alle = [p for _, ps in themen for p in ps]
        for i in (0, col):
            assert len({p[i] for p in alle}) == len(alle), ('doppelt', sp, l, [p[i] for p in alle if [q[i] for q in alle].count(p[i]) > 1])
        extra = saetze.get(l, [])
        zu = []
        for thema, ps in themen:
            for k in range(0, len(ps) - 3, 4):
                zu.append('Z Ordne zu: %s (Teil %d). | %s' % (thema, k // 4 + 1, ' | '.join('%s = %s' % (p[0], p[col]) for p in ps[k:k + 4])))
        zu = zu[:10]
        vor = []
        rueck = []
        for thema, ps in themen:
            for p in ps:
                andere = [q for q in ps if q is not p]
                f = r.sample(andere, 3)
                vor.append('M Was heißt „%s“ auf %s? | %s | %s' % (p[0], name, p[col], ' | '.join(q[col] for q in f)))
                f = r.sample(andere, 3)
                rueck.append('M Was bedeutet „%s“? | %s | %s' % (p[col], p[0], ' | '.join(q[0] for q in f)))
        n_rueck = 100 - len(extra) - len(zu) - len(vor)
        assert 0 <= n_rueck <= len(rueck), (sp, l, len(extra), len(zu), len(vor))
        schritt = len(rueck) / n_rueck if n_rueck else 1
        rueck = [rueck[int(i * schritt)] for i in range(n_rueck)]
        out = ['# %s Level %d – erzeugt von gen_sprache.py aus vokabeln.txt und %s_saetze.txt' % (name, l + 1, sp),
               '# --- Sätze und Wendungen'] + extra + ['# --- Deutsch → %s' % name] + vor + ['# --- %s → Deutsch' % name] + rueck + ['# --- Zuordnen'] + zu
        assert sum(1 for x in out if not x.startswith('#')) == 100
        open(os.path.join(here, '%s_%d.txt' % (sp, l)), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
        print('%s_%d.txt' % (sp, l), 'Sätze', len(extra), 'vor', len(vor), 'rück', n_rueck, 'zuordnen', len(zu))


if __name__ == '__main__':
    baue('it', 'Italienisch', 1)
    baue('en', 'Englisch', 2)
