#!/usr/bin/env python3
"""Erzeugt et_0.txt bis et_4.txt: je 40 Rechenaufgaben (Vorlagen mit wechselnden Zahlen)
plus die 60 Theoriefragen aus et_<n>_theorie.txt.  Neu erzeugen:  python3 gen_et.py
"""
import math, os
from gen_fr import N, M, L, z, c

PI = math.pi


def level0():
    A = L(20)

    def um(r):
        k = c(r, 0, 1, 2, 3, 4)
        if k == 0:
            v = c(r, 250, 35, 1200, 4.5, 800)
            return N('Rechne %s mA in A um.' % z(v), v / 1000, 'A', '1000 mA = 1 A', 'Durch 1000', 4, 0)
        if k == 1:
            v = c(r, 0.3, 1.25, 0.045, 2.5)
            return N('Rechne %s A in mA um.' % z(v), v * 1000, 'mA', '1 A = 1000 mA', 'Mal 1000')
        if k == 2:
            v = c(r, 1.5, 3.3, 0.68, 12)
            return N('Rechne %s kΩ in Ω um.' % z(v), v * 1000, 'Ω', '1 kΩ = 1000 Ω', 'Mal 1000')
        if k == 3:
            v = c(r, 470, 2200, 150, 5600)
            return N('Rechne %s Ω in kΩ um.' % z(v), v / 1000, 'kΩ', '1000 Ω = 1 kΩ', 'Durch 1000', 3, 0)
        v = c(r, 450, 900, 60, 1250)
        return N('Rechne %s mV in V um.' % z(v), v / 1000, 'V', '1000 mV = 1 V', 'Durch 1000', 3, 0)

    def u(r):
        rr, i = c(r, (2, 5), (4, 3), (6, 2), (10, 1.2), (3, 4), (8, 1.5), (12, 0.5))
        return N('R = %s Ω, I = %s A. Wie groß ist die Spannung U?' % (z(rr), z(i)), rr * i, 'V', 'U = R · I', 'U = R · I', 2)

    def i(r):
        uu, rr = c(r, (12, 6), (12, 4), (6, 3), (9, 4.5), (24, 8), (12, 24), (4.5, 9))
        return N('U = %s V, R = %s Ω. Wie groß ist der Strom I?' % (z(uu), z(rr)), uu / rr, 'A', 'I = U / R', 'I = U / R', 2)

    def rr_(r):
        uu, ii = c(r, (12, 2), (6, 0.3), (12, 0.5), (9, 3), (230, 10), (1.5, 0.1), (24, 6))
        return N('U = %s V, I = %s A. Wie groß ist der Widerstand R?' % (z(uu), z(ii)), uu / ii, 'Ω', 'R = U / I', 'R = U / I', 2)

    def p(r):
        uu, ii = c(r, (12, 5), (230, 4), (12, 1.75), (6, 0.5), (230, 0.26), (12, 10), (24, 2.5))
        return N('Ein Verbraucher liegt an %s V und nimmt %s A auf. Wie groß ist die Leistung?' % (z(uu), z(ii)), uu * ii, 'W', 'P = U · I', 'P = U · I', 1)

    def zellen(r):
        n, uz = c(r, (4, 1.5), (6, 2), (3, 1.2), (2, 1.5), (8, 1.5))
        return N('%d Zellen mit je %s V sind in Reihe geschaltet. Wie groß ist die Gesamtspannung?' % (n, z(uz)), n * uz, 'V', 'In Reihe addieren sich die Spannungen.', 'Anzahl mal Zellenspannung', 1)

    for t, n, f in [('Einheiten umrechnen', 12, um), ('Spannung berechnen', 6, u), ('Strom berechnen', 6, i), ('Widerstand berechnen', 6, rr_), ('Leistung berechnen', 6, p), ('Zellen in Reihe', 4, zellen)]:
        A.add(t, n, f)
    return A


