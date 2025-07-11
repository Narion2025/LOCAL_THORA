#!/bin/bash
# THOR Agent - Einfacher Start

echo "🔨 Starte THOR mit ElevenLabs Voice nF9mrdeA89H7gsev6yt0..."

# Gehe ins Projektverzeichnis
cd "$(dirname "$0")"

# Setze PYTHONPATH und starte THOR
cd src
export PYTHONPATH=.
python3 main.py
