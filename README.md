# Dienstplan Kalender

Automatische Umwandlung von PDF-Dienstplänen in ICS-Kalenderdateien für iOS und andere Kalender-Apps.

## Übersicht

Dieses Repository enthält ein Python-Skript, das PDF-Dienstpläne in ICS-Kalenderdateien umwandelt. Die ICS-Datei kann dann in iOS-Kalender oder andere Kalender-Apps importiert oder als Kalender-Abo verwendet werden.

## Dateien

- `pdf_to_ics_converter.py`: Python-Skript zur Umwandlung von PDF-Dienstplänen in ICS-Format
- `dienstplan.ics`: Beispiel-ICS-Datei, die aus einem PDF-Dienstplan generiert wurde

## Verwendung

### Voraussetzungen

```bash
pip install ics
```

### PDF zu ICS konvertieren

1. Extrahieren Sie den Text aus Ihrem PDF-Dienstplan (z.B. mit OCR-Software)
2. Speichern Sie den extrahierten Text in einer Datei namens `pdf_ocr_output.txt`
3. Führen Sie das Konvertierungsskript aus:

```bash
python pdf_to_ics_converter.py
```

4. Die generierte ICS-Datei `dienstplan.ics` kann nun in Ihren Kalender importiert werden

### Kalender-Abo einrichten

Die ICS-Datei in diesem Repository kann als Kalender-Abo verwendet werden:

**URL für Kalender-Abo:**
```
https://raw.githubusercontent.com/MioEck/dienstplan-kalender/main/dienstplan.ics
```

#### iOS-Kalender

1. Öffnen Sie die Einstellungen-App
2. Gehen Sie zu "Kalender" > "Accounts"
3. Tippen Sie auf "Account hinzufügen" > "Andere"
4. Wählen Sie "Kalender-Abo hinzufügen"
5. Geben Sie die obige URL ein
6. Folgen Sie den Anweisungen zum Abschluss der Einrichtung

#### Google Kalender

1. Öffnen Sie Google Kalender im Browser
2. Klicken Sie links auf das "+" neben "Weitere Kalender"
3. Wählen Sie "Über URL"
4. Geben Sie die obige URL ein
5. Klicken Sie auf "Kalender hinzufügen"

## Automatisierung

Das Repository kann mit GitHub Actions erweitert werden, um automatisch neue PDF-Dienstpläne zu verarbeiten und die ICS-Datei zu aktualisieren.

## Hinweise

- Das Skript ist speziell für das Format der bereitgestellten PDF-Dienstpläne optimiert
- Bei anderen PDF-Formaten müssen möglicherweise Anpassungen am Parsing-Code vorgenommen werden
- Die OCR-Qualität beeinflusst die Genauigkeit der Konvertierung

## Lizenz

MIT License

