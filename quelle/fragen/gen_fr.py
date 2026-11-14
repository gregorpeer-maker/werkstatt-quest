#!/usr/bin/env python3
"""Erzeugt die Fachrechnen-Aufgaben fr_0.txt bis fr_4.txt (je 100 Aufgaben).

Die Aufgaben sind Vorlagen mit wechselnden Zahlen. Ergebnis, Lösungsweg und Tipp
werden ausgerechnet. Neu erzeugen:  python3 gen_fr.py
Themen nach Lehrstoffverteilung (FR · LJ 1 bis LJ 3), Level 5 ist Prüfungsvorbereitung.
"""
import math, os, random

PI = math.pi


def z(x, nd=None):
    """Zahl deutsch formatieren."""
    if nd is not None:
        x = round(x, nd)
    s = ('%.6f' % x).rstrip('0').rstrip('.')
    if s in ('-0', ''):
        s = '0'
    return s.replace('.', ',')


def N(text, ans, unit, weg, tipp, nd=None, tol=None):
    if nd is not None:
        ans = round(ans, nd)
    if tol is None:
        tol = 0 if nd in (None, 0) and abs(ans - round(ans)) < 1e-9 else 0.6 * 10 ** (-(nd or 0))
        if nd is None and abs(ans - round(ans)) > 1e-9:
            tol = 0
    return 'N %s | %s | %s | %s || %s >> %s' % (text, z(ans), unit, z(tol), weg, tipp)


def M(text, right, wrong, weg=''):
    assert len(wrong) == 3 and right not in wrong and len(set(wrong)) == 3, text
    return 'M %s | %s | %s%s' % (text, right, ' | '.join(wrong), (' || ' + weg) if weg else '')


class L:
    """Sammelt die Aufgaben eines Levels."""

    def __init__(self, seed):
        self.r = random.Random(seed)
        self.out, self.seen = [], set()

    def add(self, title, n, fn):
        self.out.append('# --- ' + title)
        k = tries = 0
        while k < n:
            tries += 1
            assert tries < 500, title
            line = fn(self.r)
            key = line.split('|')[0]
            if key in self.seen:
                continue
            self.seen.add(key)
            self.out.append(line)
            k += 1

    def count(self):
        return sum(1 for l in self.out if not l.startswith('#'))


def c(r, *vals):
    return r.choice(vals)


# ---------------------------------------------------------------- Level 1: Grundstufe
def level0():
    A = L(10)

    def add_dez(r):
        a, b, d = c(r, 12.5, 24.9, 37.4, 48.75, 59.9, 86.3), c(r, 7.8, 13.6, 19.95, 28.4, 34.5), c(r, 4.5, 9.9, 15.25, 22.8)
        return N('Drei Ersatzteile kosten %s €, %s € und %s €. Wie viel kosten sie zusammen?' % (z(a), z(b), z(d)), a + b + d, '€', 'Alle drei Beträge zusammenzählen.', 'Komma unter Komma schreiben.', 2)

    def sub_dez(r):
        a, b = c(r, 50, 100, 200), c(r, 23.4, 37.85, 46.9, 68.25, 81.6, 12.75)
        if b >= a:
            a = 100
        return N('Ein Kunde zahlt mit %s €. Die Rechnung beträgt %s €. Wie viel Wechselgeld bekommt er?' % (z(a), z(b)), a - b, '€', '%s € − %s €' % (z(a), z(b)), 'Gegebener Betrag minus Rechnungsbetrag', 2)

    def mul(r):
        n, p = c(r, 3, 4, 5, 6, 8, 12), c(r, 2.4, 3.75, 4.9, 6.5, 8.2, 11.5)
        return N('Eine Zündkerze kostet %s €. Was kosten %d Zündkerzen?' % (z(p), n), n * p, '€', '%d · %s €' % (n, z(p)), 'Stückzahl mal Stückpreis', 2)

    def div(r):
        n, t = c(r, 4, 5, 8, 10), c(r, 36, 48, 60, 84, 120, 150)
        return N('Ein Karton mit %d Ölfiltern kostet %s €. Was kostet ein Ölfilter?' % (n, z(t)), t / n, '€', '%s € : %d' % (z(t), n), 'Gesamtpreis durch Stückzahl', 2)

    def runden(r):
        x = c(r, 3.456, 12.874, 0.6749, 7.995, 45.123, 8.3651, 19.498, 2.0449)
        nd = c(r, 1, 2)
        return N('Runde %s auf %d Dezimalstelle%s.' % (z(x), nd, '' if nd == 1 else 'n'), round(x + 1e-9, nd), '', 'Die nächste Stelle entscheidet: ab 5 wird aufgerundet.', 'Schau auf die Stelle rechts daneben.', nd, 0)

    def laenge(r):
        k = c(r, 0, 1, 2, 3)
        if k == 0:
            v = c(r, 1.2, 0.85, 2.45, 3.6, 0.07)
            return N('Rechne %s m in mm um.' % z(v), v * 1000, 'mm', '1 m = 1000 mm', 'Mal 1000')
        if k == 1:
            v = c(r, 450, 1250, 75, 2380, 60)
            return N('Rechne %s mm in m um.' % z(v), v / 1000, 'm', '1000 mm = 1 m', 'Durch 1000')
        if k == 2:
            v = c(r, 35, 120, 8.5, 250)
            return N('Rechne %s cm in mm um.' % z(v), v * 10, 'mm', '1 cm = 10 mm', 'Mal 10')
        v = c(r, 3.5, 12, 0.8, 45.6)
        return N('Rechne %s km in m um.' % z(v), v * 1000, 'm', '1 km = 1000 m', 'Mal 1000')

    def masse_vol(r):
        k = c(r, 0, 1, 2, 3)
        if k == 0:
            v = c(r, 2.5, 0.75, 4.2, 1.05)
            return N('Rechne %s Liter in ml um.' % z(v), v * 1000, 'ml', '1 l = 1000 ml', 'Mal 1000')
        if k == 1:
            v = c(r, 350, 1500, 250, 4750)
            return N('Rechne %s ml in Liter um.' % z(v), v / 1000, 'l', '1000 ml = 1 l', 'Durch 1000')
        if k == 2:
            v = c(r, 1.8, 0.45, 12.5, 3.25)
            return N('Rechne %s kg in g um.' % z(v), v * 1000, 'g', '1 kg = 1000 g', 'Mal 1000')
        v = c(r, 1.45, 0.9, 2.3, 16)
        return N('Rechne %s t in kg um.' % z(v), v * 1000, 'kg', '1 t = 1000 kg', 'Mal 1000')

    def zeit(r):
        k = c(r, 0, 1, 2)
        if k == 0:
            v = c(r, 1.5, 2.25, 0.75, 3.5, 0.2)
            return N('Wie viele Minuten sind %s Stunden?' % z(v), v * 60, 'min', '%s · 60 min' % z(v), '1 h = 60 min')
        if k == 1:
            v = c(r, 90, 45, 150, 210, 36)
            return N('Wie viele Stunden sind %d Minuten?' % v, v / 60, 'h', '%d min : 60' % v, '60 min = 1 h', 2)
        a, b = c(r, 7, 8), c(r, 15, 30, 45)
        d = c(r, 95, 140, 200, 255)
        return N('Eine Reparatur beginnt um %d:%02d Uhr und dauert %d Minuten. Wie viele Minuten nach %d:00 Uhr ist sie fertig?' % (a, b, d, a), b + d, 'min', '%d min + %d min' % (b, d), 'Startminute plus Dauer')

    def prozent(r):
        p, g = c(r, 10, 20, 25, 50, 5), c(r, 80, 120, 240, 60, 360, 150)
        return N('Wie viel sind %d %% von %s €?' % (p, z(g)), g * p / 100, '€', '%s € · %d / 100' % (z(g), p), 'Grundwert mal Prozentzahl durch 100', 2)

    def dreisatz(r):
        n1, p1, n2 = c(r, 2, 4, 5), c(r, 18, 30, 44, 56), c(r, 6, 8, 10, 12)
        return N('%d Liter Motoröl kosten %s €. Was kosten %d Liter?' % (n1, z(p1), n2), p1 / n1 * n2, '€', 'Ein Liter kostet %s €, mal %d' % (z(p1 / n1, 2), n2), 'Zuerst den Preis für 1 Liter ausrechnen.', 2)

    def rechteck(r):
        a, b = c(r, 4, 6, 8, 12, 15), c(r, 2.5, 3, 4.5, 5, 7.5)
        return N('Ein Werkstattboden ist %s m lang und %s m breit. Wie groß ist die Fläche?' % (z(a), z(b)), a * b, 'm²', 'A = Länge · Breite', 'Länge mal Breite', 2)

    def umfang(r):
        a, b = c(r, 4, 6, 8, 12), c(r, 2.5, 3, 4.5, 5)
        return N('Ein rechteckiges Blech ist %s m lang und %s m breit. Wie groß ist der Umfang?' % (z(a), z(b)), 2 * (a + b), 'm', 'U = 2 · (Länge + Breite)', 'Alle vier Seiten zusammenzählen.', 2)

    def schnitt(r):
        v = r.sample([28, 31, 32, 34, 35, 36, 38, 40, 42], 3)
        return N('Drei Reifen haben %d, %d und %d Zehntelmillimeter Profil mehr als das Minimum. Wie groß ist der Durchschnitt?' % tuple(v), sum(v) / 3, 'Zehntel-mm', 'Summe geteilt durch 3', 'Alle Werte zusammenzählen und durch die Anzahl teilen.', 1)

    def punkt(r):
        a, b, d = c(r, 12, 20, 36, 48), c(r, 4, 6, 8), c(r, 2, 3, 5)
        k = c(r, 0, 1)
        if k == 0:
            return N('Berechne: %d + %d · %d' % (a, b, d), a + b * d, '', 'Punkt vor Strich: zuerst %d · %d' % (b, d), 'Punktrechnung vor Strichrechnung')
        return N('Berechne: (%d + %d) · %d' % (a, b, d), (a + b) * d, '', 'Zuerst die Klammer: %d + %d' % (a, b), 'Klammer zuerst')

    def stunden(r):
        h, s = c(r, 1.5, 2, 2.5, 0.5, 3.5), c(r, 48, 56, 60, 64, 72)
        return N('Eine Werkstattstunde kostet %d €. Was kosten %s Stunden Arbeit?' % (s, z(h)), h * s, '€', '%s h · %d €/h' % (z(h), s), 'Stunden mal Stundensatz', 2)

    def einheit(r):
        k = c(r, 0, 1, 2)
        if k == 0:
            v = c(r, 1.5, 2.2, 0.75, 55, 110)
            return N('Rechne %s kW in W um.' % z(v), v * 1000, 'W', '1 kW = 1000 W', 'Mal 1000')
        if k == 1:
            v = c(r, 350, 20, 1500, 4.7)
            return N('Rechne %s mA in A um.' % z(v), v / 1000, 'A', '1000 mA = 1 A', 'Durch 1000', 4, 0)
        v = c(r, 2.2, 4.7, 10, 0.47)
        return N('Rechne %s kΩ in Ω um.' % z(v), v * 1000, 'Ω', '1 kΩ = 1000 Ω', 'Mal 1000')

    for t, n, f in [('Addieren und Subtrahieren mit Dezimalzahlen', 6, add_dez), ('Wechselgeld', 6, sub_dez), ('Multiplizieren', 7, mul), ('Dividieren', 7, div), ('Runden', 7, runden),
                    ('Längen umrechnen', 9, laenge), ('Volumen und Masse umrechnen', 9, masse_vol), ('Zeit umrechnen', 8, zeit), ('Elektrische Einheiten umrechnen', 7, einheit),
                    ('Prozent', 8, prozent), ('Dreisatz', 6, dreisatz), ('Fläche und Umfang', 5, rechteck), ('Umfang', 3, umfang), ('Rechenregeln', 6, punkt), ('Arbeitskosten', 4, stunden), ('Durchschnitt', 2, schnitt)]:
        A.add(t, n, f)
    return A


