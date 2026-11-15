#!/usr/bin/env python3
"""Erzeugt edv_0.txt bis edv_4.txt (je 100 Fragen) aus Begriffslisten, Tabellen und den
handgeschriebenen Fragen in edv_<n>_extra.txt.  Neu erzeugen:  python3 gen_edv.py

Falsche Antworten stammen aus derselben Liste (andere Begriffe, andere Tastenkombinationen),
damit sie nicht offensichtlich sind.
"""
import os, random
from gen_fr import N, z

here = os.path.dirname(os.path.abspath(__file__))

# Begriff | Erklärung   (je Level)
GLOSSAR = {
0: """
Hardware | Alle Teile eines Computers, die man anfassen kann
Software | Programme und Daten, die auf dem Computer laufen
Betriebssystem | Grundprogramm, das den Computer steuert und andere Programme startet
Browser | Programm zum Anzeigen von Internetseiten
Ordner | Behälter, in dem Dateien und weitere Ordner abgelegt werden
Datei | Gespeicherte Einheit von Daten mit Namen und Endung
Dateiendung | Kürzel hinter dem Punkt, das den Dateityp angibt
Arbeitsspeicher (RAM) | Schneller Speicher, dessen Inhalt beim Ausschalten verloren geht
Festplatte oder SSD | Dauerhafter Speicher für Programme und Dateien
Prozessor (CPU) | Baustein, der die Befehle der Programme ausführt
USB-Stick | Kleiner, steckbarer Datenträger zum Mitnehmen
Cloud | Speicherplatz auf Servern im Internet
Download | Daten aus dem Internet auf das eigene Gerät laden
Upload | Daten vom eigenen Gerät ins Internet übertragen
WLAN | Funkverbindung zum lokalen Netzwerk
Passwort | Geheime Zeichenfolge zum Schutz eines Zugangs
Schadsoftware | Programm, das Daten ausspäht, verschlüsselt oder zerstört
Update | Neuere Version, die Fehler behebt und Sicherheitslücken schließt
Backup | Sicherungskopie von Daten auf einem zweiten Datenträger
Papierkorb | Ablage für gelöschte Dateien, aus der sie wiederhergestellt werden können
Desktop | Arbeitsfläche, die nach dem Anmelden auf dem Bildschirm erscheint
Taskleiste | Leiste mit Startmenü und den geöffneten Programmen
E-Mail-Anhang | Datei, die zusammen mit einer E-Mail verschickt wird
Link | Verweis, der beim Anklicken eine Seite oder Datei öffnet
""",
1: """
Schriftart | Aussehen der Buchstaben, zum Beispiel Arial oder Calibri
Schriftgrad | Größe der Schrift, angegeben in Punkt
Absatz | Textabschnitt, der mit der Eingabetaste beendet wird
Zeilenabstand | Abstand zwischen den Zeilen innerhalb eines Absatzes
Einzug | Abstand eines Absatzes vom linken oder rechten Seitenrand
Tabstopp | Feste Position, an die der Cursor mit der Tabulatortaste springt
Blocksatz | Ausrichtung, bei der alle Zeilen links und rechts bündig abschließen
Zentriert | Ausrichtung, bei der jede Zeile mittig zwischen den Rändern steht
Linksbündig | Ausrichtung, bei der die Zeilen am linken Rand beginnen und rechts flattern
Aufzählung | Liste, deren Einträge mit einem Punkt oder Zeichen beginnen
Nummerierung | Liste, deren Einträge fortlaufende Zahlen tragen
Seitenrand | Freier Bereich zwischen Text und Blattkante
Formatierungszeichen | Sichtbar gemachte Leerzeichen, Tabulatoren und Absatzmarken
Silbentrennung | Automatisches Trennen langer Wörter am Zeilenende
Rechtschreibprüfung | Funktion, die falsch geschriebene Wörter rot unterstreicht
Zwischenablage | Speicher, in dem Kopiertes bis zum Einfügen liegt
Format übertragen | Pinsel, der die Formatierung auf anderen Text kopiert
Seitenumbruch | Befehl, der den folgenden Text auf einer neuen Seite beginnen lässt
Geschütztes Leerzeichen | Leerzeichen, an dem die Zeile nicht umbrochen wird
Druckvorschau | Anzeige, wie das Dokument auf Papier aussehen wird
""",
2: """
Tabelle | Raster aus Zeilen und Spalten für geordnete Angaben
Tabellenzelle | Einzelnes Feld einer Tabelle
Zellen verbinden | Mehrere Felder einer Tabelle zu einem zusammenfassen
Kopfzeile | Bereich am oberen Seitenrand, der auf jeder Seite wiederholt wird
Fußzeile | Bereich am unteren Seitenrand, der auf jeder Seite wiederholt wird
Seitenzahl | Feld, das die Nummer der jeweiligen Seite automatisch anzeigt
Formatvorlage | Gespeicherte Kombination von Formatierungen mit einem Namen
Dokumentvorlage | Muster, aus dem neue Dokumente mit gleichem Aufbau entstehen
Inhaltsverzeichnis | Automatisch erzeugte Liste der Überschriften mit Seitenzahlen
Serienbrief | Dokument, das mit Daten aus einer Liste für viele Empfänger erstellt wird
Datenquelle | Liste mit den Adressen und Angaben für einen Serienbrief
Seriendruckfeld | Platzhalter, der beim Seriendruck durch einen Wert ersetzt wird
Textfeld | Frei verschiebbarer Rahmen mit Text
Textumbruch | Einstellung, wie Text um ein Bild herumfließt
Abschnittswechsel | Trennung, nach der andere Seiteneinstellungen gelten können
Querformat | Ausrichtung, bei der das Blatt breiter als hoch ist
Hochformat | Ausrichtung, bei der das Blatt höher als breit ist
Fußnote | Anmerkung am Seitenende, auf die eine hochgestellte Zahl verweist
PDF | Dateiformat, das auf jedem Gerät gleich aussieht und sich kaum ändern lässt
Anschriftfeld | Bereich im Geschäftsbrief für die Adresse des Empfängers
Betreffzeile | Kurze Angabe, worum es in einem Brief geht
Bezugszeichenzeile | Zeile im Geschäftsbrief mit Zeichen, Datum und Ansprechpartner
Grußformel | Abschluss eines Briefs vor der Unterschrift
Anlagenvermerk | Hinweis am Briefende auf beigelegte Unterlagen
Formularfeld | Feld, in das der Benutzer später etwas einträgt oder ankreuzt
Wasserzeichen | Blasser Schriftzug oder Bild hinter dem Text
Kommentar | Anmerkung am Rand, die nicht zum Text gehört
Änderungen nachverfolgen | Funktion, die jede Bearbeitung sichtbar markiert
""",
3: """
Arbeitsmappe | Excel-Datei, die ein oder mehrere Tabellenblätter enthält
Tabellenblatt | Einzelne Tabelle innerhalb einer Excel-Datei
Zelle | Schnittpunkt von Spalte und Zeile, zum Beispiel B3
Zellbezug | Angabe in einer Formel, aus welcher Zelle der Wert stammt
Relativer Bezug | Bezug, der sich beim Kopieren der Formel mitverschiebt
Absoluter Bezug | Bezug mit Dollarzeichen, der beim Kopieren gleich bleibt
Formel | Rechenanweisung, die mit einem Gleichheitszeichen beginnt
Funktion | Vorgefertigte Rechenanweisung mit Namen, zum Beispiel SUMME
Bereich | Mehrere zusammenhängende Zellen, zum Beispiel A1:A10
Ausfüllkästchen | Kleines Quadrat an der Zellecke zum Kopieren und Fortsetzen von Reihen
Zahlenformat | Einstellung, wie ein Wert angezeigt wird, zum Beispiel als Währung
Bedingte Formatierung | Formatierung, die sich nach dem Zellinhalt richtet
Filter | Funktion, die nur Zeilen mit bestimmten Werten anzeigt
Sortieren | Zeilen nach den Werten einer Spalte ordnen
Diagramm | Grafische Darstellung von Zahlen aus der Tabelle
Bearbeitungsleiste | Zeile über der Tabelle, die den Inhalt der aktiven Zelle zeigt
Namenfeld | Feld links oben, das die Adresse der aktiven Zelle zeigt
Fixieren | Zeilen oder Spalten beim Scrollen sichtbar halten
""",
4: """
Diagnosetester | Gerät oder Programm, das Steuergeräte ausliest und ansteuert
Diagnosesteckdose (OBD) | Genormter 16-poliger Anschluss für den Tester im Fahrzeug
Pass-Thru | Zugang zur Herstellersoftware über eine genormte Schnittstelle
Software-Update (Flashen) | Aufspielen einer neuen Programmversion auf ein Steuergerät
Codierung | Anpassen eines Steuergeräts an die Ausstattung des Fahrzeugs
Fahrgestellnummer (FIN) | 17-stellige Nummer, die ein Fahrzeug eindeutig kennzeichnet
Elektronischer Teilekatalog | Programm, das passende Ersatzteile zum Fahrzeug anzeigt
Digitales Serviceheft | Online beim Hersteller gespeicherte Wartungsnachweise
Reparaturleitfaden | Anleitung des Herstellers mit Arbeitsschritten und Anzugsmomenten
Stromlaufplan | Zeichnung der elektrischen Verbindungen eines Systems
Arbeitswert | Zeitvorgabe des Herstellers für eine Arbeit
Werkstattauftrag | Dokument mit Kundendaten, Fahrzeugdaten und beauftragten Arbeiten
Dealer-Management-System | Programm für Aufträge, Rechnungen, Lager und Kundendaten des Betriebs
Diagnoseprotokoll | Ausdruck mit Fahrzeugdaten, Fehlercodes und Messwerten
Fernwartung | Zugriff eines Spezialisten auf den Tester über das Internet
Datenschutz | Schutz personenbezogener Daten vor Missbrauch
Personenbezogene Daten | Angaben, die sich einer bestimmten Person zuordnen lassen
Einwilligung | Zustimmung einer Person zur Verarbeitung ihrer Daten
Datensicherung | Regelmäßiges Kopieren der Betriebsdaten auf einen getrennten Speicher
Verschlüsselung | Verfahren, das Daten für Unbefugte unlesbar macht
Zwei-Faktor-Anmeldung | Anmeldung mit Passwort und einem zweiten Nachweis, etwa einem Code
Phishing | Gefälschte Nachricht, die Zugangsdaten erschleichen soll
Firewall | Schutz, der unerwünschte Verbindungen aus dem Netz blockiert
Virenschutz | Programm, das Schadsoftware erkennt und entfernt
Benutzerkonto | Persönlicher Zugang mit eigenen Rechten und eigenem Passwort
Administrator | Benutzer mit dem Recht, Programme zu installieren und Einstellungen zu ändern
Netzwerk | Verbindung mehrerer Geräte zum Austausch von Daten
Router | Gerät, das das lokale Netz mit dem Internet verbindet
Server | Rechner, der Daten oder Dienste für andere Geräte bereitstellt
IP-Adresse | Nummer, über die ein Gerät im Netzwerk erreichbar ist
Lizenz | Erlaubnis, eine Software zu nutzen
Online-Freischaltung | Bestätigung einer geschützten Funktion über den Server des Herstellers
QR-Code | Quadratisches Muster, das eine Adresse oder einen Text für die Kamera enthält
Präsentation | Folge von Folien, die einem Publikum gezeigt wird
Signatur (E-Mail) | Textblock mit Name und Kontaktdaten am Ende einer Nachricht
Blindkopie (BCC) | Empfänger, den die anderen Empfänger nicht sehen
Tabellenkalkulation | Programm zum Rechnen mit Zahlen in Zeilen und Spalten
Datenbank | Geordnete Sammlung von Datensätzen, die sich durchsuchen lässt
""",
}

