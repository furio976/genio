#!/bin/bash
# Script d'installation des dépendances pour le générateur de vidéo quotidienne

set -e

echo "🚀 Installation des dépendances pour le générateur de vidéo quotidienne"
echo "=================================================================="

# Vérifier si on est sur Ubuntu/Debian
if ! command -v apt-get &> /dev/null; then
    echo "❌ Ce script est conçu pour Ubuntu/Debian. Veuillez installer manuellement:"
    echo "   - Python 3.8+"
    echo "   - ffmpeg"
    echo "   - espeak-ng"
    echo "   - libespeak1"
    exit 1
fi

# Mettre à jour les paquets
echo "📦 Mise à jour des paquets système..."
sudo apt-get update -y

# Installer les dépendances système
echo "🔧 Installation des dépendances système..."
sudo apt-get install -y \
    python3 \
    python3-venv \
    python3-pip \
    ffmpeg \
    espeak-ng \
    libespeak1 \
    libportaudio2

# Créer l'environnement virtuel
echo "🐍 Création de l'environnement virtuel Python..."
python3 -m venv .venv

# Activer l'environnement et installer les dépendances Python
echo "📚 Installation des dépendances Python..."
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

echo ""
echo "✅ Installation terminée !"
echo ""
echo "🚀 Pour utiliser le générateur:"
echo "   source .venv/bin/activate"
echo "   python generate_daily_video.py --topic 'Mon sujet' --slides 5"
echo ""
echo "📅 Pour la planification quotidienne (cron):"
echo "   crontab -e"
echo "   # Ajouter cette ligne pour 9h chaque jour:"
echo "   0 9 * * * cd $(pwd) && $(pwd)/.venv/bin/python $(pwd)/generate_daily_video.py --topic 'Actu du jour' --slides 5 --out $(pwd)/output --basename daily_video >> $(pwd)/cron.log 2>&1"