# ---------------------------------------------------------------- Level 2: 1. Klasse (FR · LJ 1)
def level1():
    A = L(11)

    def flaeche_um(r):
        k = c(r, 0, 1, 2)
        if k == 0:
            v = c(r, 2.5, 12, 0.8, 45)
            return N('Rechne %s cm² in mm² um.' % z(v), v * 100, 'mm²', '1 cm² = 100 mm²', 'Bei Flächen ist die Umrechnungszahl 100.')
        if k == 1:
            v = c(r, 1.6, 2, 0.45, 1.25)
            return N('Rechne %s Liter in cm³ um.' % z(v), v * 1000, 'cm³', '1 l = 1 dm³ = 1000 cm³', '1 Liter sind 1000 cm³.')
        v = c(r, 1998, 1598, 2496, 999)
        return N('Ein Motor hat %d cm³ Hubraum. Wie viele Liter sind das?' % v, v / 1000, 'l', '1000 cm³ = 1 l', 'Durch 1000', 3, 0.001)

    def bruch(r):
        k = c(r, 0, 1, 2)
        if k == 0:
            a, b = c(r, (1, 4), (3, 4), (1, 8), (3, 8), (5, 8), (1, 5), (2, 5))
            return N('Schreibe den Bruch %d/%d als Dezimalzahl.' % (a, b), a / b, '', '%d : %d' % (a, b), 'Zähler durch Nenner teilen.', 3, 0)
        if k == 1:
            a, b, d = c(r, (1, 2, 4), (3, 4, 8), (1, 4, 8), (1, 2, 8))
            return N('Berechne %d/%d + 1/%d als Dezimalzahl.' % (a, b, d), a / b + 1 / d, '', 'Auf den gemeinsamen Nenner %d bringen.' % d, 'Zuerst gleichnamig machen.', 3, 0)
        a, b, g = c(r, (3, 4, 60), (2, 5, 45), (1, 8, 64), (5, 8, 48), (2, 3, 54))
        return N('Ein Tank fasst %d Liter und ist zu %d/%d voll. Wie viele Liter sind im Tank?' % (g, a, b), g * a / b, 'l', '%d l · %d / %d' % (g, a, b), 'Durch den Nenner teilen, mit dem Zähler malnehmen.', 1)

    def dreisatz(r):
        k = c(r, 0, 1)
        if k == 0:
            l, km, km2 = c(r, 21, 28, 33, 39), c(r, 350, 420, 500, 600), c(r, 150, 250, 800)
            return N('Ein Auto verbraucht auf %d km genau %d Liter. Wie viele Liter braucht es bei gleichem Verbrauch für %d km?' % (km, l, km2), l / km * km2, 'l', '%d l : %d km · %d km' % (l, km, km2), 'Zuerst den Verbrauch für 1 km ausrechnen.', 1)
        a, t, b = c(r, 2, 3, 4), c(r, 6, 9, 12), c(r, 6, 8)
        return N('%d Mechaniker brauchen für eine Arbeit %d Stunden. Wie lange brauchen %d Mechaniker bei gleichem Tempo?' % (a, t, b), a * t / b, 'h', 'Umgekehrtes Verhältnis: %d · %d h : %d' % (a, t, b), 'Mehr Mechaniker brauchen weniger Zeit.', 2)

    def mischung(r):
        g, p = c(r, 5, 6, 8, 7.5, 10), c(r, 40, 50, 30, 35)
        return N('Ein Kühlsystem fasst %s Liter. Der Frostschutzanteil soll %d %% betragen. Wie viele Liter Frostschutz braucht man?' % (z(g), p), g * p / 100, 'l', '%s l · %d / 100' % (z(g), p), 'Gesamtmenge mal Anteil in Prozent', 2)

    def mischung2(r):
        a, b, f = c(r, (1, 1, 3), (1, 2, 2), (2, 3, 4), (1, 3, 1.5))
        return N('Frostschutz und Wasser werden im Verhältnis %d : %d gemischt. Wie viele Liter Wasser kommen auf %s Liter Frostschutz?' % (a, b, z(f)), f / a * b, 'l', '%s l : %d · %d' % (z(f), a, b), 'Ein Teil entspricht Frostschutzmenge durch %d.' % a, 2)

    def pz_teil(r):
        g, p = c(r, 85, 140, 260, 480, 1250), c(r, 22, 15, 8, 12.5, 3)
        return N('Wie viel sind %s %% von %s €?' % (z(p), z(g)), g * p / 100, '€', 'W = G · p / 100', 'Grundwert mal Prozentsatz durch 100', 2)

    def pz_satz(r):
        g, w = c(r, (80, 12), (250, 45), (1200, 150), (64, 16), (400, 28), (36, 27))
        return N('Von %d kontrollierten Fahrzeugen haben %d einen Mangel. Wie viel Prozent sind das?' % (g, w), w / g * 100, '%', 'p = W · 100 / G', 'Anteil durch Gesamtzahl mal 100', 2)

    def pz_grund(r):
        w, p = c(r, (44, 22), (36, 15), (18, 12), (75, 25), (9, 4.5))
        return N('%s € sind %s %% eines Betrags. Wie groß ist der ganze Betrag?' % (z(w), z(p)), w / p * 100, '€', 'G = W · 100 / p', 'Prozentwert durch Prozentsatz mal 100', 2)

    def mwst(r):
        n = c(r, 150, 240, 85, 420, 1200, 67.5)
        k = c(r, 0, 1)
        if k == 0:
            return N('Eine Rechnung beträgt netto %s €. Wie hoch ist der Bruttobetrag mit 22 %% MwSt.?' % z(n), n * 1.22, '€', 'Brutto = Netto · 1,22', 'Netto mal 1,22', 2)
        return N('Eine Rechnung beträgt brutto %s €. Wie hoch ist der Nettobetrag bei 22 %% MwSt.?' % z(n * 1.22, 2), n, '€', 'Netto = Brutto : 1,22', 'Brutto durch 1,22', 2)

    def rabatt(r):
        g, p = c(r, 180, 95, 320, 64, 540), c(r, 10, 15, 5, 20)
        return N('Ein Ersatzteil kostet %s €. Der Kunde bekommt %d %% Rabatt. Wie viel zahlt er?' % (z(g), p), g * (100 - p) / 100, '€', '%s € · %d / 100' % (z(g), 100 - p), 'Er zahlt %d %% des Preises.' % (100 - p), 2)

    def gleichung(r):
        k = c(r, 0, 1, 2, 3)
        if k == 0:
            a, b = c(r, 4, 6, 8, 12), c(r, 36, 48, 72, 96)
            return N('Löse nach x auf: %d · x = %d' % (a, b), b / a, '', 'x = %d : %d' % (b, a), 'Beide Seiten durch %d teilen.' % a, 2)
        if k == 1:
            a, b = c(r, 17, 28, 45), c(r, 63, 80, 112)
            return N('Löse nach x auf: x + %d = %d' % (a, b), b - a, '', 'x = %d − %d' % (b, a), 'Auf beiden Seiten %d abziehen.' % a)
        if k == 2:
            a, b = c(r, 3, 5, 8), c(r, 12, 15, 7.5)
            return N('Löse nach x auf: x : %d = %s' % (a, z(b)), a * b, '', 'x = %s · %d' % (z(b), a), 'Beide Seiten mit %d malnehmen.' % a, 2)
        a, b, d = c(r, 2, 3, 5), c(r, 4, 7, 10), c(r, 22, 34, 40)
        return N('Löse nach x auf: %d · x + %d = %d' % (a, b, d), (d - b) / a, '', 'x = (%d − %d) : %d' % (d, b, a), 'Zuerst %d abziehen, dann durch %d teilen.' % (b, a), 2)

    def formel(r):
        k = c(r, 0, 1, 2)
        if k == 0:
            return M('Stelle die Formel U = R · I nach I um.', 'I = U / R', ['I = U · R', 'I = R / U', 'I = U − R'])
        if k == 1:
            return M('Stelle die Formel v = s / t nach s um.', 's = v · t', ['s = v / t', 's = t / v', 's = v + t'])
        return M('Stelle die Formel p = F / A nach A um.', 'A = F / p', ['A = F · p', 'A = p / F', 'A = p − F'])

    def kreis_u(r):
        d = c(r, 60, 120, 250, 0.6, 35)
        e = 'm' if d < 1 else 'mm'
        return N('Eine Riemenscheibe hat %s %s Durchmesser. Wie groß ist ihr Umfang? (auf 1 Dezimale)' % (z(d), e), PI * d, e, 'U = π · d', 'Durchmesser mal π', 1 if d >= 1 else 2)

    def pyth(r):
        a, b = c(r, (3, 4), (6, 8), (5, 12), (9, 12), (8, 15), (30, 40))
        return N('Ein rechtwinkliges Dreieck hat die Katheten %d cm und %d cm. Wie lang ist die Hypotenuse?' % (a, b), math.hypot(a, b), 'cm', 'c = √(a² + b²)', 'Satz des Pythagoras: c² = a² + b²', 1)

    def fl_dreieck(r):
        g, h = c(r, 8, 12, 15, 24), c(r, 5, 6, 9, 10)
        return N('Ein dreieckiges Blech hat die Grundseite %d cm und die Höhe %d cm. Wie groß ist die Fläche?' % (g, h), g * h / 2, 'cm²', 'A = g · h / 2', 'Grundseite mal Höhe durch 2', 1)

    def fl_trapez(r):
        a, b, h = c(r, (10, 6, 4), (12, 8, 5), (20, 14, 6), (9, 5, 3))
        return N('Ein Trapez hat die parallelen Seiten %d cm und %d cm und die Höhe %d cm. Wie groß ist die Fläche?' % (a, b, h), (a + b) / 2 * h, 'cm²', 'A = (a + c) / 2 · h', 'Mittelwert der parallelen Seiten mal Höhe', 1)

    def fl_kreis(r):
        d = c(r, 8, 10, 7.5, 12, 6.5)
        return N('Ein Kolben hat %s cm Durchmesser. Wie groß ist die Kolbenfläche? (auf 1 Dezimale)' % z(d), PI / 4 * d * d, 'cm²', 'A = π / 4 · d²', 'A = 0,785 · d²', 1, 0.2)

    def fl_ring(r):
        D, d = c(r, (10, 6), (12, 8), (8, 5), (20, 16))
        return N('Eine Dichtscheibe hat außen %d cm und innen %d cm Durchmesser. Wie groß ist die Ringfläche? (auf 1 Dezimale)' % (D, d), PI / 4 * (D * D - d * d), 'cm²', 'A = π / 4 · (D² − d²)', 'Große Kreisfläche minus kleine Kreisfläche', 1, 0.2)

    def vol_quader(r):
        a, b, h = c(r, (40, 25, 20), (60, 30, 25), (50, 40, 30), (35, 20, 10))
        return N('Eine Ölwanne ist innen %d cm lang, %d cm breit und %d cm hoch. Wie viele Liter fasst sie?' % (a, b, h), a * b * h / 1000, 'l', 'V = l · b · h, dann cm³ durch 1000', '1000 cm³ sind 1 Liter.', 1)

    def vol_zyl(r):
        d, h = c(r, (8, 9), (10, 12), (7.5, 8), (20, 30), (6, 15))
        return N('Ein zylindrischer Behälter hat %s cm Durchmesser und %d cm Höhe. Wie groß ist das Volumen? (auf ganze cm³)' % (z(d), h), PI / 4 * d * d * h, 'cm³', 'V = π / 4 · d² · h', 'Grundfläche mal Höhe', 0, 2)

    def dichte(r):
        k = c(r, 0, 1)
        if k == 0:
            v, rho, name = c(r, (500, 7.85, 'Stahl'), (200, 2.7, 'Aluminium'), (120, 8.9, 'Kupfer'), (1000, 0.85, 'Dieselkraftstoff'))
            return N('Ein Körper aus %s hat ein Volumen von %d cm³. Die Dichte beträgt %s g/cm³. Wie groß ist die Masse in Gramm?' % (name, v, z(rho)), v * rho, 'g', 'm = V · ρ', 'Masse = Volumen mal Dichte', 0, 1)
        l, rho, name = c(r, (50, 0.75, 'Benzin'), (60, 0.84, 'Diesel'), (4.5, 0.88, 'Motoröl'), (40, 0.75, 'Benzin'))
        return N('Wie viel wiegen %s Liter %s mit der Dichte %s kg/l?' % (z(l), name, z(rho)), l * rho, 'kg', 'm = V · ρ', 'Liter mal Dichte', 2)

    def gewicht(r):
        m = c(r, 75, 1200, 1450, 180, 25)
        return N('Wie groß ist die Gewichtskraft einer Masse von %d kg? Rechne mit g = 9,81 m/s².' % m, m * 9.81, 'N', 'FG = m · g', 'Masse mal 9,81', 1, 1)

    for t, n, f in [('Flächen- und Volumeneinheiten', 6, flaeche_um), ('Bruchrechnen', 9, bruch), ('Dreisatz', 6, dreisatz), ('Mischungsrechnen', 4, mischung), ('Mischungsverhältnis', 3, mischung2),
                    ('Prozentwert', 5, pz_teil), ('Prozentsatz', 5, pz_satz), ('Grundwert', 4, pz_grund), ('Mehrwertsteuer', 6, mwst), ('Rabatt', 4, rabatt),
                    ('Gleichungen', 9, gleichung), ('Formeln umstellen', 3, formel), ('Kreisumfang', 4, kreis_u), ('Satz des Pythagoras', 5, pyth),
                    ('Dreieck', 3, fl_dreieck), ('Trapez', 3, fl_trapez), ('Kreisfläche', 4, fl_kreis), ('Kreisring', 3, fl_ring), ('Quader', 3, vol_quader), ('Zylinder', 4, vol_zyl), ('Dichte und Masse', 4, dichte), ('Gewichtskraft', 3, gewicht)]:
        A.add(t, n, f)
    return A


