#!/bin/bash
# Script de configuration du cron pour la génération quotidienne automatique

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_PATH="$SCRIPT_DIR/.venv/bin/python"
GENERATOR_SCRIPT="$SCRIPT_DIR/generate_daily_video.py"
OUTPUT_DIR="$SCRIPT_DIR/output"
LOG_FILE="$SCRIPT_DIR/cron.log"

echo "⏰ Configuration du cron pour la génération quotidienne automatique"
echo "================================================================="

# Vérifier que les fichiers existent
if [ ! -f "$PYTHON_PATH" ]; then
    echo "❌ Environnement Python non trouvé. Exécutez d'abord:"
    echo "   ./install_dependencies.sh"
    exit 1
fi

if [ ! -f "$GENERATOR_SCRIPT" ]; then
    echo "❌ Script générateur non trouvé: $GENERATOR_SCRIPT"
    exit 1
fi

# Créer le dossier de sortie
mkdir -p "$OUTPUT_DIR"

# Demander l'heure de génération
echo ""
echo "🕐 À quelle heure voulez-vous générer la vidéo quotidienne ?"
echo "   Format: HH (ex: 09 pour 9h00, 14 pour 14h00)"
read -p "Heure (défaut: 09): " HOUR
HOUR=${HOUR:-09}

# Valider l'heure
if ! [[ "$HOUR" =~ ^[0-9]{1,2}$ ]] || [ "$HOUR" -gt 23 ]; then
    echo "❌ Heure invalide. Utilisation de 09h00 par défaut."
    HOUR="09"
fi

# Demander le sujet par défaut
echo ""
echo "📝 Quel sera le sujet par défaut des vidéos ?"
read -p "Sujet (défaut: 'Actu du jour'): " TOPIC
TOPIC=${TOPIC:-"Actu du jour"}

# Demander le nombre de slides
echo ""
echo "📊 Combien de slides par vidéo ?"
read -p "Nombre de slides (défaut: 5): " SLIDES
SLIDES=${SLIDES:-5}

# Créer la commande cron
CRON_COMMAND="0 $HOUR * * * cd $SCRIPT_DIR && $PYTHON_PATH $GENERATOR_SCRIPT --topic '$TOPIC' --slides $SLIDES --out $OUTPUT_DIR --basename daily_video --cleanup >> $LOG_FILE 2>&1"

echo ""
echo "📋 Commande cron qui sera ajoutée:"
echo "   $CRON_COMMAND"
echo ""

# Demander confirmation
read -p "Voulez-vous ajouter cette tâche au cron ? (y/N): " CONFIRM
if [[ $CONFIRM =~ ^[Yy]$ ]]; then
    # Sauvegarder le cron actuel
    crontab -l > /tmp/current_cron 2>/dev/null || touch /tmp/current_cron
    
    # Ajouter la nouvelle tâche
    echo "$CRON_COMMAND" >> /tmp/current_cron
    
    # Installer le nouveau cron
    crontab /tmp/current_cron
    rm /tmp/current_cron
    
    echo "✅ Tâche cron ajoutée avec succès !"
    echo ""
    echo "📅 La vidéo sera générée automatiquement tous les jours à ${HOUR}h00"
    echo "📁 Vidéos sauvegardées dans: $OUTPUT_DIR"
    echo "📝 Logs dans: $LOG_FILE"
    echo ""
    echo "🔍 Pour vérifier les tâches cron:"
    echo "   crontab -l"
    echo ""
    echo "🧪 Pour tester manuellement:"
    echo "   source .venv/bin/activate"
    echo "   python generate_daily_video.py --topic '$TOPIC' --slides $SLIDES"
else
    echo "❌ Configuration annulée."
    echo ""
    echo "💡 Pour configurer manuellement, ajoutez cette ligne à votre crontab:"
    echo "   crontab -e"
    echo "   $CRON_COMMAND"
fi