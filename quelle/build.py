#!/usr/bin/env python3
"""Baut Werkstatt-Quest: Fragen aus fragen/*.txt einsetzen, App-Fassung (index.html) erzeugen.

Aufruf:  python3 build.py [Zielordner für index.html und sw.js]
Quelle:  werkstatt-quest.html (Spiel) und fragen/kfz_lf*.txt (je Lernfeld eine Datei)
"""
import os, re, sys, json
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, 'fragen'))
import pruefen

qs = pruefen.load_all(os.path.join(here, 'fragen'))
src = os.path.join(here, 'werkstatt-quest.html')
s = open(src, encoding='utf-8').read()
a, b = s.index('/*FILE_Q_START*/'), s.index('/*FILE_Q_END*/')
s = s[:a] + '/*FILE_Q_START*/\nconst FILE_Q=' + json.dumps(qs, ensure_ascii=False, separators=(',', ':')) + ';\n' + s[b:]
open(src, 'w', encoding='utf-8').write(s)
print(len(qs), 'Fragen aus Dateien eingesetzt')

out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, 'app')
t = '<title>Werkstatt-Quest</title>'
assert s.count(t) == 1 and s.count('</body>') == 1
app = s.replace(t, t + '''
<meta name="description" content="Lernspiel für KFZ-Technik, Elektrotechnik und Fachrechnen">
<meta name="theme-color" content="#14181f">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon-192.png">
<link rel="apple-touch-icon" href="icon-192.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Werkstatt-Quest">''')
app = app.replace('</body>', '''<script>if('serviceWorker' in navigator)window.addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}));</script>
</body>''')
open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(app)
# Versionsnummer des Offline-Speichers hochzählen, damit Geräte die neue Fassung laden
swp = os.path.join(out, 'sw.js')
sw = open(swp, encoding='utf-8').read()
m = re.search(r"werkstatt-quest-v(\d+)", sw)
sw = sw.replace(m.group(0), 'werkstatt-quest-v%d' % (int(m.group(1)) + 1))
open(swp, 'w', encoding='utf-8').write(sw)
print('App-Fassung geschrieben nach', out, '·', re.search(r"werkstatt-quest-v\d+", sw).group(0))
