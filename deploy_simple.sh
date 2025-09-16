#!/bin/bash

echo "🌐 Déploiement Public Simplifié - IA d'Étude"
echo "============================================"
echo ""

# Arrêter les instances précédentes
pkill -f "python main.py" 2>/dev/null
pkill -f "ngrok" 2>/dev/null

# Activer l'environnement virtuel
source venv/bin/activate

# Créer les dossiers
mkdir -p uploads sessions static

echo "🚀 Lancement de l'application..."

# Lancer l'application
python main.py &
APP_PID=$!

echo "📝 PID de l'application : $APP_PID"
echo "⏳ Attente du démarrage..."
sleep 5

# Vérifier si l'app fonctionne
if curl -s http://localhost:8000/ > /dev/null; then
    echo "✅ Application démarrée !"
    echo ""
    echo "🔗 Création du tunnel public..."
    
    # Lancer ngrok
    ngrok http 8000 &
    NGROK_PID=$!
    
    echo "📝 PID de ngrok : $NGROK_PID"
    echo ""
    echo "🎉 VOTRE IA D'ÉTUDE EST MAINTENANT ACCESSIBLE !"
    echo "=============================================="
    echo ""
    echo "🌐 URLs d'accès :"
    echo "  • Local  : http://localhost:8000"
    echo "  • Public : Consultez la console ngrok ci-dessous"
    echo ""
    echo "📱 Partagez l'URL publique ngrok avec qui vous voulez !"
    echo ""
    echo "🎯 Fonctionnalités disponibles :"
    echo "  • Upload de fichiers (PDF, DOCX, TXT, MD)"
    echo "  • Génération de résumés intelligents"
    echo "  • Création de questions d'étude"
    echo "  • Quiz interactifs personnalisables"
    echo "  • Cartes mémoire pour la révision"
    echo ""
    echo "📋 Pour arrêter :"
    echo "  Ctrl+C dans ce terminal ou ./stop_public.sh"
    echo ""
    
    # Créer script d'arrêt
    cat > stop_public.sh << EOF
#!/bin/bash
echo "🛑 Arrêt de l'IA d'Étude publique..."
kill $APP_PID 2>/dev/null
kill $NGROK_PID 2>/dev/null
pkill -f "python main.py" 2>/dev/null
pkill -f "ngrok" 2>/dev/null
echo "✅ Application arrêtée"
EOF
    chmod +x stop_public.sh
    
    echo "🎮 Script d'arrêt créé : ./stop_public.sh"
    echo ""
    echo "⬇️  CONSOLE NGROK (URL publique ci-dessous) :"
    echo "=" * 50
    
    # Attendre les processus
    wait
    
else
    echo "❌ Erreur : Impossible de démarrer l'application"
    exit 1
fi