KURZ_BASIS = [('Markiertes kopieren', 'Strg + C'), ('Kopiertes einfügen', 'Strg + V'), ('Markiertes ausschneiden', 'Strg + X'), ('Letzten Schritt rückgängig machen', 'Strg + Z'),
              ('Alles markieren', 'Strg + A'), ('Speichern', 'Strg + S'), ('Drucken', 'Strg + P'), ('Suchen', 'Strg + F'), ('Neues Dokument anlegen', 'Strg + N'),
              ('Datei öffnen', 'Strg + O'), ('Aktives Fenster schließen', 'Alt + F4'), ('Zwischen geöffneten Fenstern wechseln', 'Alt + Tab')]
KURZ_WORD = [('Text fett setzen', 'Strg + Umschalt + F'), ('Text kursiv setzen', 'Strg + Umschalt + K'), ('Text unterstreichen', 'Strg + Umschalt + U'), ('Absatz zentrieren', 'Strg + E'),
             ('Absatz linksbündig ausrichten', 'Strg + L'), ('Absatz rechtsbündig ausrichten', 'Strg + R'), ('Absatz im Blocksatz ausrichten', 'Strg + B'), ('Letzten Schritt wiederholen', 'Strg + Y'),
             ('Seitenumbruch einfügen', 'Strg + Eingabe'), ('Suchen und Ersetzen öffnen', 'Strg + H'), ('Speichern unter öffnen', 'F12'), ('Rechtschreibprüfung starten', 'F7'),
             ('Neue Zeile ohne neuen Absatz', 'Umschalt + Eingabe'), ('Zum Anfang des Dokuments springen', 'Strg + Pos1'), ('Zum Ende des Dokuments springen', 'Strg + Ende')]
