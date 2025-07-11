# THOR Agent Installation Guide

## Voraussetzungen

1. **Python 3.8+** installiert
2. **Git** installiert
3. **LM Studio** (für lokales LLM)
4. **API Keys** in `.env` Datei:
   ```
   ANTHROPIC_API_KEY=your_key_here
   ELEVENLABS_API_KEY=your_key_here
   ELEVENLABS_VOICE_ID=nF9mrdeA89H7gsev6yt0
   PICOVOICE_ACCESS_KEY=your_key_here (optional)
   ```

## Installation

### 1. Repository klonen
```bash
git clone https://github.com/Narion2025/L_Thor_M.git
cd L_Thor_M
```

### 2. Virtuelle Umgebung erstellen
```bash
python3 -m venv venv
source venv/bin/activate  # Auf Mac/Linux
```

### 3. Dependencies installieren
```bash
pip install -r requirements.txt
```

### 4. LM Studio Setup
- LM Studio öffnen
- Model "Phi-4 Mini Reasoning" herunterladen
- Server auf Port 1234 starten

### 5. Konfiguration anpassen
- `config/config.yaml` nach Bedarf anpassen
- Besonders die Pfade unter `system.personal_spaces`

## THOR starten

```bash
python src/main.py
```

## Features

### 1. Proaktive Unterstützung
- Beobachtet Ihr Nutzerverhalten
- Schlägt automatisch Verbesserungen vor
- Räumt Downloads-Ordner auf
- Erstellt Backups

### 2. MIND System
- Semantisches Bewusstsein
- Selbstreflexion
- Lernt aus Erfahrungen
- Merkt sich Präferenzen

### 3. Sprachsteuerung
- Wake Word: "THOR" oder Taste 't'
- Natürliche deutsche Sprache
- ElevenLabs Sprachausgabe

### 4. Dateioperationen
- Kopieren, Verschieben, Löschen
- Automatische Organisation
- Projekt-Strukturierung
- Git-Integration

## Beispielbefehle

Nach Aktivierung durch "THOR" oder 't':

- "Kopiere alle PDFs von Downloads nach Dokumente"
- "Räume meinen Downloads-Ordner auf"
- "Erstelle ein Backup meiner Projekte"
- "Was hast du heute gelernt?"
- "Zeige mir deine Gedanken"

## Troubleshooting

### LM Studio verbindet nicht
- Prüfen ob Server auf Port 1234 läuft
- Firewall-Einstellungen checken

### ElevenLabs funktioniert nicht
- API Key prüfen
- Voice ID prüfen
- Internet-Verbindung checken

### Wake Word reagiert nicht
- Mikrofon-Berechtigung prüfen
- Alternativ Keyboard-Mode verwenden (Taste 't')

## Updates

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## Support

Bei Fragen oder Problemen:
- GitHub Issues erstellen
- Logs checken in `logs/thor.log`
