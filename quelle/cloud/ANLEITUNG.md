# Online-Speicher einrichten (Klassenrangliste, Wunsch- und Fehlerliste)

Die Online-Funktionen brauchen einen kostenlosen Speicher bei Supabase. Gespeichert werden nur
Vorname, Klasse, Punkte und die Meldungen aus der Wunsch- und Fehlerliste. E-Mail-Adressen werden nicht erfasst.

## Einmalig einrichten

1. Auf https://supabase.com ein kostenloses Konto anlegen.
2. `New project` wählen. Name frei, Region `Central EU (Frankfurt)`. Das Datenbank-Passwort notieren; im Spiel wird es nicht gebraucht.
3. Links `SQL Editor` öffnen, `New query` wählen.
4. Den gesamten Inhalt von `supabase.sql` einfügen.
5. In der letzten Zeile `HIER-EIN-LANGES-KENNWORT-EINTRAGEN` durch ein eigenes, langes Kennwort ersetzen. Das ist das Online-Kennwort für den Lehrer-Bereich.
6. `Run` drücken. Es muss „Success“ erscheinen.
7. Links `Project Settings`, dann `API` (oder `API Keys`) öffnen. Dort stehen:
   - die `Project URL`, zum Beispiel `https://abcdefgh.supabase.co`
   - der öffentliche Schlüssel (`anon public` oder `publishable`)
8. Beide Werte in `cloud.json` eintragen und das Spiel neu bauen (`python3 quelle/build.py .`), oder die Werte an Claude geben.

Der öffentliche Schlüssel darf im Spiel stehen. Er erlaubt nur die Funktionen aus `supabase.sql`.
Den Schlüssel `service_role` oder `secret` niemals weitergeben oder ins Spiel schreiben.

## Benutzen

- Lehrer-Bereich, Reiter „Klassen und Meldungen“: mit dem Online-Kennwort anmelden, Klasse anlegen, Code weitergeben.
- Schüler: „Rangliste“, Code eingeben oder den Einladungslink antippen.
- Meldungen der Schüler erscheinen im selben Reiter, mit Bild, und lassen sich als erledigt markieren oder löschen.

## Kennwort ändern

Im SQL Editor ausführen (neues Kennwort einsetzen):

```sql
update wq_config set value = wq_h('NEUES-KENNWORT') where key = 'admin_hash';
```

## Hinweise

- Das kostenlose Supabase-Projekt wird nach längerer Zeit ohne Zugriffe pausiert und muss dann im Supabase-Konto wieder gestartet werden.
- Die Rangliste ist ein Ansporn, kein Leistungsnachweis: Wer sich auskennt, kann seinen Punktestand auf dem eigenen Gerät verändern.

## E-Mail bei neuer Meldung (freiwillig)

Das Spiel kann bei jeder neuen Meldung eine E-Mail an die Lehrperson auslösen. Dafür wird der
kostenlose Dienst Web3Forms benutzt.

1. Auf https://web3forms.com die eigene E-Mail-Adresse eintragen und „Create Access Key“ wählen.
2. Den Schlüssel aus der Bestätigungs-E-Mail in `cloud.json` bei `mail` eintragen und neu bauen.

Mitgeschickt werden Art und Text der Meldung, aber kein Name und kein Bild. Der Schlüssel steht
im Spiel und ist öffentlich; mit ihm kann man nur E-Mails an die hinterlegte Adresse auslösen.

## Update 1: Klassenstufe über den Klassencode

Seit diesem Update wählen neue Schüler ihre Klasse nicht mehr selbst. Sie melden sich mit Vorname und
Klassencode an und bekommen die Klassenstufe der Klasse.

1. Im Supabase SQL Editor den Inhalt von `update_1_klassenstufe.sql` einfügen und `Run` drücken.
   Das Lehrer-Kennwort bleibt erhalten. Nicht das ganze `supabase.sql` erneut ausführen, sonst wird das Kennwort zurückgesetzt.
2. Im Spiel unter „Klassen und Meldungen“ bei jeder bestehenden Klasse die richtige Klassenstufe einstellen.
   Bestehende Klassen stehen nach dem Update auf „Grundstufe“.