def level1():
    A = L(21)

    def reihe(r):
        k = c(r, 0, 1, 2)
        a, b, uu = c(r, (2, 4, 12), (4, 8, 12), (10, 20, 12), (3, 9, 24), (1, 5, 12), (15, 45, 12))
        if k == 0:
            return N('R1 = %d Ω und R2 = %d Ω sind in Reihe geschaltet. Wie groß ist der Gesamtwiderstand?' % (a, b), a + b, 'Ω', 'Reihe: R = R1 + R2', 'Addieren')
        if k == 1:
            return N('R1 = %d Ω und R2 = %d Ω liegen in Reihe an %d V. Wie groß ist der Strom? (auf 2 Dezimalen)' % (a, b, uu), uu / (a + b), 'A', 'I = U / (R1 + R2)', 'Zuerst den Gesamtwiderstand berechnen.', 2, 0.01)
        return N('R1 = %d Ω und R2 = %d Ω liegen in Reihe an %d V. Welche Spannung fällt an R1 ab? (auf 2 Dezimalen)' % (a, b, uu), uu * a / (a + b), 'V', 'I = U / (R1 + R2), dann U1 = R1 · I', 'Erst den Strom, dann U1 = R1 · I', 2, 0.01)

    def par(r):
        k = c(r, 0, 1, 2)
        if k == 0:
            a = c(r, 10, 8, 6, 24, 100)
            return N('Zwei Widerstände von je %d Ω sind parallel geschaltet. Wie groß ist der Gesamtwiderstand?' % a, a / 2, 'Ω', 'Zwei gleiche Widerstände parallel: R / 2', 'Die Hälfte')
        a, b, uu = c(r, (6, 3, 12), (12, 4, 12), (10, 15, 12), (20, 30, 12), (8, 24, 24))
        if k == 1:
            return N('R1 = %d Ω und R2 = %d Ω sind parallel geschaltet. Wie groß ist der Gesamtwiderstand? (auf 2 Dezimalen)' % (a, b), a * b / (a + b), 'Ω', 'R = R1 · R2 / (R1 + R2)', 'Produkt durch Summe', 2, 0.01)
        return N('R1 = %d Ω und R2 = %d Ω liegen parallel an %d V. Wie groß ist der Gesamtstrom? (auf 2 Dezimalen)' % (a, b, uu), uu / a + uu / b, 'A', 'I = U / R1 + U / R2', 'Die Teilströme einzeln berechnen und addieren.', 2, 0.01)

    def lampen(r):
        n, pp = c(r, (2, 55), (2, 21), (4, 5), (2, 60), (3, 21))
        return N('%d Glühlampen mit je %d W sind an 12 V parallel geschaltet. Wie groß ist der Gesamtstrom? (auf 2 Dezimalen)' % (n, pp), n * pp / 12, 'A', 'I = P gesamt / U', 'Gesamtleistung durch Spannung', 2, 0.01)

    def leistung(r):
        k = c(r, 0, 1, 2)
        if k == 0:
            pp = c(r, 21, 55, 5, 60, 100, 180)
            return N('Eine Glühlampe hat 12 V und %d W. Welcher Strom fließt? (auf 2 Dezimalen)' % pp, pp / 12, 'A', 'I = P / U', 'I = P / U', 2, 0.01)
        if k == 1:
            uu, rr = c(r, (12, 6), (12, 2.4), (12, 0.6), (230, 52.9))
            return N('An einem Widerstand von %s Ω liegen %s V an. Wie groß ist die Leistung? (auf ganze W)' % (z(rr), z(uu)), uu * uu / rr, 'W', 'P = U² / R', 'P = U² / R', 0, 1)
        ii, rr = c(r, (5, 2), (10, 0.5), (2, 6), (20, 0.1))
        return N('Durch einen Widerstand von %s Ω fließen %d A. Wie groß ist die Leistung?' % (z(rr), ii), ii * ii * rr, 'W', 'P = I² · R', 'P = I² · R', 0, 1)

    def arbeit(r):
        pp, t = c(r, (60, 2), (110, 0.5), (1000, 1.5), (55, 3), (21, 10), (2000, 0.25))
        return N('Ein %d-W-Verbraucher läuft %s Stunden. Wie viel Energie verbraucht er?' % (pp, z(t)), pp * t, 'Wh', 'W = P · t', 'Leistung mal Zeit', 1)

    def eta(r):
        pz, pa = c(r, (100, 85), (1500, 1200), (60, 45), (250, 220), (800, 560))
        return N('Ein Elektromotor nimmt %d W auf und gibt %d W ab. Wie groß ist der Wirkungsgrad in %%?' % (pz, pa), pa / pz * 100, '%', 'η = Pab / Pzu · 100', 'Abgegeben durch aufgenommen', 1, 0.1)

    def batt(r):
        k = c(r, 0, 1)
        if k == 0:
            q, ii = c(r, (60, 5), (44, 2), (70, 3.5), (95, 10), (50, 0.5))
            return N('Eine Batterie mit %d Ah versorgt einen Verbraucher mit %s A. Wie viele Stunden reicht sie theoretisch?' % (q, z(ii)), q / ii, 'h', 't = Q / I', 'Kapazität durch Strom', 1, 0.1)
        ii, t = c(r, (6, 5), (4, 8), (10, 3), (2.5, 12))
        return N('Eine Batterie wird %d Stunden lang mit %s A geladen. Welche Ladung wird zugeführt?' % (t, z(ii)), ii * t, 'Ah', 'Q = I · t', 'Strom mal Zeit', 1)

    def ufall(r):
        ii, rr = c(r, (10, 0.05), (20, 0.02), (150, 0.004), (5, 0.12), (30, 0.01))
        return N('Durch eine Leitung mit %s Ω fließen %d A. Wie groß ist der Spannungsfall an der Leitung?' % (z(rr), ii), ii * rr, 'V', 'Uv = I · RLeitung', 'Strom mal Leitungswiderstand', 2, 0.01)

    def rleit(r):
        l, a = c(r, (5, 1.5), (10, 2.5), (3, 0.75), (8, 4), (2, 1))
        return N('Eine Kupferleitung ist %d m lang und hat %s mm² Querschnitt. Wie groß ist ihr Widerstand? Rechne mit ρ = 0,0178 Ω·mm²/m. (auf 3 Dezimalen)' % (l, z(a)), 0.0178 * l / a, 'Ω', 'R = ρ · l / A', 'R = ρ · l / A', 3, 0.002)

    for t, n, f in [('Reihenschaltung', 9, reihe), ('Parallelschaltung', 8, par), ('Lampen parallel', 3, lampen), ('Leistung', 7, leistung), ('Elektrische Arbeit', 3, arbeit), ('Wirkungsgrad', 2, eta), ('Batterie', 4, batt), ('Spannungsfall', 2, ufall), ('Leitungswiderstand', 2, rleit)]:
        A.add(t, n, f)
    return A


