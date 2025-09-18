#!/usr/bin/env python3
"""
🎬 GÉNÉRATEUR DE VIDÉO QUOTIDIENNE - TOUT EN UN
===============================================

Un script complet qui génère automatiquement des vidéos verticales quotidiennes
avec slides, narration TTS et planification cron.

Usage:
    python daily_video_generator.py install    # Installation des dépendances
    python daily_video_generator.py generate   # Génération manuelle
    python daily_video_generator.py setup      # Configuration cron
    python daily_video_generator.py test       # Test du système
"""

import os
import sys
import subprocess
import argparse
import shutil
from datetime import date
from pathlib import Path
from typing import List, Dict, Tuple
import textwrap

# ============================================================================
# CONFIGURATION
# ============================================================================

DEFAULT_SIZE = (1080, 1920)  # Format vertical 9:16
BACKGROUND_COLOR = (18, 18, 18)
TITLE_COLOR = (255, 255, 255)
TEXT_COLOR = (220, 220, 220)
MARGIN = 80

# ============================================================================
# DÉPENDANCES ET INSTALLATION
# ============================================================================

def check_system_dependencies():
    """Vérifie et installe les dépendances système"""
    print("🔍 Vérification des dépendances système...")
    
    # Vérifier si on est sur Linux
    if sys.platform != "linux":
        print("❌ Ce script est conçu pour Linux. Installation manuelle requise.")
        return False
    
    # Vérifier les commandes système
    required_commands = ["python3", "pip3", "ffmpeg", "espeak-ng"]
    missing = []
    
    for cmd in required_commands:
        if not shutil.which(cmd):
            missing.append(cmd)
    
    if missing:
        print(f"❌ Commandes manquantes: {', '.join(missing)}")
        print("🔧 Installation des dépendances système...")
        
        try:
            # Mettre à jour les paquets
            subprocess.run(["sudo", "apt-get", "update", "-y"], check=True)
            
            # Installer les dépendances
            deps = [
                "python3", "python3-venv", "python3-pip",
                "ffmpeg", "espeak-ng", "libespeak1", "libportaudio2"
            ]
            subprocess.run(["sudo", "apt-get", "install", "-y"] + deps, check=True)
            
            print("✅ Dépendances système installées")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de l'installation: {e}")
            return False
    
    return True

def install_python_dependencies():
    """Installe les dépendances Python"""
    print("🐍 Installation des dépendances Python...")
    
    # Créer l'environnement virtuel
    venv_path = Path(".venv")
    if not venv_path.exists():
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
    
    # Activer l'environnement et installer les packages
    pip_path = venv_path / "bin" / "pip"
    python_path = venv_path / "bin" / "python"
    
    # Mettre à jour pip
    subprocess.run([str(pip_path), "install", "--upgrade", "pip", "setuptools", "wheel"], check=True)
    
    # Installer les packages requis
    packages = [
        "moviepy==1.0.3",
        "Pillow==10.4.0", 
        "pyttsx3==2.90",
        "numpy==1.26.4",
        "imageio==2.35.1",
        "imageio-ffmpeg==0.5.1"
    ]
    
    for package in packages:
        subprocess.run([str(pip_path), "install", package], check=True)
    
    print("✅ Dépendances Python installées")
    return str(python_path)

# ============================================================================
# GÉNÉRATION DE CONTENU
# ============================================================================

def generate_daily_script(topic: str = None, num_slides: int = 5) -> List[Dict[str, str]]:
    """Génère un script avec slides"""
    if not topic or topic.strip() == "":
        topic = f"Faits marquants du {date.today().isoformat()}"
    
    slides = []
    for i in range(1, num_slides + 1):
        slides.append({
            "title": f"{topic} — Partie {i}",
            "text": (
                f"Voici un point clé numéro {i} sur le sujet '{topic}'. "
                "Ceci est un texte généré automatiquement pour la vidéo du jour."
            )
        })
    return slides

# ============================================================================
# GÉNÉRATION DE SLIDES
# ============================================================================