# ---------------------------------------------------------------- Level 3: 2. Klasse (FR · LJ 2)
def level2():
    A = L(12)

    def v_schnitt(r):
        s, t = c(r, (150, 2), (210, 3), (96, 1.5), (45, 0.75), (330, 4), (126, 1.75))
        return N('Ein Fahrzeug fährt %d km in %s Stunden. Wie hoch ist die Durchschnittsgeschwindigkeit?' % (s, z(t)), s / t, 'km/h', 'v = s / t', 'Weg durch Zeit', 1)

    def weg(r):
        v, t = c(r, (90, 2.5), (120, 1.5), (72, 0.5), (50, 0.2), (130, 3))
        return N('Ein Fahrzeug fährt %s Stunden lang mit %d km/h. Wie weit kommt es?' % (z(t), v), v * t, 'km', 's = v · t', 'Geschwindigkeit mal Zeit', 1)

    def kmh_ms(r):
        k = c(r, 0, 1)
        if k == 0:
            v = c(r, 36, 54, 72, 90, 108, 126, 144)
            return N('Rechne %d km/h in m/s um.' % v, v / 3.6, 'm/s', '%d : 3,6' % v, 'km/h durch 3,6', 1)
        v = c(r, 5, 12, 15, 25, 30, 35)
        return N('Rechne %d m/s in km/h um.' % v, v * 3.6, 'km/h', '%d · 3,6' % v, 'm/s mal 3,6', 1)

    def kolben(r):
        s, n = c(r, (80, 3000), (90, 6000), (86, 4500), (75, 2400), (92, 3600))
        return N('Ein Motor hat %d mm Hub und dreht mit %d 1/min. Wie groß ist die mittlere Kolbengeschwindigkeit? (auf 1 Dezimale)' % (s, n), 2 * s / 1000 * n / 60, 'm/s', 'vm = 2 · s · n = 2 · %s m · %s 1/s' % (z(s / 1000), z(n / 60)), 'Hub in m und Drehzahl in 1/s umrechnen, dann vm = 2 · s · n', 1, 0.1)

    def umfangsg(r):
        d, n = c(r, (120, 3000), (150, 2400), (200, 1500), (80, 6000), (250, 900))
        return N('Eine Riemenscheibe mit %d mm Durchmesser dreht mit %d 1/min. Wie groß ist die Umfangsgeschwindigkeit? (auf 1 Dezimale)' % (d, n), PI * d / 1000 * n / 60, 'm/s', 'v = π · d · n = π · %s m · %s 1/s' % (z(d / 1000), z(n / 60)), 'Durchmesser in m, Drehzahl in 1/s, dann v = π · d · n', 1, 0.1)

    def fahrg(r):
        d, n = c(r, (0.62, 600), (0.64, 900), (0.60, 750), (0.66, 480), (0.63, 1200))
        return N('Ein Rad hat einen Abrolldurchmesser von %s m und dreht mit %d 1/min. Wie schnell fährt das Fahrzeug in km/h? (auf ganze km/h)' % (z(d), n), PI * d * n / 60 * 3.6, 'km/h', 'v = π · d · n = π · %s m · %s 1/s, dann mal 3,6' % (z(d), z(n / 60)), 'Erst m/s ausrechnen, dann mal 3,6', 0, 1)

    def beschl(r):
        v, t = c(r, (100, 10), (100, 8), (72, 5), (54, 6), (108, 12), (90, 10))
        return N('Ein Auto beschleunigt in %d s von 0 auf %d km/h. Wie groß ist die mittlere Beschleunigung? (auf 2 Dezimalen)' % (t, v), v / 3.6 / t, 'm/s²', 'a = v / t = %s m/s : %d s' % (z(v / 3.6, 2), t), 'Geschwindigkeit zuerst in m/s umrechnen, dann a = v / t', 2, 0.02)

    def verz(r):
        v, t = c(r, (72, 4), (90, 5), (108, 6), (54, 3), (50.4, 2))
        return N('Ein Auto bremst in %d s von %s km/h bis zum Stillstand. Wie groß ist die Verzögerung?' % (t, z(v)), v / 3.6 / t, 'm/s²', 'a = v / t = %s m/s : %d s' % (z(v / 3.6, 2), t), 'Geschwindigkeit in m/s, dann durch die Bremszeit', 2, 0.02)

    def reakt(r):
        v, t = c(r, (50, 1), (90, 1), (72, 0.8), (108, 1), (130, 1.2), (36, 1))
        return N('Ein Fahrer fährt %d km/h und hat eine Reaktionszeit von %s s. Wie lang ist der Reaktionsweg? (auf 1 Dezimale)' % (v, z(t)), v / 3.6 * t, 'm', 'sR = v · tR = %s m/s · %s s' % (z(v / 3.6, 2), z(t)), 'Geschwindigkeit in m/s mal Reaktionszeit', 1, 0.1)

    def bremsweg(r):
        v, a = c(r, (72, 8), (90, 7), (108, 8), (54, 6), (50, 7.5), (126, 7))
        return N('Ein Auto bremst aus %d km/h mit einer Verzögerung von %s m/s². Wie lang ist der Bremsweg? (auf 1 Dezimale)' % (v, z(a)), (v / 3.6) ** 2 / (2 * a), 'm', 'sB = v² / (2 · a) mit v = %s m/s' % z(v / 3.6, 2), 'sB = v² / (2 · a), v in m/s', 1, 0.2)

    def anhalte(r):
        sr, sb = c(r, (15, 25), (25, 44.6), (20, 31.3), (27.8, 55.1), (12.5, 13.9))
        return N('Der Reaktionsweg beträgt %s m, der Bremsweg %s m. Wie lang ist der Anhalteweg?' % (z(sr), z(sb)), sr + sb, 'm', 'Anhalteweg = Reaktionsweg + Bremsweg', 'Beide Wege zusammenzählen.', 1)

    def kraft_res(r):
        k = c(r, 0, 1, 2)
        if k == 0:
            a, b = c(r, (300, 450), (120, 80), (1500, 700))
            return N('Zwei Kräfte von %d N und %d N wirken in dieselbe Richtung. Wie groß ist die Resultierende?' % (a, b), a + b, 'N', 'Gleiche Richtung: Kräfte addieren', 'Zusammenzählen')
        if k == 1:
            a, b = c(r, (800, 350), (500, 180), (1200, 900))
            return N('Zwei Kräfte von %d N und %d N wirken genau entgegengesetzt. Wie groß ist die Resultierende?' % (a, b), a - b, 'N', 'Entgegengesetzt: Kräfte abziehen', 'Größere minus kleinere Kraft')
        a, b = c(r, (300, 400), (600, 800), (500, 1200), (90, 120))
        return N('Zwei Kräfte von %d N und %d N wirken im rechten Winkel zueinander. Wie groß ist die Resultierende?' % (a, b), math.hypot(a, b), 'N', 'FR = √(F1² + F2²)', 'Kräfteparallelogramm mit rechtem Winkel: Satz des Pythagoras', 0, 1)

    def hebel(r):
        f1, l1, l2 = c(r, (200, 0.6, 0.15), (150, 0.8, 0.2), (400, 0.3, 0.1), (120, 1.0, 0.25), (250, 0.45, 0.09))
        return N('An einem Hebel wirkt eine Kraft von %d N am Hebelarm %s m. Welche Kraft entsteht am anderen Hebelarm von %s m?' % (f1, z(l1), z(l2)), f1 * l1 / l2, 'N', 'F1 · l1 = F2 · l2, also F2 = %d N · %s m : %s m' % (f1, z(l1), z(l2)), 'Hebelgesetz: Kraft mal Hebelarm ist auf beiden Seiten gleich.', 0, 1)

    def moment(r):
        k = c(r, 0, 1, 2)
        if k == 0:
            f, l = c(r, (120, 0.4), (250, 0.3), (90, 0.5), (300, 0.45))
            return N('An einem Schlüssel mit %s m Länge wirkt eine Kraft von %d N. Wie groß ist das Drehmoment?' % (z(l), f), f * l, 'Nm', 'M = F · r', 'Kraft mal Hebelarm', 1)
        if k == 1:
            m, l = c(r, (120, 0.4), (90, 0.3), (200, 0.5), (25, 0.2))
            return N('Eine Schraube soll mit %d Nm angezogen werden. Der Schlüssel ist %s m lang. Welche Kraft ist nötig?' % (m, z(l)), m / l, 'N', 'F = M / r', 'Drehmoment durch Hebelarm', 0, 1)
        f, d = c(r, (2000, 0.62), (1500, 0.6), (3200, 0.64), (2500, 0.66))
        return N('Am Radumfang wirkt eine Antriebskraft von %d N. Der Raddurchmesser beträgt %s m. Wie groß ist das Drehmoment am Rad?' % (f, z(d)), f * d / 2, 'Nm', 'M = F · r mit r = d / 2', 'Der Hebelarm ist der Radius, also der halbe Durchmesser.', 0, 1)

    def druck(r):
        k = c(r, 0, 1)
        if k == 0:
            f, a = c(r, (1000, 5), (2400, 8), (600, 2), (4500, 15), (900, 4.5))
            return N('Eine Kraft von %d N wirkt auf eine Kolbenfläche von %s cm². Wie groß ist der Druck in bar?' % (f, z(a)), f / a / 10, 'bar', 'p = F / A in N/cm², dann durch 10', '10 N/cm² sind 1 bar.', 1)
        p, a = c(r, (60, 4), (80, 5), (120, 3), (40, 12.5), (150, 2))
        return N('In einem Bremszylinder herrschen %d bar. Die Kolbenfläche beträgt %s cm². Welche Kraft übt der Kolben aus?' % (p, z(a)), p * 10 * a, 'N', 'F = p · A, mit 1 bar = 10 N/cm²', 'Druck in N/cm² umrechnen, dann mal Fläche', 0, 1)

    def pressung(r):
        f, a = c(r, (6000, 40), (4500, 30), (8000, 50), (3000, 24))
        return N('Ein Bremsbelag mit %d cm² Fläche wird mit %d N angepresst. Wie groß ist die Flächenpressung in N/cm²?' % (a, f), f / a, 'N/cm²', 'p = F / A', 'Kraft durch Fläche', 1)

    def hydr(r):
        f1, a1, a2 = c(r, (100, 2, 10), (300, 3, 12), (250, 2.5, 20), (500, 4, 18), (80, 1.5, 9))
        return N('Hydraulik: Am Geberkolben mit %s cm² wirken %d N. Wie groß ist die Kraft am Nehmerkolben mit %s cm²?' % (z(a1), f1, z(a2)), f1 * a2 / a1, 'N', 'F2 = F1 · A2 / A1', 'Der Druck ist überall gleich: F1 / A1 = F2 / A2', 0, 1)

    def luft(r):
        p = c(r, 2.2, 2.5, 3.0, 1.8)
        return N('Ein Reifen hat %s bar Überdruck. Wie groß ist der Absolutdruck bei 1 bar Luftdruck?' % z(p), p + 1, 'bar', 'pabs = pe + pamb', 'Überdruck plus Luftdruck', 1)

    for t, n, f in [('Durchschnittsgeschwindigkeit', 5, v_schnitt), ('Weg', 4, weg), ('km/h und m/s', 9, kmh_ms), ('Kolbengeschwindigkeit', 5, kolben), ('Umfangsgeschwindigkeit', 5, umfangsg), ('Fahrgeschwindigkeit', 5, fahrg),
                    ('Beschleunigung', 6, beschl), ('Verzögerung', 5, verz), ('Reaktionsweg', 6, reakt), ('Bremsweg', 6, bremsweg), ('Anhalteweg', 4, anhalte), ('Kräfte', 9, kraft_res),
                    ('Hebelgesetz', 5, hebel), ('Drehmoment', 9, moment), ('Druck', 8, druck), ('Flächenpressung', 3, pressung), ('Hydraulische Übersetzung', 4, hydr), ('Absolutdruck', 2, luft)]:
        A.add(t, n, f)
    return A