def level2():
    A = L(22)

    def teiler(r):
        a, b, uu = c(r, (1000, 1000, 5), (2200, 1000, 5), (3300, 1700, 5), (1000, 4000, 5), (470, 330, 12), (10000, 2500, 5), (680, 320, 5))
        return N('Spannungsteiler an %d V: R1 = %d Ω (oben), R2 = %d Ω (unten). Welche Spannung liegt an R2? (auf 2 Dezimalen)' % (uu, a, b), uu * b / (a + b), 'V', 'U2 = U · R2 / (R1 + R2)', 'Die Spannung teilt sich im Verhältnis der Widerstände.', 2, 0.01)

    def ntc(r):
        rv, rn, txt = c(r, (2500, 2500, '20 °C'), (2500, 300, '90 °C'), (2200, 5800, '0 °C'), (2500, 1200, '40 °C'), (1000, 250, '80 °C'))
        return N('Ein NTC-Fühler hat bei %s einen Widerstand von %d Ω. Er liegt in Reihe mit %d Ω im Steuergerät an 5 V. Welche Signalspannung fällt am Fühler ab? (auf 2 Dezimalen)' % (txt, rn, rv), 5 * rn / (rv + rn), 'V', 'UNTC = 5 V · RNTC / (RV + RNTC)', 'Spannungsteiler aus Vorwiderstand und Fühler', 2, 0.01)

    def poti(r):
        p = c(r, 20, 35, 50, 80, 12)
        return N('Ein Drosselklappenpotenziometer wird mit 5 V versorgt und steht bei %d %% seines Wegs. Welche Signalspannung gibt es ab?' % p, 5 * p / 100, 'V', 'U = 5 V · %d / 100' % p, 'Anteil des Wegs mal Versorgungsspannung', 2, 0.01)

    def pwm(r):
        k = c(r, 0, 1, 2)
        if k == 0:
            e, a = c(r, (2, 8), (3, 7), (5, 5), (6, 2), (1, 4), (9, 3))
            return N('Ein PWM-Signal ist %d ms eingeschaltet und %d ms ausgeschaltet. Wie groß ist das Tastverhältnis in %%?' % (e, a), e / (e + a) * 100, '%', 'Tastverhältnis = tein / T · 100', 'Einschaltzeit durch Periodendauer', 1, 0.1)
        if k == 1:
            t, uu = c(r, (25, 12), (40, 12), (75, 12), (60, 5), (10, 14))
            return N('Ein PWM-Signal mit %d V hat ein Tastverhältnis von %d %%. Wie groß ist die mittlere Spannung?' % (uu, t), uu * t / 100, 'V', 'Umittel = U · Tastverhältnis', 'Spannung mal Tastverhältnis', 2, 0.01)
        tt = c(r, 10, 20, 4, 2.5, 50, 1)
        return N('Ein Signal hat eine Periodendauer von %s ms. Wie groß ist die Frequenz?' % z(tt), 1000 / tt, 'Hz', 'f = 1 / T', 'f = 1 / T, Millisekunden in Sekunden umrechnen', 1, 0.1)

    def led(r):
        ub, ul, il = c(r, (12, 2, 20), (12, 3.2, 20), (5, 2, 10), (14, 2, 15), (12, 1.8, 30))
        return N('Eine LED (%s V, %d mA) soll an %d V betrieben werden. Wie groß muss der Vorwiderstand sein? (auf ganze Ω)' % (z(ul), il, ub), (ub - ul) / (il / 1000), 'Ω', 'R = (U − ULED) / I', 'Am Vorwiderstand fällt die Restspannung ab.', 0, 1)

    def zuend(r):
        n1, n2, u1 = c(r, (100, 10000, 300), (150, 12000, 350), (200, 20000, 400), (120, 9600, 300))
        return N('Eine Zündspule hat primär %d und sekundär %d Windungen. Die Primärspannung beim Abschalten erreicht %d V. Welche Sekundärspannung entsteht ohne Verluste? (in kV)' % (n1, n2, u1), u1 * n2 / n1 / 1000, 'kV', 'U2 = U1 · N2 / N1', 'Die Spannung wird im Verhältnis der Windungszahlen übersetzt.', 1, 0.1)

    def drehz(r):
        zz, f = c(r, (60, 3000), (60, 800), (58, 2900), (48, 1600), (36, 1200))
        return N('Ein Geberrad mit %d Zähnen erzeugt am Drehzahlsensor %d Impulse pro Sekunde. Wie groß ist die Drehzahl in 1/min?' % (zz, f), f / zz * 60, '1/min', 'n = f / z · 60', 'Impulse pro Sekunde durch Zähnezahl mal 60', 0, 1)

    def schliess(r):
        u, rr = c(r, (12, 0.6), (14, 0.5), (12, 1.5), (13.5, 0.75))
        return N('Die Primärwicklung einer Zündspule hat %s Ω. Welcher Strom stellt sich an %s V höchstens ein? (auf 1 Dezimale)' % (z(rr), z(u)), u / rr, 'A', 'I = U / R', 'Ohmsches Gesetz', 1, 0.1)

    for t, n, f in [('Spannungsteiler', 7, teiler), ('NTC am Spannungsteiler', 5, ntc), ('Potenziometer', 4, poti), ('PWM und Frequenz', 12, pwm), ('LED-Vorwiderstand', 4, led), ('Zündspule', 3, zuend), ('Drehzahlsignal', 3, drehz), ('Primärstrom', 2, schliess)]:
        A.add(t, n, f)
    return A


