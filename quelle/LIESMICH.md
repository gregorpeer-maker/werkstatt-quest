# Quelldateien von Werkstatt-Quest

- `werkstatt-quest.html`: das Spiel (eine Datei).
- `fragen/`: alle Fragen als Textdateien, je Level eine Datei mit 100 Fragen.
- `build.py`: setzt die Fragen ins Spiel ein und erzeugt die App-Fassung.

Neu bauen (im Hauptordner des Repositorys):

```bash
python3 quelle/build.py .
```

## Fragen-Dateien

| Dateien | Fach | Entstehung |
|---|---|---|
| `kfz_lf1.txt` … `kfz_lf8.txt` | KFZ-Technik, je Lernfeld | von Hand geschrieben, direkt bearbeiten |
| `fr_0.txt` … `fr_4.txt` | Fachrechnen | erzeugt von `gen_fr.py` (Vorlagen mit wechselnden Zahlen) |
| `et_0.txt` … `et_4.txt` | Elektrotechnik | erzeugt von `gen_et.py`: Theorie aus `et_<n>_theorie.txt`, dazu Rechenaufgaben |
| `it_*.txt`, `en_*.txt` | Italienisch, Englisch | erzeugt von `gen_sprache.py` aus `vokabeln.txt` und `it_saetze.txt` / `en_saetze.txt` |
| `edv_0.txt` … `edv_4.txt` | EDV | erzeugt von `gen_edv.py`: Begriffslisten im Skript, dazu `edv_<n>_extra.txt` |

Erzeugte Dateien nicht direkt ändern, sondern die Quelle (Theorie-, Satz-, Extra-Datei, `vokabeln.txt` oder das Skript) und danach neu erzeugen:

```bash
cd quelle/fragen
python3 gen_fr.py
python3 gen_et.py
python3 gen_sprache.py
python3 gen_edv.py
python3 pruefen.py
```

`pruefen.py` zählt die Fragen je Datei und meldet Formatfehler und doppelte Fragen.

## Format einer Fragenzeile

```
M Frage | richtige Antwort | falsch | falsch | falsch || Erklärung >> Tipp
R Aussage, die richtig ist || Erklärung
F Aussage, die falsch ist || Erklärung
N Rechenfrage | Ergebnis | Einheit | erlaubte Abweichung || Lösungsweg >> Tipp
Z Zuordnen | links = rechts | links = rechts | links = rechts
```
