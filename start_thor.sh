#!/bin/bash

# THOR Startskript
echo "🔨 Starte THOR Agent..."
echo "=============================================="

# Aktiviere virtuelle Umgebung
source venv/bin/activate

# Starte THOR mit interaktiver GUI und Sprachausgabe
cd src && python3 thor_interactive_voice.py

echo "=============================================="
echo "THOR wurde beendet."