def level3():
    A = L(23)

    def hvp(r):
        k = c(r, 0, 1)
        if k == 0:
            uu, ii = c(r, (400, 150), (350, 200), (800, 250), (400, 32), (360, 125))
            return N('Ein Hochvoltantrieb nimmt bei %d V einen Strom von %d A auf. Wie groß ist die Leistung in kW?' % (uu, ii), uu * ii / 1000, 'kW', 'P = U · I, dann durch 1000', 'P = U · I', 1, 0.1)
        pp, uu = c(r, (100, 400), (150, 800), (80, 350), (11, 400), (50, 400))
        return N('Eine E-Maschine leistet %d kW an %d V. Welcher Strom fließt? (auf ganze A)' % (pp, uu), pp * 1000 / uu, 'A', 'I = P / U', 'Leistung in W durch Spannung', 0, 1)

    def iso(r):
        uu = c(r, 400, 350, 800, 600, 450)
        return N('Für ein Hochvoltsystem mit %d V Gleichspannung werden mindestens 500 Ω je Volt Isolationswiderstand verlangt. Wie groß muss der Isolationswiderstand mindestens sein? (in kΩ)' % uu, uu * 500 / 1000, 'kΩ', 'R = %d V · 500 Ω/V' % uu, 'Spannung mal 500 Ω, dann in kΩ', 0, 1)

    def kond(r):
        e, v = c(r, (58, 16), (77, 18), (50, 15), (64, 20), (40, 14))
        return N('Eine Hochvoltbatterie hat %d kWh nutzbar. Der Verbrauch beträgt %d kWh/100 km. Wie groß ist die rechnerische Reichweite? (auf ganze km)' % (e, v), e / v * 100, 'km', 'Reichweite = Energie / Verbrauch · 100', 'kWh durch kWh/100 km mal 100', 0, 2)

    def ladez(r):
        e, pp = c(r, (40, 11), (55, 7.4), (30, 3.7), (60, 22), (50, 100))
        return N('Wie lange dauert es, %d kWh mit %s kW nachzuladen? (in Stunden, auf 1 Dezimale)' % (e, z(pp)), e / pp, 'h', 't = W / P', 'Energie durch Leistung', 1, 0.1)

    def bilanz(r):
        v = r.sample([8, 10, 12, 15, 18, 20, 25, 30, 4, 6], 4)
        g = c(r, 90, 120, 140)
        return N('Ein Generator liefert höchstens %d A. Eingeschaltet sind Verbraucher mit %d A, %d A, %d A und %d A. Wie viel Strom bleibt zum Laden der Batterie?' % (g, v[0], v[1], v[2], v[3]), g - sum(v), 'A', 'Generatorstrom minus Summe der Verbraucherströme', 'Zuerst alle Verbraucherströme zusammenzählen.', 0)

    def ruhe(r):
        q, ii = c(r, (70, 0.05), (60, 0.25), (80, 0.04), (95, 0.5), (44, 0.02))
        return N('Eine Batterie mit %d Ah wird durch einen Ruhestrom von %s A entladen. Nach wie vielen Tagen ist sie rechnerisch leer? (auf 1 Dezimale)' % (q, z(ii)), q / ii / 24, 'Tage', 't = Q / I in Stunden, dann durch 24', 'Erst die Stunden ausrechnen, dann durch 24 teilen.', 1, 0.2)

    def glueh(r):
        n, rr, uu = c(r, (4, 0.8, 11.5), (4, 0.6, 12), (6, 1.0, 11), (4, 1.2, 12), (3, 0.5, 11))
        return N('%d Glühkerzen mit je %s Ω liegen parallel an %s V. Wie groß ist der Gesamtstrom? (auf 1 Dezimale)' % (n, z(rr), z(uu)), n * uu / rr, 'A', 'I = Anzahl · U / R', 'Den Strom einer Kerze ausrechnen und mit der Anzahl malnehmen.', 1, 0.1)

    def starter(r):
        ii, uv = c(r, (200, 0.4), (150, 0.6), (300, 0.3), (180, 0.9), (250, 0.5))
        return N('Beim Starten fließen %d A, in der Plusleitung fallen %s V ab. Wie groß ist der Widerstand der Leitung samt Übergängen? (in mΩ)' % (ii, z(uv)), uv / ii * 1000, 'mΩ', 'R = U / I, dann mal 1000', 'R = U / I', 1, 0.1)

    def lader(r):
        pz, e = c(r, (11, 92), (7.4, 90), (22, 94), (3.7, 88))
        return N('Ein Onboard-Lader nimmt %s kW aus dem Netz auf und hat einen Wirkungsgrad von %d %%. Welche Leistung kommt an der Batterie an? (auf 2 Dezimalen)' % (z(pz), e), pz * e / 100, 'kW', 'Pab = Pzu · η', 'Aufgenommene Leistung mal Wirkungsgrad', 2, 0.02)

    def welle(r):
        zz, n = c(r, (4, 3000), (4, 1500), (6, 2400), (3, 6000))
        return N('Wie viele Einspritzungen (Haupteinspritzungen) pro Sekunde braucht ein %d-Zylinder-Viertaktmotor bei %d 1/min?' % (zz, n), n / 60 / 2 * zz, '1/s', 'Jeder Zylinder spritzt einmal in zwei Umdrehungen ein: n / 60 / 2 · z', 'Ein Arbeitsspiel dauert zwei Umdrehungen.', 0, 0)

    for t, n, f in [('Leistung im Hochvoltsystem', 7, hvp), ('Isolationswiderstand', 4, iso), ('Reichweite', 3, kond), ('Ladezeit', 4, ladez), ('Strombilanz', 5, bilanz), ('Ruhestrom', 4, ruhe), ('Glühkerzen', 4, glueh), ('Starterleitung', 4, starter), ('Lader', 3, lader), ('Einspritzfrequenz', 2, welle)]:
        A.add(t, n, f)
    return A