# ---------------------------------------------------------------- Level 4: 3. Klasse (FR · LJ 3)
def level3():
    A = L(13)

    def hub(r):
        d, s = c(r, (80, 90), (82, 92.8), (76, 86), (86, 86), (72, 82), (95, 87))
        return N('Bohrung d = %s mm, Hub s = %s mm. Wie groß ist der Hubraum eines Zylinders in cm³? (auf 1 Dezimale)' % (z(d), z(s)), PI / 4 * (d / 10) ** 2 * s / 10, 'cm³', 'Vh = π / 4 · d² · s = 0,7854 · (%s cm)² · %s cm' % (z(d / 10), z(s / 10)), 'In cm rechnen: Vh = π / 4 · d² · s', 1, 1)

    def gesamt(r):
        v, zz = c(r, (399.5, 4), (499.6, 4), (333, 3), (498, 6), (449.5, 4))
        return N('Ein Zylinder hat %s cm³ Hubraum, der Motor hat %d Zylinder. Wie groß ist der Gesamthubraum?' % (z(v), zz), v * zz, 'cm³', 'VH = Vh · z', 'Einzelhubraum mal Zylinderzahl', 1)

    def eps(r):
        vh, vc = c(r, (450, 50), (500, 50), (400, 40), (498, 31), (360, 40), (475, 25))
        return N('Hubraum Vh = %d cm³, Verdichtungsraum Vc = %d cm³. Wie groß ist das Verdichtungsverhältnis ε? (auf 1 Dezimale)' % (vh, vc), (vh + vc) / vc, '', 'ε = (Vh + Vc) / Vc', 'ε = (Vh + Vc) / Vc', 1, 0.1)

    def vc(r):
        vh, e = c(r, (450, 10), (500, 11), (400, 9), (490, 17), (360, 19))
        return N('Hubraum Vh = %d cm³, Verdichtungsverhältnis ε = %d. Wie groß ist der Verdichtungsraum? (auf 1 Dezimale)' % (vh, e), vh / (e - 1), 'cm³', 'Vc = Vh / (ε − 1)', 'Vc = Vh / (ε − 1)', 1, 0.2)

    def arbeit(r):
        f, s = c(r, (500, 12), (1200, 3), (800, 25), (15000, 0.5), (250, 40))
        return N('Eine Kraft von %d N verschiebt einen Körper um %s m. Wie groß ist die verrichtete Arbeit?' % (f, z(s)), f * s, 'Nm', 'W = F · s', 'Kraft mal Weg', 0)

    def leistung(r):
        w, t = c(r, (6000, 4), (30000, 12), (7500, 5), (120000, 60), (18000, 8))
        return N('In %d s wird eine Arbeit von %d Nm verrichtet. Wie groß ist die Leistung in Watt?' % (t, w), w / t, 'W', 'P = W / t', 'Arbeit durch Zeit', 0)

    def p_mn(r):
        m, n = c(r, (200, 3000), (150, 4200), (320, 1800), (250, 3600), (110, 6000), (400, 2400))
        return N('M = %d Nm bei n = %d 1/min. Wie groß ist die Leistung in kW? (auf 1 Dezimale)' % (m, n), 2 * PI * m * n / 60 / 1000, 'kW', 'P = 2 · π · M · n = 2 · π · %d Nm · %s 1/s' % (m, z(n / 60)), 'Drehzahl in 1/s, dann P = 2 · π · M · n, Ergebnis durch 1000', 1, 0.3)

    def m_pn(r):
        p, n = c(r, (75, 3000), (110, 4000), (55, 2500), (140, 3500), (90, 4500))
        return N('Ein Motor leistet %d kW bei %d 1/min. Wie groß ist das Drehmoment? (auf ganze Nm)' % (p, n), p * 1000 / (2 * PI * n / 60), 'Nm', 'M = P / (2 · π · n) mit n = %s 1/s' % z(n / 60, 2), 'M = P / (2 · π · n), Leistung in W und Drehzahl in 1/s', 0, 2)

    def eta(r):
        k = c(r, 0, 1)
        if k == 0:
            pz, pa = c(r, (80, 28), (120, 42), (60, 24), (200, 76), (95, 38))
            return N('Zugeführte Leistung %d kW, abgegebene Leistung %d kW. Wie groß ist der Wirkungsgrad in %%? (auf 1 Dezimale)' % (pz, pa), pa / pz * 100, '%', 'η = Pab / Pzu · 100 %', 'Abgegebene durch zugeführte Leistung', 1, 0.1)
        pm, e = c(r, (100, 92), (150, 90), (74, 88), (120, 85))
        return N('Ein Motor gibt %d kW ab. Der Wirkungsgrad der Kraftübertragung beträgt %d %%. Wie groß ist die Leistung an den Rädern? (auf 1 Dezimale)' % (pm, e), pm * e / 100, 'kW', 'PRad = PMotor · η', 'Motorleistung mal Wirkungsgrad', 1, 0.1)

    def ps(r):
        k = c(r, 0, 1)
        if k == 0:
            v = c(r, 66, 81, 110, 140, 85)
            return N('Rechne %d kW in PS um. (auf ganze PS)' % v, v * 1.36, 'PS', '1 kW = 1,36 PS', 'kW mal 1,36', 0, 1)
        v = c(r, 90, 150, 204, 75, 320)
        return N('Rechne %d PS in kW um. (auf ganze kW)' % v, v / 1.36, 'kW', '1 PS = 0,735 kW', 'PS durch 1,36', 0, 1)

    def reib(r):
        fn, mu, txt = c(r, (5000, 0.8, 'trockener Asphalt'), (4000, 0.5, 'nasser Asphalt'), (6000, 0.1, 'Eis'), (3600, 0.35, 'Bremsbelag auf Bremsscheibe'), (4500, 0.3, 'Schnee'))
        return N('Normalkraft %d N, Reibungszahl μ = %s (%s). Wie groß ist die Reibungskraft?' % (fn, z(mu), txt), fn * mu, 'N', 'FR = μ · FN', 'Reibungszahl mal Normalkraft', 0, 1)

    def reibl(r):
        fr, v = c(r, (400, 5), (250, 12), (1200, 2.5), (600, 8))
        return N('Eine Reibungskraft von %d N wirkt bei einer Gleitgeschwindigkeit von %s m/s. Wie groß ist die Reibungsleistung?' % (fr, z(v)), fr * v, 'W', 'PR = FR · v', 'Kraft mal Geschwindigkeit', 0, 1)

    def fma(r):
        m, a = c(r, (1200, 2.5), (1500, 7), (1000, 3.2), (1800, 8), (1350, 6))
        return N('Ein Fahrzeug mit %d kg wird mit %s m/s² verzögert. Wie groß ist die Bremskraft?' % (m, z(a)), m * a, 'N', 'F = m · a', 'Dynamisches Grundgesetz: Masse mal Beschleunigung', 0, 1)

    def ekin(r):
        m, v = c(r, (1200, 20), (1500, 30), (1000, 25), (1800, 15), (1400, 10))
        return N('Ein Fahrzeug mit %d kg fährt %d m/s. Wie groß ist die Bewegungsenergie in kJ?' % (m, v), m * v * v / 2 / 1000, 'kJ', 'Ekin = m · v² / 2, dann durch 1000', 'Ekin = m · v² / 2', 1, 0.5)

    def bremsarb(r):
        f, s = c(r, (9000, 40), (12000, 25), (7500, 60), (10500, 32))
        return N('Eine Bremskraft von %d N wirkt auf einem Bremsweg von %d m. Wie groß ist die Bremsarbeit in kJ?' % (f, s), f * s / 1000, 'kJ', 'W = F · s, dann durch 1000', 'Kraft mal Weg', 1)

    def igesamt(r):
        ig, ia = c(r, (3.5, 3.9), (1.9, 3.6), (1.0, 4.1), (0.8, 3.4), (2.1, 4.4), (1.3, 3.2))
        return N('Getriebeübersetzung %s, Achsübersetzung %s. Wie groß ist die Gesamtübersetzung? (auf 2 Dezimalen)' % (z(ig), z(ia)), ig * ia, '', 'iges = iG · iA', 'Einzelübersetzungen malnehmen', 2, 0.01)

    def nrad(r):
        n, i = c(r, (3000, 12), (4500, 9), (2400, 4), (6000, 15), (1800, 3.6))
        return N('Motordrehzahl %d 1/min, Gesamtübersetzung %s. Wie groß ist die Raddrehzahl?' % (n, z(i)), n / i, '1/min', 'nRad = nMotor / iges', 'Drehzahl durch Übersetzung', 0, 1)

    def mrad(r):
        m, i, e = c(r, (200, 12, 0.9), (150, 14, 0.92), (320, 8, 0.9), (250, 10, 0.88))
        return N('Motordrehmoment %d Nm, Gesamtübersetzung %s, Wirkungsgrad %s. Wie groß ist das Drehmoment an den Antriebsrädern?' % (m, z(i), z(e)), m * i * e, 'Nm', 'MRad = MMotor · iges · η', 'Drehmoment mal Übersetzung mal Wirkungsgrad', 0, 1)

    def fantrieb(r):
        m, rr = c(r, (2160, 0.3), (1800, 0.32), (2500, 0.31), (1500, 0.3), (2880, 0.32))
        return N('Das Drehmoment an den Antriebsrädern beträgt %d Nm, der Radhalbmesser %s m. Wie groß ist die Antriebskraft?' % (m, z(rr)), m / rr, 'N', 'F = M / r', 'Drehmoment durch Radhalbmesser', 0, 2)

    def pfahr(r):
        f, v = c(r, (600, 25), (900, 30), (450, 20), (1200, 36), (750, 27.8))
        return N('Die Summe der Fahrwiderstände beträgt %d N bei %s m/s. Welche Leistung ist an den Rädern nötig? (in kW, auf 1 Dezimale)' % (f, z(v)), f * v / 1000, 'kW', 'P = F · v, dann durch 1000', 'Kraft mal Geschwindigkeit', 1, 0.1)

    def hubl(r):
        p, v = c(r, (110, 1.968), (85, 1.598), (140, 1.984), (70, 0.999), (180, 2.979))
        return N('Ein Motor leistet %d kW bei %s Litern Hubraum. Wie groß ist die Hubraumleistung? (auf 1 Dezimale)' % (p, z(v)), p / v, 'kW/l', 'PH = P / VH', 'Leistung durch Hubraum in Litern', 1, 0.1)

    def lgew(r):
        m, p = c(r, (1400, 100), (1250, 81), (1800, 150), (1100, 55), (1650, 110))
        return N('Ein Fahrzeug wiegt %d kg und leistet %d kW. Wie groß ist das Leistungsgewicht? (auf 1 Dezimale)' % (m, p), m / p, 'kg/kW', 'Leistungsgewicht = Masse / Leistung', 'Masse durch Leistung', 1, 0.1)

    def verbrauch(r):
        l, km = c(r, (42, 600), (38.5, 550), (27, 450), (51, 680), (33, 750), (18.2, 280))
        return N('Ein Fahrzeug verbraucht %s Liter auf %d km. Wie hoch ist der Streckenverbrauch pro 100 km? (auf 1 Dezimale)' % (z(l), km), l / km * 100, 'l/100 km', 'Verbrauch = Liter / km · 100', 'Liter durch Kilometer mal 100', 1, 0.1)

    def spez(r):
        b, p = c(r, (22, 100), (15, 60), (30, 125), (12.6, 60), (18, 80))
        return N('Ein Motor verbraucht %s kg Kraftstoff pro Stunde bei %d kW. Wie groß ist der spezifische Verbrauch in g/kWh?' % (z(b), p), b * 1000 / p, 'g/kWh', 'be = B / P = %s g/h : %d kW' % (z(b * 1000), p), 'Verbrauch in g/h durch Leistung in kW', 0, 1)

    for t, n, f in [('Hubraum', 5, hub), ('Gesamthubraum', 4, gesamt), ('Verdichtungsverhältnis', 5, eps), ('Verdichtungsraum', 4, vc), ('Mechanische Arbeit', 4, arbeit), ('Leistung', 4, leistung),
                    ('Leistung aus Drehmoment und Drehzahl', 5, p_mn), ('Drehmoment aus Leistung', 4, m_pn), ('Wirkungsgrad', 6, eta), ('kW und PS', 4, ps), ('Reibungskraft', 4, reib), ('Reibungsleistung', 3, reibl),
                    ('Dynamisches Grundgesetz', 4, fma), ('Bewegungsenergie', 4, ekin), ('Bremsarbeit', 3, bremsarb), ('Gesamtübersetzung', 5, igesamt), ('Raddrehzahl', 4, nrad), ('Drehmoment am Rad', 3, mrad),
                    ('Antriebskraft', 4, fantrieb), ('Fahrwiderstandsleistung', 4, pfahr), ('Hubraumleistung', 4, hubl), ('Leistungsgewicht', 4, lgew), ('Streckenverbrauch', 5, verbrauch), ('Spezifischer Verbrauch', 4, spez)]:
        A.add(t, n, f)
    return A


