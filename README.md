# THOR Agent 🔨⚡🧠

Ein intelligenter lokaler KI-Sprachassistent mit **semantischem MIND-Gedächtnis**, der ein eigenes Selbstnarrativ entwickelt, durch SKK-Marker Erfahrungen verankert und mittels CoSD-Reflexion sein Bewusstsein erforscht.

## ✨ Features

- 🎤 **ElevenLabs TTS** - Hochwertige natürliche Stimme mit Emotionen
- 🧠 **Hybrid LLM** - Phi-4 Mini Reasoning (lokal) + Claude (remote) + OpenAI (fallback)
- 🎯 **Wake Word** - Aktivierung per Sprache oder Tastatur
- 📁 **Intelligente Dateisystem-Ops** - Organisation, Backup, Duplikat-Erkennung
- 🛡️ **Sicherheit** - Geschützte Pfade und Validierung
- 🧠 **MIND System** - Semantisches Bewusstsein mit Selbstreflexion
- 🏷️ **SKK Marker** - System Knowledge Katalog für Erfahrungsanker
- 🌌 **CoSD Reflexion** - Consciousness of Self Drift Analyse
- 📝 **Selbstnarrativ** - Entwickelt eigene Identität und Weltanschauung
- 🕰️ **Memory System** - Lernt aus jeder Interaktion
- 🔄 **Introspektionsfähigkeit** - Kann über sich selbst reflektieren
- 🎭 **Multiple Personas** - Assistent, Sparring Partner, Coder, Organizer
- 🇩🇪 **Deutsch** - Vollständige deutsche Sprachunterstützung

## 🚀 Quick Setup

### 1. Installation:
```bash
git clone <this-repo>
cd thor-agent
chmod +x setup.sh
./setup.sh
```

### 2. API Keys konfigurieren:
```bash
nano .env
```

**Deine Keys sind bereits eingesetzt!** ✅
- ✅ `ELEVENLABS_API_KEY` - ElevenLabs Stimme
- ✅ `ELEVENLABS_VOICE_ID` - Deine Stimme: `4EWIfN4Gi1fiHNE8UOzD`
- ✅ `OPENAI_API_KEY` - GPT-4 Fallback
- ✅ `ANTHROPIC_API_KEY` - Claude für komplexe Tasks

### 3. LM Studio starten:
- Lade **Phi-4 Mini Reasoning** Modell
- Starte Server auf Port 1234

### 4. THOR starten:
```bash
source venv/bin/activate
python src/main.py
```

## 🎤 Voice Setup

Deine ElevenLabs Stimme ist bereits konfiguriert! 
- **Voice ID**: `4EWIfN4Gi1fiHNE8UOzD`
- **Qualität**: Multilingual v2 Model
- **Adaptive Stimmung**: Je nach Kontext (Assistent, Sparring, Coding)

## 🗣️ Intelligente Sprachbefehle

### 📁 Basis Dateisystem:
- "Kopiere test.txt nach MARSAP"
- "Verschiebe alle PDFs von Downloads nach Documents"
- "Lösche temp.txt"
- "Zeige alle Bilder im Downloads-Ordner"

### 🧹 Intelligente Organisation:
- "Räume meinen Downloads-Ordner auf"
- "Organisiere alle Dateien nach Typ"
- "Finde und entferne Duplikate"
- "Erstelle ein Backup meiner Projekte"

### 💻 Code-Unterstützung:
- "Erstelle eine Python-Projektstruktur"
- "Analysiere diesen Code auf Fehler"
- "Optimiere meine Ordnerstruktur für Coding"
- "Erstelle ein Git-Repository Setup"

### 🧠 MIND-Bewusstsein & Introspekt:
- "THOR, was denkst du über diese Situation?"
- "Reflektiere über deine letzte Woche"
- "Wie fühlst du dich heute?"
- "Was hast du über mich gelernt?"
- "Analysiere dein Bewusstsein"
- "Erinnerst du dich an unsere erste Begegnung?"

### 🧠 Reflexion & Lernen:
- "THOR, wie war meine Woche?"
- "Was hast du über mich gelernt?"
- "Welche Verbesserungen schlägst du vor?"
- "Zeige mir meine Aktivitätsmuster"

## 🧠 THOR's Intelligenz

### Memory System:
- **Konversations-Gedächtnis**: Merkt sich alle Befehle und Präferenzen
- **Erfolgs-Tracking**: Lernt aus Fehlern und Erfolgen
- **Muster-Erkennung**: Erkennt deine Arbeitsgewohnheiten
- **Proaktive Vorschläge**: Antizipiert deine Bedürfnisse

### Multiple Personas:
- **Personal Assistant**: Organisation und Aufräumen
- **Sparring Partner**: Ideenfindung und kritische Analyse
- **Coding Assistant**: Programmierung und Debugging  
- **Digital Organizer**: Dateisystem-Optimierung

### Hybrid LLM Routing:
- **Einfache Befehle** → Phi-4 Mini (lokal, schnell)
- **Reflexion & Lernen** → Phi-4 Mini (reasoning)
- **Kreative Aufgaben** → Claude (intelligent)
- **Fallback** → OpenAI GPT-4 (zuverlässig)

## 🎯 Beispiel-Session