def load_font(size: int):
    """Charge une police avec fallback"""
    try:
        from PIL import ImageFont
        for font_name in ["DejaVuSans-Bold.ttf", "Arial.ttf", "LiberationSans-Bold.ttf"]:
            try:
                return ImageFont.truetype(font_name, size=size)
            except:
                continue
        return ImageFont.load_default()
    except ImportError:
        print("❌ PIL non disponible. Installation en cours...")
        return None

def render_slides(slides: List[Dict[str, str]], out_dir: str) -> List[str]:
    """Génère les images de slides"""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("❌ PIL non disponible. Installation en cours...")
        return []
    
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    
    for idx, slide in enumerate(slides, start=1):
        img = Image.new("RGB", DEFAULT_SIZE, BACKGROUND_COLOR)
        draw = ImageDraw.Draw(img)
        
        title_font = load_font(72)
        body_font = load_font(44)
        
        if not title_font or not body_font:
            print("❌ Impossible de charger les polices")
            return []
        
        # Titre
        title = slide.get("title", "")
        title_wrapped = textwrap.fill(title, width=18)
        draw.text((MARGIN, MARGIN), title_wrapped, font=title_font, fill=TITLE_COLOR)
        
        # Corps du texte
        bbox = draw.multiline_textbbox((MARGIN, MARGIN), title_wrapped, font=title_font)
        title_height = bbox[3] - bbox[1]
        body_y = MARGIN + title_height + 40
        body = slide.get("text", "")
        body_wrapped = textwrap.fill(body, width=28)
        draw.multiline_text((MARGIN, body_y), body_wrapped, font=body_font, fill=TEXT_COLOR, spacing=8)
        
        path = os.path.join(out_dir, f"slide_{idx:02d}.png")
        img.save(path)
        paths.append(path)
    
    return paths

# ============================================================================
# SYNTHÈSE VOCALE
# ============================================================================

def synthesize_audios(texts: List[str], out_dir: str) -> List[str]:
    """Génère les fichiers audio avec TTS"""
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    
    # Essayer espeak-ng d'abord
    if shutil.which("espeak-ng"):
        print("🎵 Utilisation d'espeak-ng pour la synthèse vocale...")
        for idx, text in enumerate(texts, start=1):
            path = os.path.join(out_dir, f"audio_{idx:02d}.wav")
            cmd = ["espeak-ng", "-w", path, "-s", "170", "-v", "fr+f3", "-a", "200", text]
            try:
                subprocess.run(cmd, check=True)
                paths.append(path)
            except subprocess.CalledProcessError:
                print(f"❌ Erreur espeak-ng pour le texte {idx}")
                return []
    else:
        # Fallback sur pyttsx3
        print("🎵 Utilisation de pyttsx3 pour la synthèse vocale...")
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 170)
            engine.setProperty('volume', 1.0)
            
            for idx, text in enumerate(texts, start=1):
                path = os.path.join(out_dir, f"audio_{idx:02d}.wav")
                engine.save_to_file(text, path)
                engine.runAndWait()
                paths.append(path)
            engine.stop()
        except Exception as e:
            print(f"❌ Erreur pyttsx3: {e}")
            return []
    
    return paths

# ============================================================================
# ASSEMBLAGE VIDÉO
# ============================================================================

def assemble_video(slide_paths: List[str], audio_paths: List[str], out_path: str) -> str:
    """Assemble la vidéo finale"""
    try:
        from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
    except ImportError:
        print("❌ MoviePy non disponible")
        return ""
    
    if len(slide_paths) != len(audio_paths):
        print("❌ Nombre de slides et d'audio différent")
        return ""
    
    clips = []
    for img_path, audio_path in zip(slide_paths, audio_paths):
        try:
            audio = AudioFileClip(audio_path)
            img_clip = ImageClip(img_path).set_duration(audio.duration).set_audio(audio)
            img_clip = img_clip.set_fps(30)
            clips.append(img_clip)
        except Exception as e:
            print(f"❌ Erreur lors du traitement de {img_path}: {e}")
            return ""
    
    try:
        final = concatenate_videoclips(clips, method="compose")
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        final.write_videofile(out_path, fps=30, codec="libx264", audio_codec="aac")
        return out_path
    except Exception as e:
        print(f"❌ Erreur lors de l'assemblage: {e}")
        return ""