# ---------------------------------------------------------------- Level 5: 4. Klasse (Prüfungsvorbereitung, Werkstattrechnen)
def level4():
    A = L(14)

    def rechnung(r):
        aw, satz, teile = c(r, (12, 6.5, 84), (18, 7, 126.5), (25, 6.8, 240), (8, 7.2, 39.9), (30, 6.5, 310))
        return N('Eine Reparatur umfasst %d Arbeitswerte zu je %s € und Teile für %s €. Wie hoch ist der Nettobetrag?' % (aw, z(satz), z(teile)), aw * satz + teile, '€', 'Arbeit: %d · %s €, dazu die Teile' % (aw, z(satz)), 'Arbeitswerte mal Preis, dann die Teile dazuzählen', 2, 0.01)

    def brutto(r):
        n = c(r, 185, 342.5, 96, 1280, 57.4, 760)
        return N('Der Nettobetrag einer Rechnung ist %s €. Wie hoch ist der Rechnungsbetrag mit 22 %% MwSt.?' % z(n), n * 1.22, '€', 'Brutto = Netto · 1,22', 'Netto mal 1,22', 2, 0.01)

    def mwstanteil(r):
        b = c(r, 244, 610, 122, 427, 1464)
        return N('Eine Rechnung beträgt brutto %d € mit 22 %% MwSt. Wie viel Euro Mehrwertsteuer sind enthalten?' % b, b - b / 1.22, '€', 'Netto = %d € : 1,22, MwSt. = Brutto − Netto' % b, 'Zuerst den Nettobetrag ausrechnen.', 2, 0.01)

    def skonto(r):
        b, p = c(r, (850, 2), (1240, 3), (460, 2), (2300, 3))
        return N('Eine Lieferantenrechnung über %d € wird mit %d %% Skonto bezahlt. Wie hoch ist der Zahlbetrag?' % (b, p), b * (100 - p) / 100, '€', '%d € · %d / 100' % (b, 100 - p), 'Es werden %d %% des Betrags bezahlt.' % (100 - p), 2, 0.01)

    def aufschlag(r):
        e, p = c(r, (40, 35), (120, 25), (18, 50), (260, 20), (75, 40))
        return N('Ein Ersatzteil kostet im Einkauf %d €. Die Werkstatt schlägt %d %% auf. Wie hoch ist der Verkaufspreis netto?' % (e, p), e * (100 + p) / 100, '€', '%d € · %s' % (e, z((100 + p) / 100)), 'Einkaufspreis mal (1 + Aufschlag)', 2, 0.01)

    def awzeit(r):
        aw, m = c(r, (24, 5), (15, 6), (36, 5), (50, 6), (9, 5))
        return N('Eine Arbeit ist mit %d Arbeitswerten zu je %d Minuten vorgegeben. Wie viele Stunden sind das?' % (aw, m), aw * m / 60, 'h', '%d · %d min = %d min, durch 60' % (aw, m, aw * m), 'Minuten ausrechnen und durch 60 teilen', 2, 0.01)

    def ohm(r):
        k = c(r, 0, 1, 2)
        if k == 0:
            u, rr = c(r, (12, 4), (12, 0.5), (13.8, 6), (5, 250), (24, 8))
            return N('An einem Widerstand von %s Ω liegen %s V an. Welcher Strom fließt? (auf 2 Dezimalen)' % (z(rr), z(u)), u / rr, 'A', 'I = U / R', 'I = U / R', 2, 0.01)
        if k == 1:
            u, i = c(r, (12, 5), (12, 0.25), (14, 20), (5, 0.02))
            return N('Bei %s V fließen %s A. Wie groß ist der Widerstand?' % (z(u), z(i)), u / i, 'Ω', 'R = U / I', 'R = U / I', 2, 0.01)
        rr, i = c(r, (4, 3), (0.05, 150), (120, 0.1), (2.4, 5))
        return N('Durch einen Widerstand von %s Ω fließen %s A. Wie groß ist die Spannung?' % (z(rr), z(i)), rr * i, 'V', 'U = R · I', 'U = R · I', 2, 0.01)

    def pel(r):
        k = c(r, 0, 1)
        if k == 0:
            u, p = c(r, (12, 55), (12, 21), (12, 120), (230, 2000), (400, 11000))
            return N('Ein Verbraucher hat %d W an %d V. Welcher Strom fließt? (auf 2 Dezimalen)' % (p, u), p / u, 'A', 'I = P / U', 'I = P / U', 2, 0.01)
        u, i = c(r, (12, 15), (13.5, 90), (400, 32), (230, 16))
        return N('Bei %s V fließen %d A. Wie groß ist die Leistung?' % (z(u), i), u * i, 'W', 'P = U · I', 'P = U · I', 0, 1)

    def reihe_par(r):
        k = c(r, 0, 1, 2)
        if k == 0:
            a, b, d = c(r, (2, 4, 6), (10, 22, 47), (100, 220, 330), (1.5, 2.5, 4))
            return N('Drei Widerstände mit %s Ω, %s Ω und %s Ω sind in Reihe geschaltet. Wie groß ist der Gesamtwiderstand?' % (z(a), z(b), z(d)), a + b + d, 'Ω', 'Reihe: R = R1 + R2 + R3', 'In Reihe werden Widerstände addiert.', 1)
        if k == 1:
            a, b = c(r, (6, 3), (10, 15), (20, 30), (4, 12), (60, 40))
            return N('R1 = %d Ω und R2 = %d Ω sind parallel geschaltet. Wie groß ist der Gesamtwiderstand? (auf 2 Dezimalen)' % (a, b), a * b / (a + b), 'Ω', 'R = R1 · R2 / (R1 + R2)', 'Parallel: Produkt durch Summe', 2, 0.01)
        a, b, u = c(r, (2, 4, 12), (100, 200, 12), (1, 3, 12), (220, 330, 5))
        return N('R1 = %d Ω und R2 = %d Ω liegen in Reihe an %d V. Welche Spannung fällt an R2 ab? (auf 2 Dezimalen)' % (a, b, u), u * b / (a + b), 'V', 'U2 = U · R2 / (R1 + R2)', 'Spannungsteiler: Die Spannung teilt sich im Verhältnis der Widerstände.', 2, 0.01)

    def batterie(r):
        k = c(r, 0, 1)
        if k == 0:
            q, i = c(r, (60, 4), (70, 0.05), (95, 2.5), (44, 8))
            return N('Eine Batterie mit %d Ah wird mit %s A entladen. Nach wie vielen Stunden ist sie rechnerisch leer?' % (q, z(i)), q / i, 'h', 't = Q / I', 'Kapazität durch Strom', 1, 0.1)
        e, u = c(r, (50, 400), (77, 400), (58, 350), (100, 800))
        return N('Eine Hochvoltbatterie hat %d kWh bei %d V. Wie groß ist ihre Kapazität in Ah? (auf ganze Ah)' % (e, u), e * 1000 / u, 'Ah', 'Q = W / U, kWh in Wh umrechnen', 'Energie in Wh durch Spannung', 0, 1)

    def laden(r):
        k = c(r, 0, 1)
        if k == 0:
            e, p = c(r, (44, 11), (60, 7.4), (50, 22), (77, 50), (36, 3.6))
            return N('Wie viele Stunden dauert es, %d kWh mit %s kW Ladeleistung nachzuladen? (auf 1 Dezimale)' % (e, z(p)), e / p, 'h', 't = W / P', 'Energie durch Leistung', 1, 0.1)
        e, pr = c(r, (45, 0.32), (60, 0.55), (38, 0.28), (70, 0.69))
        return N('Eine Ladung von %d kWh kostet %s € pro kWh. Wie hoch sind die Kosten?' % (e, z(pr)), e * pr, '€', 'Kosten = Energie · Preis', 'kWh mal Preis je kWh', 2, 0.01)

    def kosten_km(r):
        v, pr, km = c(r, (6.5, 1.85, 15000), (5.2, 1.75, 20000), (7.8, 1.9, 12000), (4.6, 1.7, 25000))
        return N('Ein Auto verbraucht %s l/100 km, der Liter kostet %s €. Wie hoch sind die Kraftstoffkosten für %d km?' % (z(v), z(pr), km), v / 100 * km * pr, '€', '%s l/100 km · %d km / 100 · %s €' % (z(v), km, z(pr)), 'Zuerst die Liter für die Strecke ausrechnen.', 2, 0.5)

    def abbrems(r):
        f, g = c(r, (9000, 15000), (7200, 12000), (10400, 16000), (6500, 13000), (11900, 17000))
        return N('Auf dem Bremsenprüfstand beträgt die Summe der Bremskräfte %d N, die Gewichtskraft des Fahrzeugs %d N. Wie groß ist die Abbremsung in %%?' % (f, g), f / g * 100, '%', 'z = Bremskraft / Gewichtskraft · 100', 'Bremskraft durch Gewichtskraft mal 100', 1, 0.1)

    def diff(r):
        a, b = c(r, (2500, 2000), (1800, 1530), (3000, 2100), (2200, 1980), (1600, 1040))
        return N('Bremskraft links %d N, rechts %d N. Wie groß ist die Differenz in %% des größeren Werts?' % (a, b), (a - b) / a * 100, '%', '(%d − %d) / %d · 100' % (a, b, a), 'Unterschied durch den größeren Wert mal 100', 1, 0.1)

    def wdh(r):
        k = c(r, 0, 1, 2, 3, 4, 5)
        if k == 0:
            d, s, zz = c(r, (80, 90, 4), (82, 92.8, 4), (84, 90, 6), (74, 77, 3))
            return N('Bohrung %s mm, Hub %s mm, %d Zylinder. Wie groß ist der Gesamthubraum? (auf ganze cm³)' % (z(d), z(s), zz), PI / 4 * (d / 10) ** 2 * s / 10 * zz, 'cm³', 'VH = π / 4 · d² · s · z, in cm rechnen', 'Zuerst den Hubraum eines Zylinders in cm³', 0, 3)
        if k == 1:
            m, n = c(r, (180, 3500), (240, 2000), (130, 5500), (350, 1750))
            return N('Ein Motor gibt %d Nm bei %d 1/min ab. Wie groß ist die Leistung in kW? (auf 1 Dezimale)' % (m, n), 2 * PI * m * n / 60 / 1000, 'kW', 'P = 2 · π · M · n mit n = %s 1/s' % z(n / 60, 2), 'Drehzahl in 1/s umrechnen', 1, 0.3)
        if k == 2:
            v, a, t = c(r, (50, 7, 1), (100, 8, 1), (80, 7.5, 1), (130, 8, 1))
            vs = v / 3.6
            return N('Geschwindigkeit %d km/h, Reaktionszeit %d s, Verzögerung %s m/s². Wie lang ist der Anhalteweg? (auf ganze m)' % (v, t, z(a)), vs * t + vs * vs / (2 * a), 'm', 'sA = v · tR + v² / (2 · a) mit v = %s m/s' % z(vs, 2), 'Reaktionsweg plus Bremsweg', 0, 1)
        if k == 3:
            f1, a1, a2 = c(r, (400, 3, 15), (600, 4, 10), (350, 2.5, 12.5))
            return N('Am Hauptbremszylinder (%s cm²) wirken %d N. Welche Kraft wirkt am Radbremskolben mit %s cm²?' % (z(a1), f1, z(a2)), f1 * a2 / a1, 'N', 'F2 = F1 · A2 / A1', 'Gleicher Druck auf beiden Seiten', 0, 1)
        if k == 4:
            z1, z2 = c(r, (13, 39), (17, 51), (11, 41), (23, 29), (31, 26))
            return N('Das treibende Zahnrad hat %d Zähne, das getriebene %d Zähne. Wie groß ist die Übersetzung? (auf 2 Dezimalen)' % (z1, z2), z2 / z1, '', 'i = z2 / z1', 'Getriebenes durch treibendes Rad', 2, 0.01)
        l, km = c(r, (47, 720), (36.4, 560), (55, 610))
        return N('Verbrauch: %s Liter auf %d km. Wie viel sind das pro 100 km? (auf 1 Dezimale)' % (z(l), km), l / km * 100, 'l/100 km', 'Liter / km · 100', 'Liter durch km mal 100', 1, 0.1)

    for t, n, f in [('Werkstattrechnung', 5, rechnung), ('Bruttobetrag', 6, brutto), ('Enthaltene Mehrwertsteuer', 5, mwstanteil), ('Skonto', 4, skonto), ('Teileaufschlag', 5, aufschlag), ('Arbeitswerte', 5, awzeit),
                    ('Ohmsches Gesetz', 11, ohm), ('Elektrische Leistung', 8, pel), ('Reihen- und Parallelschaltung', 11, reihe_par), ('Batterie', 7, batterie), ('Laden', 8, laden), ('Kraftstoffkosten', 4, kosten_km),
                    ('Abbremsung', 5, abbrems), ('Bremskraftdifferenz', 5, diff), ('Wiederholung Motor, Bremsen, Antrieb', 11, wdh)]:
        A.add(t, n, f)
    return A


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    titel = ['Grundstufe: Grundrechnen und Einheiten', '1. Klasse KFZ (FR · LJ 1)', '2. Klasse KFZ (FR · LJ 2)', '3. Klasse KFZ (FR · LJ 3)', '4. Klasse KFZ: Werkstattrechnen und Prüfungsvorbereitung']
    for i, fn in enumerate([level0, level1, level2, level3, level4]):
        A = fn()
        assert A.count() == 100, ('fr_%d' % i, A.count())
        open(os.path.join(here, 'fr_%d.txt' % i), 'w', encoding='utf-8').write('# Fachrechnen Level %d – %s\n# Diese Datei wird von gen_fr.py erzeugt. Änderungen bitte dort vornehmen.\n' % (i + 1, titel[i]) + '\n'.join(A.out) + '\n')
        print('fr_%d.txt' % i, A.count())
