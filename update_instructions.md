# Anleitung zur manuellen Aktualisierung des Kalenders

Da GitHub Actions aufgrund von Berechtigungsbeschränkungen nicht automatisch eingerichtet werden können, hier die Anleitung zur manuellen Aktualisierung:

## Schritt 1: PDF-Text extrahieren

1. Öffnen Sie Ihr PDF-Dienstplan
2. Verwenden Sie OCR-Software oder kopieren Sie den Text manuell
3. Speichern Sie den extrahierten Text in der Datei `pdf_ocr_output.txt`

## Schritt 2: Repository aktualisieren

1. Klonen Sie das Repository lokal:
   ```bash
   git clone https://github.com/MioEck/dienstplan-kalender.git
   cd dienstplan-kalender
   ```

2. Ersetzen Sie die Datei `pdf_ocr_output.txt` mit Ihrem neuen Text

3. Führen Sie das Konvertierungsskript aus:
   ```bash
   pip install ics
   python pdf_to_ics_converter.py
   ```

4. Committen und pushen Sie die Änderungen:
   ```bash
   git add .
   git commit -m "Update calendar for week XX"
   git push
   ```

## Schritt 3: Kalender-Abo verwenden

Die aktualisierte ICS-Datei ist dann über diese URL verfügbar:
```
https://raw.githubusercontent.com/MioEck/dienstplan-kalender/main/dienstplan.ics
```

Diese URL können Sie in Ihrem iOS-Kalender oder anderen Kalender-Apps als Abo hinzufügen.

## Automatisierung (optional)

Für eine vollständige Automatisierung können Sie:

1. Ein GitHub Actions Workflow manuell im Repository erstellen
2. Einen Webhook einrichten, der bei PDF-Uploads ausgelöst wird
3. Eine Web-App entwickeln, die PDFs hochlädt und automatisch konvertiert

## Hinweise

- Die ICS-Datei wird bei jeder Aktualisierung überschrieben
- Kalender-Apps aktualisieren Abos in unterschiedlichen Intervallen
- Bei iOS kann eine manuelle Synchronisation in den Kalender-Einstellungen erzwungen werden

