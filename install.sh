#!/bin/bash

# Script d'installation automatique pour l'IA Génératrice de Vidéos
# =================================================================

set -e

echo "🎥 INSTALLATION - IA GÉNÉRATRICE DE VIDÉOS"
echo "=========================================="

# Vérifier Python
echo "🐍 Vérification de Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python $PYTHON_VERSION détecté"

# Vérifier pip
echo "📦 Vérification de pip..."
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi
echo "✅ pip3 disponible"

# Créer un environnement virtuel (optionnel mais recommandé)
echo "🏠 Configuration de l'environnement..."
if [ ! -d "venv" ]; then
    echo "📁 Création de l'environnement virtuel..."
    python3 -m venv venv
    echo "✅ Environnement virtuel créé"
else
    echo "✅ Environnement virtuel existant trouvé"
fi

# Activer l'environnement virtuel
echo "🔄 Activation de l'environnement virtuel..."
source venv/bin/activate

# Mettre à jour pip
echo "⬆️ Mise à jour de pip..."
pip install --upgrade pip

# Installer les dépendances
echo "📚 Installation des dépendances..."
pip install -r requirements.txt

# Créer le fichier .env s'il n'existe pas
if [ ! -f ".env" ]; then
    echo "⚙️ Création du fichier de configuration..."
    cp .env.example .env
    echo "✅ Fichier .env créé à partir de .env.example"
    echo "⚠️  IMPORTANT: Éditez le fichier .env pour ajouter votre clé API OpenAI"
else
    echo "✅ Fichier .env existant trouvé"
fi

# Créer les répertoires nécessaires
echo "📁 Création des répertoires..."
mkdir -p videos
mkdir -p temp
echo "✅ Répertoires créés"

# Rendre les scripts exécutables
echo "🔧 Configuration des permissions..."
chmod +x main.py
chmod +x run_example.py
chmod +x install.sh
echo "✅ Permissions configurées"

echo ""
echo "🎉 INSTALLATION TERMINÉE!"
echo "========================"
echo ""
echo "📋 Prochaines étapes:"
echo "1. Éditez le fichier .env pour ajouter votre clé API OpenAI:"
echo "   nano .env"
echo ""
echo "2. Testez l'installation avec un exemple:"
echo "   python3 run_example.py"
echo ""
echo "3. Lancez le programme principal:"
echo "   python3 main.py"
echo ""
echo "📖 Consultez README.md pour plus d'informations."
echo ""
echo "🤖 Bon génération de vidéos!"