REGISTER = ['Datei', 'Start', 'Einfügen', 'Entwurf', 'Layout', 'Referenzen', 'Sendungen', 'Überprüfen', 'Ansicht']
MENUE1 = [('Schriftart und Schriftgrad', 'Start'), ('Aufzählungszeichen', 'Start'), ('Formatvorlagen', 'Start'), ('Bild einfügen', 'Einfügen'), ('Symbol einfügen', 'Einfügen'),
          ('Seitenränder', 'Layout'), ('Hoch- oder Querformat', 'Layout'), ('Rechtschreibung und Grammatik', 'Überprüfen'), ('Lineal einblenden', 'Ansicht'), ('Drucken', 'Datei')]
MENUE2 = [('Tabelle einfügen', 'Einfügen'), ('Kopf- und Fußzeile', 'Einfügen'), ('Seitenzahl', 'Einfügen'), ('Textfeld', 'Einfügen'), ('Spalten', 'Layout'), ('Abschnittswechsel (Umbrüche)', 'Layout'),
          ('Inhaltsverzeichnis', 'Referenzen'), ('Fußnote einfügen', 'Referenzen'), ('Seriendruck starten', 'Sendungen'), ('Kommentar einfügen', 'Überprüfen'), ('Änderungen nachverfolgen', 'Überprüfen'),
          ('Wasserzeichen', 'Entwurf'), ('Als PDF exportieren', 'Datei')]
