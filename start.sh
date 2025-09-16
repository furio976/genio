#!/bin/bash

echo "🧠 Démarrage de l'IA d'Étude Personnalisée..."
echo "=============================================="

# Activer l'environnement virtuel
source venv/bin/activate

# Créer les dossiers nécessaires
mkdir -p uploads sessions static

echo "✅ Environnement préparé"
echo "🚀 Lancement de l'application..."
echo ""
echo "🌐 L'application sera accessible sur : http://localhost:8000"
echo "📁 Vous pouvez tester avec le fichier : test_cours.txt"
echo ""
echo "💡 Mode démo activé (pas de clé API OpenAI requise)"
echo "   Pour utiliser l'IA complète, ajoutez votre clé dans le fichier .env"
echo ""

# Lancer l'application
python main.py