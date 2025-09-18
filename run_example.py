#!/usr/bin/env python3
"""
Exemple d'utilisation de l'IA Génératrice de Vidéos
==================================================

Ce script montre comment utiliser les composants individuellement
pour générer une vidéo de démonstration.
"""

import os
from config import Config
from content_generator import ContentGenerator
from video_generator import VideoGenerator

def create_demo_video():
    """Créer une vidéo de démonstration"""
    
    print("🎬 Création d'une vidéo de démonstration...")
    
    # Vérifier la configuration
    try:
        Config.validate_config()
        Config.ensure_directories()
    except Exception as e:
        print(f"❌ Erreur de configuration: {e}")
        print("💡 Assurez-vous d'avoir configuré votre fichier .env")
        return False
    
    # Initialiser les générateurs
    content_gen = ContentGenerator()
    video_gen = VideoGenerator()
    
    try:
        # Générer le contenu
        print("📝 Génération du contenu...")
        content_data = content_gen.generate_daily_content()
        
        if not content_data:
            print("❌ Échec de la génération du contenu")
            return False
        
        print(f"✅ Contenu généré:")
        print(f"   Titre: {content_data['title']}")
        print(f"   Mots-clés: {content_data['keywords']}")
        print(f"   Script: {len(content_data['script'])} caractères")
        
        # Créer la vidéo
        print("🎞️ Création de la vidéo...")
        video_path = video_gen.create_video(content_data)
        
        if video_path:
            # Obtenir les informations de la vidéo
            video_info = video_gen.get_video_info(video_path)
            
            print(f"✅ Vidéo créée avec succès!")
            print(f"📁 Chemin: {video_path}")
            
            if video_info:
                print(f"⏱️ Durée: {video_info['duration']:.1f} secondes")
                print(f"📐 Résolution: {video_info['size'][0]}x{video_info['size'][1]}")
                print(f"💾 Taille du fichier: {video_info['file_size'] / (1024*1024):.1f} MB")
            
            return video_path
        else:
            print("❌ Échec de la création de la vidéo")
            return False
    
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        return False

def create_custom_video():
    """Créer une vidéo avec contenu personnalisé"""
    
    print("🎨 Création d'une vidéo personnalisée...")
    
    # Contenu personnalisé
    custom_content = {
        'title': 'Bienvenue dans l\'IA Génératrice de Vidéos!',
        'script': '''
        Bonjour et bienvenue! Cette vidéo a été entièrement générée par intelligence artificielle.
        
        Notre système combine plusieurs technologies avancées pour créer du contenu vidéo automatiquement.
        
        Nous utilisons GPT-4 pour générer des scripts engageants, Google Text-to-Speech pour la narration,
        et Python avec MoviePy pour l'assemblage vidéo final.
        
        Cette démonstration prouve que l'IA peut créer du contenu éducatif de qualité de manière autonome.
        
        Merci de votre attention et à bientôt pour de nouvelles créations automatisées!
        ''',
        'keywords': 'ia, intelligence artificielle, vidéo, automatisation, démonstration'
    }
    
    try:
        Config.ensure_directories()
        video_gen = VideoGenerator()
        
        # Créer la vidéo personnalisée
        video_path = video_gen.create_video(custom_content)
        
        if video_path:
            print(f"✅ Vidéo personnalisée créée: {video_path}")
            return video_path
        else:
            print("❌ Échec de la création de la vidéo personnalisée")
            return False
    
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    
    print("🎥 EXEMPLES D'UTILISATION - IA GÉNÉRATRICE DE VIDÉOS")
    print("=" * 55)
    
    while True:
        print("\nOptions disponibles:")
        print("1. Créer une vidéo de démonstration (avec IA)")
        print("2. Créer une vidéo personnalisée (contenu fixe)")
        print("3. Voir la configuration actuelle")
        print("4. Quitter")
        
        choice = input("\nVotre choix (1-4): ").strip()
        
        if choice == '1':
            result = create_demo_video()
            if result:
                print(f"\n🎉 Succès! Vidéo disponible dans: {result}")
        
        elif choice == '2':
            result = create_custom_video()
            if result:
                print(f"\n🎉 Succès! Vidéo personnalisée créée: {result}")
        
        elif choice == '3':
            print(f"\n📋 Configuration actuelle:")
            print(f"   Répertoire de sortie: {Config.OUTPUT_DIRECTORY}")
            print(f"   Catégorie de contenu: {Config.VIDEO_TOPIC_CATEGORY}")
            print(f"   Langue: {Config.CONTENT_LANGUAGE}")
            print(f"   Durée vidéo: {Config.VIDEO_DURATION}s")
            print(f"   Résolution: {Config.VIDEO_WIDTH}x{Config.VIDEO_HEIGHT}")
            
            # Vérifier si les répertoires existent
            if os.path.exists(Config.OUTPUT_DIRECTORY):
                videos = [f for f in os.listdir(Config.OUTPUT_DIRECTORY) if f.endswith('.mp4')]
                print(f"   Vidéos existantes: {len(videos)}")
            else:
                print(f"   Répertoire de sortie: non créé")
        
        elif choice == '4':
            print("\n👋 Au revoir!")
            break
        
        else:
            print("❌ Choix invalide, veuillez réessayer.")

if __name__ == "__main__":
    main()