DATEITYP = [('ein Word-Dokument', '.docx'), ('eine Excel-Arbeitsmappe', '.xlsx'), ('eine PowerPoint-Präsentation', '.pptx'), ('ein PDF-Dokument', '.pdf'), ('ein Foto', '.jpg'),
            ('ein Bild mit durchsichtigem Hintergrund', '.png'), ('eine Musikdatei', '.mp3'), ('ein Video', '.mp4'), ('ein gepacktes Archiv', '.zip'), ('eine reine Textdatei', '.txt'),
            ('ein ausführbares Windows-Programm', '.exe'), ('eine Tabelle mit Trennzeichen', '.csv')]
EXCELFUNK = [('addiert alle Zahlen eines Bereichs', 'SUMME'), ('berechnet den Durchschnitt', 'MITTELWERT'), ('liefert den größten Wert', 'MAX'), ('liefert den kleinsten Wert', 'MIN'),
             ('zählt die Zellen, die Zahlen enthalten', 'ANZAHL'), ('zählt alle nicht leeren Zellen', 'ANZAHL2'), ('gibt je nach Bedingung einen von zwei Werten aus', 'WENN'),
             ('rundet auf eine angegebene Stellenzahl', 'RUNDEN'), ('liefert das aktuelle Datum', 'HEUTE'), ('sucht einen Wert in der ersten Spalte und gibt einen Wert derselben Zeile zurück', 'SVERWEIS'),
             ('zählt die Zellen, die eine Bedingung erfüllen', 'ZÄHLENWENN'), ('addiert nur die Zahlen, die eine Bedingung erfüllen', 'SUMMEWENN')]
EXCELFEHLER = [('#DIV/0!', 'Es wird durch null oder eine leere Zelle geteilt'), ('#NAME?', 'Excel kennt den Namen der Funktion nicht, meist ein Tippfehler'), ('#WERT!', 'Die Formel rechnet mit Text statt mit einer Zahl'),
               ('#BEZUG!', 'Die Formel verweist auf eine gelöschte Zelle'), ('#####', 'Die Spalte ist zu schmal für den Wert'), ('#NV', 'Der gesuchte Wert wurde nicht gefunden')]


def paare(txt):
    out = []
    for s in txt.strip().split('\n'):
        a, b = [x.strip() for x in s.split('|')]
        out.append((a, b))
    return out


def mc(r, frage, richtig, pool):
    f = r.sample([x for x in pool if x != richtig], 3)
    return 'M %s | %s | %s' % (frage, richtig, ' | '.join(f))