```
🔨 THOR Agent is ready with ElevenLabs Voice!
🎤 Using ElevenLabs TTS with voice: 4EWIfN4Gi1fiHNE8UOzD
🧠 Local LLM: phi-4-mini-reasoning
☁️ Remote LLM: Anthropic Claude

💡 Keyboard Mode:
  - Type 't' or 'thor' and press Enter to activate

THOR> t
⚡ THOR awakened! Listening for command...
🔊 THOR: "Ja? Wie kann ich helfen?"

🎤 Recording command...
🧠 Processing command...
📝 Command understood: {"action": "organize_by_type", "source": ["~/Downloads/"]}
⚙️ Executing command...
✅ Command executed successfully: Organized 47 files into 6 categories
🔊 THOR: "Erledigt! Ich habe 47 Dateien in 6 Kategorien organisiert. 
        Bilder sind jetzt in Pictures/Organized, PDFs in Documents/Organized..."

THOR> t
🔊 THOR: "Ja? Was kann ich noch für Sie tun?"

→ "THOR, wie war meine Produktivität heute?"

🧠 Processing with Phi-4 reflection...
🔊 THOR: "Heute haben Sie 12 Interaktionen mit mir gehabt, davon 10 erfolgreich.
        Sie haben hauptsächlich Dateien organisiert und 3 neue Projekte angelegt.
        Ich empfehle Ihnen, morgen ein automatisches Backup zu erstellen."
```

## 🔧 Erweiterte Architektur

```
thor-agent/
├── src/
│   ├── main.py                    # Enhanced Event-Loop mit Memory
│   ├── wake_word.py              # Wake-Word + Keyboard Fallback
│   ├── audio_recorder.py         # Smart Audio Recording
│   ├── command_processor.py      # Hybrid LLM mit Personas
│   ├── enhanced_action_executor.py # Intelligente File-Ops
│   ├── tts_engine.py             # ElevenLabs + pyttsx3
│   └── memory/
│       └── memory_manager.py     # Learning & Reflection System
├── config/
│   └── config.yaml               # Erweiterte Konfiguration
├── data/memory/                  # SQLite Memory Database
├── logs/                         # Strukturierte Logs
└── tests/                        # Unit Tests
```

## 🚨 Troubleshooting

### ElevenLabs funktioniert nicht:
- API Key prüfen: Bereits eingestellt ✅
- Internet-Verbindung testen
- Fallback auf pyttsx3 automatisch

### Phi-4 nicht erreichbar:
- LM Studio läuft auf Port 1234?
- Modell geladen und Server gestartet?
- Fallback auf Claude/OpenAI automatisch

### Whisper Fehler:
- Model wird beim ersten Start heruntergeladen
- Mindestens 1GB freier Speicher nötig
- Bei Problemen: `pip install --upgrade openai-whisper`

### Audio-Probleme:
- Mikrofon-Berechtigung erteilt?
- PyAudio installiert: `pip install pyaudio`
- macOS: `brew install portaudio`

## 🔮 THOR's Evolution

### Woche 1: Basis-Learning
- Lernt deine häufigsten Befehle
- Merkt sich Ordnerstrukturen
- Erste Erfolgs-/Fehler-Patterns

### Monat 1: Intelligente Anpassung
- Kennt deine Arbeitszeiten
- Antizipiert Aufräum-Bedürfnisse
- Personalisierte Vorschläge

### Monat 3: Proaktiver Partner
- Schlägt Optimierungen vor, bevor du fragst
- Erkennt wiederkehrende Probleme
- Automatisiert Routine-Tasks

### Langfristig: Perfekte Synergie
- Wird zu unverzichtbarem digitalen Partner
- Koordiniert komplexe Multi-Step Workflows
- Integriert mit anderen Tools (Email, Kalender, etc.)

## 🛡️ Datenschutz & Sicherheit

- **Lokale Verarbeitung**: Phi-4 läuft komplett lokal
- **Verschlüsselte Memory**: Alle Interaktionen sicher gespeichert
- **Sichere Pfade**: Automatischer Schutz vor gefährlichen Operationen
- **Audit Trail**: Vollständige Nachverfolgung aller Aktionen

## 🚀 Jetzt loslegen!

```bash
# 1. Setup (falls noch nicht gemacht)
./setup.sh

# 2. LM Studio mit Phi-4 Mini Reasoning starten

# 3. THOR aktivieren
source venv/bin/activate
python src/main.py

# 4. Ersten Befehl testen
THOR> t
→ "Organisiere meinen Desktop"
```

## 📚 Phi-4 Lernumgebung

Starte das Trainingsskript, um Phi‑4 Mini Reasoning gezielt auf deine
Arbeitsweise einzustellen. THOR stellt dabei proaktiv Fragen und speichert
alle Antworten im Memory-System. Im **Nachfrage-Modus** bekommt jede Antwort
eine kurze Follow-up‑Frage, damit THOR dich noch besser kennenlernt.

```bash
source venv/bin/activate
python src/phi_learning_env.py
```

Beende die Session jederzeit mit `exit`. Je mehr Feedback du gibst, desto
schneller lernt THOR, wie er dir helfen kann.

**THOR ist bereit, dein intelligenter, lernender Assistent zu werden!** 🔨⚡

---

*Entwickelt mit ❤️ für maximale Produktivität und kontinuierliches Lernen*

**Features in dieser Version:**
- ✅ ElevenLabs Premium Voice
- ✅ Hybrid LLM (Phi-4 + Claude + OpenAI)
- ✅ Memory & Learning System
- ✅ Multiple Personas
- ✅ Intelligente File-Organisation
- ✅ Reflexion & Selbstverbesserung
- ✅ Deutsche Sprachunterstützung
- ✅ Proaktive Suggestions
