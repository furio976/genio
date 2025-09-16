#!/bin/bash
echo "🛑 Arrêt de l'IA d'Étude publique..."
kill 7164 2>/dev/null
kill 7250 2>/dev/null
pkill -f "python main.py" 2>/dev/null
pkill -f "ngrok" 2>/dev/null
echo "✅ Application arrêtée"