# ============================================================================
# GÉNÉRATION PRINCIPALE
# ============================================================================

def generate_video(topic: str = "", slides: int = 5, output_dir: str = "output", 
                  basename: str = "daily_video", cleanup: bool = False):
    """Fonction principale de génération de vidéo"""
    
    print("🎬 GÉNÉRATEUR DE VIDÉO QUOTIDIENNE")
    print("=" * 40)
    
    # Vérifier les dépendances
    if not check_system_dependencies():
        return False
    
    # Générer le script
    print("📝 Génération du script...")
    script = generate_daily_script(topic, slides)
    print(f"✅ Script généré avec {len(script)} slides")
    
    # Créer les dossiers
    date_str = date.today().strftime("%Y-%m-%d")
    work_dir = Path(output_dir) / date_str
    img_dir = work_dir / "images"
    audio_dir = work_dir / "audio"
    video_path = Path(output_dir) / f"{basename}_{date_str}.mp4"
    
    # Générer les slides
    print("🖼️  Génération des slides...")
    slide_paths = render_slides(script, str(img_dir))
    if not slide_paths:
        print("❌ Erreur lors de la génération des slides")
        return False
    print(f"✅ {len(slide_paths)} slides générées")
    
    # Générer l'audio
    print("🎵 Génération de l'audio...")
    texts = [s.get("text", "") for s in script]
    audio_paths = synthesize_audios(texts, str(audio_dir))
    if not audio_paths:
        print("❌ Erreur lors de la génération de l'audio")
        return False
    print(f"✅ {len(audio_paths)} fichiers audio générés")
    
    # Assembler la vidéo
    print("🎥 Assemblage de la vidéo...")
    assembled = assemble_video(slide_paths, audio_paths, str(video_path))
    if not assembled:
        print("❌ Erreur lors de l'assemblage de la vidéo")
        return False
    print(f"✅ Vidéo générée: {assembled}")
    
    # Nettoyage
    if cleanup:
        print("🧹 Nettoyage des fichiers temporaires...")
        shutil.rmtree(work_dir, ignore_errors=True)
        print("✅ Fichiers temporaires supprimés")
    
    # Informations finales
    if video_path.exists():
        size_mb = video_path.stat().st_size / (1024 * 1024)
        print(f"\n📊 INFORMATIONS DE LA VIDÉO:")
        print(f"   📁 Fichier: {video_path}")
        print(f"   📏 Taille: {size_mb:.1f} MB")
        print(f"   📅 Date: {date_str}")
        print(f"   🎬 Slides: {len(slide_paths)}")
        print(f"   🎵 Audio: {len(audio_paths)} segments")
    
    return True

# ============================================================================
# CONFIGURATION CRON
# ============================================================================

