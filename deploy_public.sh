#!/bin/bash

echo "🌐 Déploiement Public de l'IA d'Étude"
echo "===================================="
echo ""

# Vérifier si l'application tourne déjà
if pgrep -f "python main.py" > /dev/null; then
    echo "⚠️  Application déjà en cours d'exécution"
    echo "🔄 Arrêt de l'instance précédente..."
    pkill -f "python main.py"
    sleep 2
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Créer les dossiers nécessaires
mkdir -p uploads sessions static

# Lancer l'application en arrière-plan
echo "🚀 Lancement de l'application..."
nohup python main.py > app.log 2>&1 &
APP_PID=$!

# Attendre que l'application démarre
echo "⏳ Démarrage en cours..."
sleep 5

# Vérifier si l'application fonctionne
if curl -s http://localhost:8000/ > /dev/null; then
    echo "✅ Application démarrée avec succès !"
    echo ""
    echo "🌐 VOTRE IA D'ÉTUDE EST MAINTENANT PUBLIQUE !"
    echo "============================================="
    echo ""
    
    # Lancer ngrok pour créer un tunnel public
    echo "🔗 Création du tunnel public avec ngrok..."
    echo "⏳ Génération de l'URL publique..."
    
    # Lancer ngrok en arrière-plan
    nohup ngrok http 8000 --log=stdout > ngrok.log 2>&1 &
    NGROK_PID=$!
    
    # Attendre que ngrok démarre
    sleep 10
    
    # Extraire l'URL publique
    PUBLIC_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o 'https://[^"]*\.ngrok-free\.app')
    
    if [ ! -z "$PUBLIC_URL" ]; then
        echo ""
        echo "🎉 SUCCÈS ! Votre IA d'étude est accessible publiquement :"
        echo ""
        echo "🔗 URL PUBLIQUE : $PUBLIC_URL"
        echo ""
        echo "📱 Partagez cette URL avec qui vous voulez !"
        echo "🌍 Accessible depuis n'importe où dans le monde"
        echo "🔒 Sécurisé avec HTTPS"
        echo ""
        echo "📊 Fonctionnalités disponibles :"
        echo "  • Upload de fichiers (PDF, DOCX, TXT, MD)"
        echo "  • Génération de résumés"
        echo "  • Création de questions d'étude"
        echo "  • Quiz interactifs"
        echo "  • Cartes mémoire"
        echo ""
        echo "🎯 Fichier de test inclus : test_cours.txt"
        echo ""
        
        # Sauvegarder l'URL dans un fichier
        echo "$PUBLIC_URL" > public_url.txt
        
        echo "💾 URL sauvegardée dans : public_url.txt"
        echo ""
        echo "📋 Commandes utiles :"
        echo "  • Voir les logs : tail -f app.log"
        echo "  • Arrêter : ./stop_public.sh"
        echo "  • Redémarrer : ./deploy_public.sh"
        echo ""
        
    else
        echo "⚠️  Impossible d'obtenir l'URL publique ngrok"
        echo "🔧 Vérifiez les logs : tail -f ngrok.log"
        echo "💡 Vous pouvez toujours accéder localement : http://localhost:8000"
    fi
    
    # Créer un script d'arrêt
    cat > stop_public.sh << 'EOF'
#!/bin/bash
echo "🛑 Arrêt de l'IA d'Étude publique..."
pkill -f "python main.py"
pkill -f "ngrok"
echo "✅ Application arrêtée"
EOF
    chmod +x stop_public.sh
    
    echo "🎮 Pour arrêter l'application publique : ./stop_public.sh"
    
else
    echo "❌ Erreur : L'application n'a pas pu démarrer"
    echo "🔍 Vérifiez les logs : tail -f app.log"
    exit 1
fi

echo ""
echo "🎉 Déploiement terminé ! Votre IA d'étude est en ligne !"