def glossar(r, l):
    g = paare(GLOSSAR[l])
    assert len({a for a, _ in g}) == len(g) and len({b for _, b in g}) == len(g)
    out = ['# --- Begriffe']
    for a, b in g:
        out.append(mc(r, 'Was ist bzw. bedeutet „%s“?' % a, b, [y for _, y in g]))
    out.append('# --- Begriffe erkennen')
    for a, b in g:
        out.append(mc(r, 'Welcher Begriff passt zu dieser Beschreibung? „%s“' % b, a, [x for x, _ in g]))
    return out


def kurz(r, liste, rueck=True):
    out = ['# --- Tastenkombinationen']
    for a, b in liste:
        out.append(mc(r, 'Mit welcher Tastenkombination kannst du: %s?' % a, b, [y for _, y in liste]))
    if rueck:
        for a, b in liste:
            out.append(mc(r, 'Was bewirkt in Word die Tastenkombination %s?' % b, a, [x for x, _ in liste]))
    return out


def menue(r, liste):
    out = ['# --- Menüband']
    for a, b in liste:
        out.append(mc(r, 'In welchem Register von Word findest du: %s?' % a, b, REGISTER))
    return out


def einheiten(r):
    out, seen = ['# --- Speichergrößen'], set()
    def add(line):
        k = line.split('|')[0]
        if k not in seen:
            seen.add(k); out.append(line)
    for v in (2, 16, 0.5, 250):
        add(N('Wie viele Megabyte (MB) sind %s Gigabyte (GB)? Rechne mit 1 GB = 1000 MB.' % z(v), v * 1000, 'MB', '1 GB = 1000 MB', 'Mal 1000'))
    for v in (4500, 750, 32000):
        add(N('Wie viele Gigabyte (GB) sind %s Megabyte (MB)? Rechne mit 1000 MB = 1 GB.' % z(v), v / 1000, 'GB', '1000 MB = 1 GB', 'Durch 1000', 2, 0))
    for v in (3, 12):
        add(N('Wie viele Bit sind %d Byte?' % v, v * 8, 'Bit', '1 Byte = 8 Bit', 'Mal 8'))
    for g, m in ((32, 4), (64, 8), (16, 5)):
        add(N('Ein USB-Stick hat %d GB frei. Ein Foto braucht %d MB. Wie viele Fotos passen darauf? Rechne mit 1 GB = 1000 MB.' % (g, m), g * 1000 / m, 'Fotos', '%d GB = %d MB, geteilt durch %d MB' % (g, g * 1000, m), 'Zuerst GB in MB umrechnen.'))
    for g, t in ((2, 4), (1.5, 3)):
        add(N('Wie viele Terabyte (TB) Speicher braucht man für %d Sicherungen zu je %s TB?' % (t, z(g)), g * t, 'TB', 'Anzahl mal Größe', 'Malnehmen', 1, 0))
    return out