def setup_cron():
    """Configure la planification automatique"""
    print("⏰ CONFIGURATION DE LA PLANIFICATION AUTOMATIQUE")
    print("=" * 50)
    
    script_path = Path(__file__).absolute()
    python_path = script_path.parent / ".venv" / "bin" / "python"
    output_dir = script_path.parent / "output"
    
    if not python_path.exists():
        print("❌ Environnement Python non trouvé. Exécutez d'abord: install")
        return False
    
    # Créer le dossier de sortie
    output_dir.mkdir(exist_ok=True)
    
    # Demander l'heure
    print("\n🕐 À quelle heure voulez-vous générer la vidéo quotidienne ?")
    hour = input("Heure (défaut: 09): ").strip() or "09"
    
    if not hour.isdigit() or int(hour) > 23:
        print("❌ Heure invalide. Utilisation de 09h00.")
        hour = "09"
    
    # Demander le sujet
    print("\n📝 Quel sera le sujet par défaut des vidéos ?")
    topic = input("Sujet (défaut: 'Actu du jour'): ").strip() or "Actu du jour"
    
    # Demander le nombre de slides
    print("\n📊 Combien de slides par vidéo ?")
    slides = input("Nombre de slides (défaut: 5): ").strip() or "5"
    
    if not slides.isdigit():
        slides = "5"
    
    # Créer la commande cron
    cron_cmd = f"0 {hour} * * * cd {script_path.parent} && {python_path} {script_path} generate --topic '{topic}' --slides {slides} --out {output_dir} --basename daily_video --cleanup >> {script_path.parent}/cron.log 2>&1"
    
    print(f"\n📋 Commande cron qui sera ajoutée:")
    print(f"   {cron_cmd}")
    
    if input("\nVoulez-vous ajouter cette tâche au cron ? (y/N): ").lower() == 'y':
        try:
            # Sauvegarder le cron actuel
            result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
            current_cron = result.stdout if result.returncode == 0 else ""
            
            # Ajouter la nouvelle tâche
            new_cron = current_cron + "\n" + cron_cmd + "\n"
            
            # Installer le nouveau cron
            subprocess.run(["crontab", "-"], input=new_cron, text=True, check=True)
            
            print("✅ Tâche cron ajoutée avec succès !")
            print(f"📅 La vidéo sera générée automatiquement tous les jours à {hour}h00")
            print(f"📁 Vidéos sauvegardées dans: {output_dir}")
            print(f"📝 Logs dans: {script_path.parent}/cron.log")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de l'ajout du cron: {e}")
            return False
    else:
        print("❌ Configuration annulée.")
        print(f"\n💡 Pour configurer manuellement, ajoutez cette ligne à votre crontab:")
        print(f"   crontab -e")
        print(f"   {cron_cmd}")
    
    return True

# ============================================================================
# INTERFACE PRINCIPALE
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Générateur de vidéo quotidienne tout-en-un")
    subparsers = parser.add_subparsers(dest="command", help="Commandes disponibles")
    
    # Commande install
    subparsers.add_parser("install", help="Installer les dépendances")
    
    # Commande generate
    gen_parser = subparsers.add_parser("generate", help="Générer une vidéo")
    gen_parser.add_argument("--topic", default="", help="Sujet de la vidéo")
    gen_parser.add_argument("--slides", type=int, default=5, help="Nombre de slides")
    gen_parser.add_argument("--out", default="output", help="Dossier de sortie")
    gen_parser.add_argument("--basename", default="daily_video", help="Nom de base")
    gen_parser.add_argument("--cleanup", action="store_true", help="Nettoyer les fichiers temporaires")
    
    # Commande setup
    subparsers.add_parser("setup", help="Configurer la planification cron")
    
    # Commande test
    subparsers.add_parser("test", help="Tester le système")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == "install":
        print("🚀 INSTALLATION DES DÉPENDANCES")
        print("=" * 35)
        
        if not check_system_dependencies():
            print("❌ Échec de l'installation des dépendances système")
            return
        
        python_path = install_python_dependencies()
        if python_path:
            print("\n✅ INSTALLATION TERMINÉE !")
            print(f"🐍 Python: {python_path}")
            print("\n🚀 Pour utiliser le générateur:")
            print(f"   {python_path} {__file__} generate --topic 'Mon test' --slides 3")
            print("\n📅 Pour configurer la planification:")
            print(f"   {python_path} {__file__} setup")
        else:
            print("❌ Échec de l'installation des dépendances Python")
    
    elif args.command == "generate":
        success = generate_video(
            topic=args.topic,
            slides=args.slides,
            output_dir=args.out,
            basename=args.basename,
            cleanup=args.cleanup
        )
        sys.exit(0 if success else 1)
    
    elif args.command == "setup":
        success = setup_cron()
        sys.exit(0 if success else 1)
    
    elif args.command == "test":
        print("🧪 TEST DU SYSTÈME")
        print("=" * 20)
        success = generate_video(topic="Test du système", slides=2, cleanup=True)
        if success:
            print("\n✅ Test réussi ! Le système fonctionne correctement.")
        else:
            print("\n❌ Test échoué. Vérifiez les erreurs ci-dessus.")
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()