def level4():
    A = L(24)

    def gemischt(r):
        a, b, d, uu = c(r, (2, 6, 3, 12), (4, 12, 6, 12), (10, 20, 30, 12), (1, 4, 4, 12), (5, 10, 10, 24), (3, 6, 12, 14))
        k = c(r, 0, 1)
        rp = b * d / (b + d)
        if k == 0:
            return N('R1 = %d Ω liegt in Reihe mit der Parallelschaltung aus R2 = %d Ω und R3 = %d Ω. Wie groß ist der Gesamtwiderstand? (auf 2 Dezimalen)' % (a, b, d), a + rp, 'Ω', 'Rp = R2 · R3 / (R2 + R3), dann R = R1 + Rp', 'Zuerst die Parallelschaltung zusammenfassen.', 2, 0.01)
        return N('R1 = %d Ω liegt in Reihe mit der Parallelschaltung aus R2 = %d Ω und R3 = %d Ω an %d V. Wie groß ist der Gesamtstrom? (auf 2 Dezimalen)' % (a, b, d, uu), uu / (a + rp), 'A', 'I = U / (R1 + Rp)', 'Zuerst den Gesamtwiderstand berechnen.', 2, 0.01)

    def can(r):
        k = c(r, 0, 1)
        if k == 0:
            a, b = c(r, (120, 120), (120, 60), (120, 240))
            return N('Zwischen CAN-High und CAN-Low liegen zwei Widerstände mit %d Ω und %d Ω parallel. Welchen Wert zeigt das Ohmmeter?' % (a, b), a * b / (a + b), 'Ω', 'Parallel: R1 · R2 / (R1 + R2)', 'Produkt durch Summe', 1, 0.5)
        h, l = c(r, (3.5, 1.5), (3.6, 1.4), (3.4, 1.6), (2.5, 2.5))
        return N('CAN-High hat %s V, CAN-Low %s V. Wie groß ist die Differenzspannung?' % (z(h), z(l)), h - l, 'V', 'UDiff = UCAN-H − UCAN-L', 'High minus Low', 1, 0.05)

    def ueber(r):
        uv, ii = c(r, (0.8, 10), (1.2, 15), (0.5, 25), (2.4, 8), (0.3, 60), (1.5, 5))
        return N('An einer Steckverbindung werden unter Last %s V Spannungsfall gemessen, es fließen %d A. Wie groß ist der Übergangswiderstand? (in mΩ)' % (z(uv), ii), uv / ii * 1000, 'mΩ', 'R = U / I, dann mal 1000', 'R = U / I', 0, 1)

    def verlust(r):
        uv, ii = c(r, (0.8, 10), (1.2, 15), (0.5, 25), (2.0, 20), (0.6, 40))
        return N('An einem korrodierten Massepunkt fallen %s V ab, es fließen %d A. Welche Leistung wird dort in Wärme umgesetzt?' % (z(uv), ii), uv * ii, 'W', 'P = U · I', 'Spannungsfall mal Strom', 1, 0.1)

    def lampe_u(r):
        ub, uv, pp = c(r, (12, 1.2, 55), (12, 0.6, 21), (13.5, 1.5, 55), (12, 2.0, 60))
        return N('Eine 12-V-Lampe mit %d W liegt wegen %s V Spannungsfall nur an %s V. Auf wie viel Prozent sinkt ihre Leistung, wenn der Widerstand gleich bleibt? (auf ganze %%)' % (pp, z(uv), z(ub - uv)), ((ub - uv) / ub) ** 2 * 100, '%', 'P ändert sich mit U²: (%s / %s)² · 100' % (z(ub - uv), z(ub)), 'Die Leistung hängt vom Quadrat der Spannung ab.', 0, 1)

    def sicherung(r):
        pp, uu = c(r, (120, 12), (180, 12), (55, 12), (300, 12), (90, 12))
        ii = pp / uu
        nxt = [x for x in [5, 7.5, 10, 15, 20, 25, 30, 40] if x >= ii * 1.25][0]
        w = [x for x in [5, 7.5, 10, 15, 20, 25, 30, 40, 50] if x != nxt]
        lo = [x for x in w if x < nxt][-1:]
        hi = [x for x in w if x > nxt][:2]
        wrong = (lo + hi + [50])[:3]
        return M('Ein Verbraucher mit %d W an %d V soll abgesichert werden. Die Sicherung soll etwa 25 %% über dem Betriebsstrom liegen. Welche Sicherung passt?' % (pp, uu), '%s A' % z(nxt), ['%s A' % z(x) for x in wrong], 'I = P / U = %s A, mal 1,25 = %s A, nächstgrößere Sicherung' % (z(ii, 2), z(ii * 1.25, 2)))

    def quer(r):
        ii, l, uv = c(r, (10, 4, 0.5), (20, 3, 0.4), (15, 6, 0.6), (30, 2, 0.3), (8, 5, 0.25))
        return N('Eine Kupferleitung von %d m Länge soll bei %d A höchstens %s V Spannungsfall haben. Welcher Querschnitt ist mindestens nötig? Rechne mit ρ = 0,0178 Ω·mm²/m. (auf 2 Dezimalen)' % (l, ii, z(uv)), 0.0178 * l * ii / uv, 'mm²', 'A = ρ · l · I / Uv', 'Zuerst den zulässigen Widerstand R = Uv / I, dann A = ρ · l / R', 2, 0.03)

    def energie(r):
        pp, t, pr = c(r, (2000, 3, 0.3), (11000, 4, 0.35), (60, 24, 0.3), (3700, 6, 0.28))
        return N('Ein Gerät mit %d W läuft %d Stunden. Die kWh kostet %s €. Wie hoch sind die Stromkosten?' % (pp, t, z(pr)), pp / 1000 * t * pr, '€', 'W = P · t in kWh, dann mal Preis', 'Leistung in kW mal Stunden mal Preis', 2, 0.01)

    def messb(r):
        v, k = c(r, (2.4, 5), (3.6, 2), (1.5, 20), (4.2, 0.5), (2.8, 10))
        return N('Auf dem Oszilloskop ist ein Signal %s Kästchen hoch. Eingestellt sind %s V pro Kästchen. Wie groß ist die Spannung?' % (z(v), z(k)), v * k, 'V', 'Kästchen mal Volt pro Kästchen', 'Höhe in Kästchen mal Einstellung', 2, 0.01)

    def zeitb(r):
        v, k = c(r, (4, 5), (2.5, 2), (8, 0.5), (5, 10), (3.2, 1))
        return N('Eine Periode ist auf dem Oszilloskop %s Kästchen breit. Eingestellt sind %s ms pro Kästchen. Wie groß ist die Frequenz? (auf 1 Dezimale)' % (z(v), z(k)), 1000 / (v * k), 'Hz', 'T = Kästchen · ms/Kästchen, f = 1 / T', 'Zuerst die Periodendauer ausrechnen.', 1, 0.2)

    for t, n, f in [('Gemischte Schaltung', 8, gemischt), ('CAN-Bus', 5, can), ('Übergangswiderstand', 5, ueber), ('Verlustleistung', 4, verlust), ('Unterspannung an der Lampe', 3, lampe_u), ('Sicherung auswählen', 4, sicherung), ('Leitungsquerschnitt', 3, quer), ('Stromkosten', 2, energie), ('Oszilloskop: Spannung', 3, messb), ('Oszilloskop: Frequenz', 3, zeitb)]:
        A.add(t, n, f)
    return A


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    titel = ['Grundstufe', '1. Klasse KFZ', '2. Klasse KFZ', '3. Klasse KFZ', '4. Klasse KFZ']
    for i, fn in enumerate([level0, level1, level2, level3, level4]):
        A = fn()
        assert A.count() == 40, ('et_%d' % i, A.count())
        tp = os.path.join(here, 'et_%d_theorie.txt' % i)
        th = open(tp, encoding='utf-8').read().strip() if os.path.exists(tp) else ''
        open(os.path.join(here, 'et_%d.txt' % i), 'w', encoding='utf-8').write('# Elektrotechnik Level %d – %s\n# Diese Datei wird von gen_et.py erzeugt: Theorie aus et_%d_theorie.txt, Rechenaufgaben aus Vorlagen.\n' % (i + 1, titel[i], i) + th + '\n# ===== Rechenaufgaben =====\n' + '\n'.join(A.out) + '\n')
        print('et_%d.txt' % i, A.count(), 'Rechenaufgaben')