def excelrechnen(r):
    out, seen = ['# --- Was zeigt die Zelle an?'], set()
    def add(line):
        k = line.split('|')[0]
        if k not in seen:
            seen.add(k); out.append(line)
    def vals(n):
        return [r.choice([4, 6, 8, 10, 12, 15, 20, 25, 30, 50]) for _ in range(n)]
    for _ in range(3):
        a, b, c = vals(3)
        add(N('A1 = %d, B1 = %d, C1 = %d. Was zeigt die Zelle mit der Formel =A1+B1*C1 an?' % (a, b, c), a + b * c, '', 'Punkt vor Strich: zuerst B1*C1', 'Excel rechnet Punkt vor Strich.'))
        add(N('A1 = %d, B1 = %d, C1 = %d. Was zeigt die Zelle mit der Formel =(A1+B1)*C1 an?' % (a, b, c), (a + b) * c, '', 'Zuerst die Klammer', 'Klammern werden zuerst gerechnet.'))
    for _ in range(3):
        v = vals(4)
        t = 'A1 = %d, A2 = %d, A3 = %d, A4 = %d.' % tuple(v)
        add(N('%s Was ergibt =SUMME(A1:A4)?' % t, sum(v), '', 'Alle vier Werte addieren', 'SUMME addiert den ganzen Bereich.'))
        add(N('%s Was ergibt =MITTELWERT(A1:A4)?' % t, sum(v) / 4, '', 'Summe geteilt durch 4', 'Summe durch Anzahl', 2, 0.01))
        add(N('%s Was ergibt =MAX(A1:A4)-MIN(A1:A4)?' % t, max(v) - min(v), '', 'Größter minus kleinster Wert', 'MAX liefert den größten, MIN den kleinsten Wert.'))
    for a in (200, 85, 1250):
        add(N('A1 = %d (Nettobetrag). Was ergibt =A1*1,22?' % a, a * 1.22, '', 'Netto mal 1,22 ergibt den Bruttobetrag mit 22 %% MwSt.' .replace('%%', '%'), 'Mal 1,22', 2, 0.01))
        add(N('A1 = %d. Was ergibt =A1*22%%?' % a, a * 0.22, '', '22 % sind 0,22', '22 % von A1', 2, 0.01))
    for a, nd in ((12.3456, 2), (7.849, 1), (199.5, 0)):
        add(N('A1 = %s. Was ergibt =RUNDEN(A1;%d)?' % (z(a), nd), round(a + 1e-9, nd), '', 'Auf %d Stellen nach dem Komma runden' % nd, 'Die zweite Angabe ist die Zahl der Nachkommastellen.', nd, 0))
    for a in (8, 15, 30):
        add(N('A1 = %d. Was ergibt =WENN(A1>10;A1*2;A1+5)?' % a, a * 2 if a > 10 else a + 5, '', 'Ist A1 größer als 10, gilt der erste Wert, sonst der zweite.', 'Zuerst prüfen, ob die Bedingung stimmt.'))
    for a, b in ((45, 60), (12, 48)):
        add(N('A1 = %d, B1 = %d. Die Zelle mit =A1/B1 ist als Prozent formatiert. Welche Zahl steht vor dem Prozentzeichen?' % (a, b), a / b * 100, '%', '%d : %d = %s' % (a, b, z(a / b)), 'Als Prozent wird der Wert mal 100 angezeigt.'))
    return out


def baue():
    titel = ['Grundstufe: Computer-Grundlagen', '1. Klasse KFZ: Word Grundlagen', '2. Klasse KFZ: Word für Auftrag und Brief', '3. Klasse KFZ: Excel', '4. Klasse KFZ: EDV in der Werkstatt']
    for l in range(5):
        r = random.Random(300 + l)
        out = glossar(r, l)
        if l == 0:
            out += kurz(r, KURZ_BASIS, False)
            out.append('# --- Dateitypen')
            for a, b in DATEITYP:
                out.append(mc(r, 'Welche Dateiendung hat üblicherweise %s?' % a, b, [y for _, y in DATEITYP]))
            for a, b in DATEITYP[:6]:
                out.append(mc(r, 'Was ist eine Datei mit der Endung %s üblicherweise?' % b, a[0].upper() + a[1:], [x[0].upper() + x[1:] for x, _ in DATEITYP]))
            out += einheiten(r)
        if l == 1:
            out += kurz(r, KURZ_WORD) + menue(r, MENUE1)
        if l == 2:
            out += menue(r, MENUE2)
        if l == 3:
            out.append('# --- Funktionen')
            for a, b in EXCELFUNK:
                out.append(mc(r, 'Welche Excel-Funktion %s?' % a, b, [y for _, y in EXCELFUNK]))
            for a, b in EXCELFUNK:
                out.append(mc(r, 'Was macht die Excel-Funktion %s?' % b, 'Sie ' + a, ['Sie ' + x for x, _ in EXCELFUNK]))
            out.append('# --- Fehlermeldungen')
            for a, b in EXCELFEHLER:
                out.append(mc(r, 'Was bedeutet die Anzeige %s in einer Excel-Zelle?' % a, b, [y for _, y in EXCELFEHLER]))
            out += excelrechnen(r)
        ep = os.path.join(here, 'edv_%d_extra.txt' % l)
        extra = [s.rstrip('\n') for s in open(ep, encoding='utf-8')] if os.path.exists(ep) else []
        n_gen = sum(1 for x in out if not x.startswith('#'))
        n_ex = sum(1 for x in extra if x.strip() and not x.startswith('#'))
        print('edv_%d: erzeugt %d + handgeschrieben %d = %d' % (l, n_gen, n_ex, n_gen + n_ex))
        open(os.path.join(here, 'edv_%d.txt' % l), 'w', encoding='utf-8').write('# EDV Level %d – %s\n# Erzeugt von gen_edv.py; handgeschriebene Fragen stehen in edv_%d_extra.txt.\n' % (l + 1, titel[l], l) + '\n'.join(extra + out) + '\n')


if __name__ == '__main__':
    baue()
