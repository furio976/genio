#!/usr/bin/env python3
"""
IA Génératrice de Vidéos Quotidiennes
====================================

Ce programme génère automatiquement des vidéos quotidiennes en utilisant l'IA.
Il combine la génération de contenu avec OpenAI, la synthèse vocale, et la création vidéo.

Usage:
    python main.py                    # Mode interactif
    python main.py --generate-now     # Générer une vidéo immédiatement
    python main.py --start-daemon     # Démarrer en mode daemon
    python main.py --help             # Afficher l'aide
"""

import argparse
import sys
import os
from datetime import datetime

from config import Config
from content_generator import ContentGenerator
from video_generator import VideoGenerator
from scheduler import VideoScheduler, VideoSchedulerManager

def setup_environment():
    """Setup the environment and check requirements"""
    try:
        # Check if .env file exists
        if not os.path.exists('.env'):
            print("⚠️  Fichier .env manquant!")
            print("📋 Copiez .env.example vers .env et configurez vos paramètres:")
            print("   cp .env.example .env")
            print("   # Puis éditez .env avec vos clés API")
            return False
        
        # Validate configuration
        Config.validate_config()
        Config.ensure_directories()
        
        print("✅ Configuration validée")
        return True
        
    except Exception as e:
        print(f"❌ Erreur de configuration: {e}")
        return False

def generate_single_video():
    """Generate a single video immediately"""
    print("🎬 Génération d'une vidéo...")
    
    try:
        content_gen = ContentGenerator()
        video_gen = VideoGenerator()
        
        # Generate content
        content_data = content_gen.generate_daily_content()
        print(f"📝 Contenu généré: {content_data['title']}")
        
        # Create video
        video_path = video_gen.create_video(content_data)
        
        if video_path:
            video_info = video_gen.get_video_info(video_path)
            print(f"✅ Vidéo créée avec succès!")
            print(f"📁 Chemin: {video_path}")
            if video_info:
                print(f"⏱️  Durée: {video_info['duration']:.1f}s")
                print(f"💾 Taille: {video_info['file_size'] / (1024*1024):.1f} MB")
            return True
        else:
            print("❌ Échec de la création de la vidéo")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def start_daemon():
    """Start the scheduler in daemon mode"""
    print("🤖 Démarrage du mode daemon...")
    
    scheduler = VideoScheduler()
    
    try:
        scheduler.start()
        print(f"⏰ Planificateur démarré - génération quotidienne à {Config.DAILY_SCHEDULE_TIME}")
        print("🔄 Appuyez sur Ctrl+C pour arrêter")
        
        # Keep the program running
        import time
        while True:
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du daemon...")
        scheduler.stop()
        print("✅ Daemon arrêté")

def show_status():
    """Show current system status"""
    print("📊 Statut du système:")
    print(f"   📁 Répertoire de sortie: {Config.OUTPUT_DIRECTORY}")
    print(f"   🎯 Catégorie de contenu: {Config.VIDEO_TOPIC_CATEGORY}")
    print(f"   🗣️  Langue: {Config.CONTENT_LANGUAGE}")
    print(f"   ⏰ Heure planifiée: {Config.DAILY_SCHEDULE_TIME}")
    print(f"   🎞️  Durée vidéo: {Config.VIDEO_DURATION}s")
    print(f"   📐 Résolution: {Config.VIDEO_WIDTH}x{Config.VIDEO_HEIGHT}")
    
    # Check if today's video exists
    today_file = os.path.join(Config.OUTPUT_DIRECTORY, Config.get_daily_filename())
    if os.path.exists(today_file):
        print(f"   ✅ Vidéo d'aujourd'hui: {today_file}")
    else:
        print(f"   ⏳ Vidéo d'aujourd'hui: pas encore générée")

def main():
    parser = argparse.ArgumentParser(
        description="IA Génératrice de Vidéos Quotidiennes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python main.py                    # Mode interactif
  python main.py --generate-now     # Générer maintenant
  python main.py --daemon           # Mode daemon
  python main.py --status           # Voir le statut
        """
    )
    
    parser.add_argument(
        '--generate-now', 
        action='store_true',
        help='Générer une vidéo immédiatement'
    )
    
    parser.add_argument(
        '--daemon', 
        action='store_true',
        help='Démarrer en mode daemon (arrière-plan)'
    )
    
    parser.add_argument(
        '--status', 
        action='store_true',
        help='Afficher le statut du système'
    )
    
    args = parser.parse_args()
    
    # Show banner
    print("🎥 IA GÉNÉRATRICE DE VIDÉOS QUOTIDIENNES")
    print("=" * 40)
    
    # Setup environment
    if not setup_environment():
        sys.exit(1)
    
    # Handle command line arguments
    if args.status:
        show_status()
        
    elif args.generate_now:
        success = generate_single_video()
        sys.exit(0 if success else 1)
        
    elif args.daemon:
        start_daemon()
        
    else:
        # Interactive mode
        manager = VideoSchedulerManager()
        manager.run_interactive()

if __name__ == "__main__":
    main()