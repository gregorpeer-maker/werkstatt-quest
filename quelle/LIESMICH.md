# Quelldateien von Werkstatt-Quest

- `werkstatt-quest.html`: das Spiel (eine Datei).
- `fragen/kfz_lf1.txt` bis `kfz_lf8.txt`: die KFZ-Fragen, je Lernfeld eine Textdatei mit 100 Fragen.
- `fragen/pruefen.py`: prüft die Fragen-Dateien (Anzahl, Format, doppelte Fragen).
- `build.py`: setzt die Fragen ins Spiel ein und erzeugt die App-Fassung.

Neu bauen (im Hauptordner des Repositorys):

```bash
python3 quelle/build.py .
```

Format einer Fragenzeile:

```
M Frage | richtige Antwort | falsch | falsch | falsch || Erklärung >> Tipp
R Aussage, die richtig ist || Erklärung
F Aussage, die falsch ist || Erklärung
N Rechenfrage | Ergebnis | Einheit | erlaubte Abweichung || Lösungsweg >> Tipp
Z Zuordnen | links = rechts | links = rechts | links = rechts
```
