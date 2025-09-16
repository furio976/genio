#!/bin/bash

echo "🌐 Création du Tunnel Public pour votre IA d'Étude"
echo "================================================="
echo ""

# Vérifier si l'application tourne
if ! pgrep -f "python main.py" > /dev/null; then
    echo "⚠️  L'application n'est pas démarrée"
    echo "🚀 Démarrage de l'application..."
    cd /workspace
    source venv/bin/activate
    python main.py &
    sleep 5
    echo "✅ Application démarrée"
fi

# Vérifier si ngrok est installé
if ! command -v ngrok &> /dev/null; then
    echo "❌ Ngrok n'est pas installé"
    echo "🔧 Installation de ngrok..."
    wget -q https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz -O ngrok.tgz
    tar -xzf ngrok.tgz
    sudo mv ngrok /usr/local/bin/
    rm ngrok.tgz
    echo "✅ Ngrok installé"
fi

echo ""
echo "🔗 Création du tunnel public..."
echo "⏳ Génération de votre URL publique..."
echo ""
echo "🎯 Une fois lancé, votre IA sera accessible mondialement !"
echo "📱 Partagez l'URL générée avec qui vous voulez"
echo ""
echo "🛑 Pour arrêter : Ctrl+C"
echo ""
echo "🌐 Lancement du tunnel ngrok..."
echo "=" * 50

# Lancer ngrok
ngrok http 8000