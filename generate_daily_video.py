#!/usr/bin/env python3
"""
Générateur de vidéo quotidienne automatique
Crée une vidéo verticale avec slides et narration TTS
"""

import os
import sys
import argparse
from datetime import date
from pathlib import Path

# Ajouter le répertoire du projet au path
sys.path.insert(0, str(Path(__file__).parent))

from daily_video.content import generate_daily_script
from daily_video.slides import render_slides
from daily_video.tts import synthesize_audios
from daily_video.video import assemble_video


def main():
    parser = argparse.ArgumentParser(description="Générateur de vidéo quotidienne")
    parser.add_argument("--topic", type=str, default="", help="Sujet de la vidéo")
    parser.add_argument("--slides", type=int, default=5, help="Nombre de slides")
    parser.add_argument("--out", type=str, default="output", help="Dossier de sortie")
    parser.add_argument("--basename", type=str, default="daily_video", help="Nom de base du fichier vidéo")
    parser.add_argument("--cleanup", action="store_true", help="Supprimer les fichiers temporaires")
    
    args = parser.parse_args()

    # Générer le script
    print("🎬 Génération du script...")
    script = generate_daily_script(topic=args.topic, num_slides=args.slides)
    print(f"✅ Script généré avec {len(script)} slides")

    # Créer les dossiers
    date_str = date.today().strftime("%Y-%m-%d")
    work_dir = Path(args.out) / date_str
    img_dir = work_dir / "images"
    audio_dir = work_dir / "audio"
    video_path = Path(args.out) / f"{args.basename}_{date_str}.mp4"

    # Générer les slides
    print("🖼️  Génération des slides...")
    slide_paths = render_slides(script, str(img_dir))
    print(f"✅ {len(slide_paths)} slides générées")

    # Générer l'audio
    print("🎵 Génération de l'audio...")
    texts = [s.get("text", "") for s in script]
    audio_paths = synthesize_audios(texts, str(audio_dir))
    print(f"✅ {len(audio_paths)} fichiers audio générés")

    # Assembler la vidéo
    print("🎥 Assemblage de la vidéo...")
    assembled = assemble_video(slide_paths, audio_paths, str(video_path))
    print(f"✅ Vidéo générée: {assembled}")

    # Nettoyage optionnel
    if args.cleanup:
        print("🧹 Nettoyage des fichiers temporaires...")
        import shutil
        shutil.rmtree(work_dir, ignore_errors=True)
        print("✅ Fichiers temporaires supprimés")

    # Afficher les informations de la vidéo
    if video_path.exists():
        size_mb = video_path.stat().st_size / (1024 * 1024)
        print(f"\n📊 Informations de la vidéo:")
        print(f"   📁 Fichier: {video_path}")
        print(f"   📏 Taille: {size_mb:.1f} MB")
        print(f"   📅 Date: {date_str}")
        print(f"   🎬 Slides: {len(slide_paths)}")
        print(f"   🎵 Audio: {len(audio_paths)} segments")


if __name__ == "__main__":
    main()