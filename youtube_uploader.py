#!/usr/bin/env python3
"""
📺 UPLOADER YOUTUBE AUTOMATIQUE
===============================

Script pour publier automatiquement les vidéos générées sur YouTube
avec l'API YouTube Data v3.

Usage:
    python youtube_uploader.py setup     # Configuration initiale
    python youtube_uploader.py upload    # Upload d'une vidéo
    python youtube_uploader.py list      # Lister les vidéos
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
import subprocess

# ============================================================================
# CONFIGURATION
# ============================================================================

CONFIG_FILE = "youtube_config.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

# ============================================================================
# INSTALLATION DES DÉPENDANCES
# ============================================================================

def install_youtube_dependencies():
    """Installe les dépendances pour l'API YouTube"""
    print("📦 Installation des dépendances YouTube...")
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "google-api-python-client", 
            "google-auth-httplib2", 
            "google-auth-oauthlib"
        ], check=True)
        print("✅ Dépendances YouTube installées")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'installation: {e}")
        return False

# ============================================================================
# CONFIGURATION YOUTUBE
# ============================================================================

def setup_youtube():
    """Configure l'API YouTube"""
    print("🔧 CONFIGURATION DE L'API YOUTUBE")
    print("=" * 40)
    
    print("""
📋 ÉTAPES DE CONFIGURATION:

1. Allez sur https://console.developers.google.com/
2. Créez un nouveau projet ou sélectionnez un projet existant
3. Activez l'API YouTube Data v3
4. Créez des identifiants OAuth 2.0
5. Téléchargez le fichier JSON des identifiants
6. Renommez-le en 'client_secrets.json' et placez-le dans ce dossier
""")
    
    # Vérifier si le fichier client_secrets.json existe
    client_secrets_file = Path("client_secrets.json")
    if not client_secrets_file.exists():
        print("❌ Fichier client_secrets.json non trouvé")
        print("📁 Placez le fichier client_secrets.json dans ce dossier")
        return False
    
    # Demander les informations de configuration
    print("\n📝 Configuration de la chaîne YouTube:")
    
    channel_name = input("Nom de la chaîne (défaut: 'Vidéos Quotidiennes'): ").strip()
    if not channel_name:
        channel_name = "Vidéos Quotidiennes"
    
    default_title = input("Titre par défaut (défaut: 'Actualités du {date}'): ").strip()
    if not default_title:
        default_title = "Actualités du {date}"
    
    default_description = input("Description par défaut (défaut: 'Vidéo quotidienne générée automatiquement'): ").strip()
    if not default_description:
        default_description = "Vidéo quotidienne générée automatiquement le {date}"
    
    default_tags = input("Tags par défaut (séparés par des virgules, défaut: 'actualités,quotidien,auto'): ").strip()
    if not default_tags:
        default_tags = "actualités,quotidien,auto"
    
    privacy_status = input("Statut de confidentialité (public/unlisted/private, défaut: 'unlisted'): ").strip().lower()
    if privacy_status not in ['public', 'unlisted', 'private']:
        privacy_status = 'unlisted'
    
    # Sauvegarder la configuration
    config = {
        "channel_name": channel_name,
        "default_title": default_title,
        "default_description": default_description,
        "default_tags": [tag.strip() for tag in default_tags.split(",")],
        "privacy_status": privacy_status,
        "last_setup": datetime.now().isoformat()
    }
    
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Configuration sauvegardée dans {CONFIG_FILE}")
    print("\n🚀 Configuration terminée ! Vous pouvez maintenant uploader des vidéos.")
    
    return True

# ============================================================================
# UPLOAD YOUTUBE
# ============================================================================

def upload_to_youtube(video_path: str, title: str = None, description: str = None, 
                     tags: list = None, privacy_status: str = None):
    """Upload une vidéo sur YouTube"""
    
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
    except ImportError:
        print("❌ Dépendances YouTube non installées. Exécutez: python youtube_uploader.py setup")
        return False
    
    # Charger la configuration
    if not Path(CONFIG_FILE).exists():
        print("❌ Configuration non trouvée. Exécutez: python youtube_uploader.py setup")
        return False
    
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Utiliser les valeurs par défaut si non spécifiées
    if not title:
        date_str = datetime.now().strftime("%Y-%m-%d")
        title = config.get("default_title", "Actualités du {date}").format(date=date_str)
    
    if not description:
        date_str = datetime.now().strftime("%Y-%m-%d")
        description = config.get("default_description", "Vidéo quotidienne générée automatiquement le {date}").format(date=date_str)
    
    if not tags:
        tags = config.get("default_tags", ["actualités", "quotidien", "auto"])
    
    if not privacy_status:
        privacy_status = config.get("privacy_status", "unlisted")
    
    # Authentification
    creds = None
    token_file = "token.json"
    
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    
    # Créer le service YouTube
    youtube = build('youtube', 'v3', credentials=creds)
    
    # Préparer les métadonnées
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': '25'  # News & Politics
        },
        'status': {
            'privacyStatus': privacy_status
        }
    }
    
    # Upload de la vidéo
    print(f"📤 Upload de la vidéo: {video_path}")
    print(f"📝 Titre: {title}")
    print(f"🔒 Statut: {privacy_status}")
    
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    
    request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=media
    )
    
    # Exécuter l'upload
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"📊 Progression: {int(status.progress() * 100)}%")
    
    if 'id' in response:
        video_id = response['id']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"✅ Vidéo uploadée avec succès !")
        print(f"🔗 URL: {video_url}")
        print(f"🆔 ID: {video_id}")
        return True
    else:
        print(f"❌ Erreur lors de l'upload: {response}")
        return False

# ============================================================================
# LISTE DES VIDÉOS
# ============================================================================

def list_youtube_videos():
    """Liste les vidéos de la chaîne YouTube"""
    
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError:
        print("❌ Dépendances YouTube non installées. Exécutez: python youtube_uploader.py setup")
        return False
    
    # Authentification
    creds = None
    token_file = "token.json"
    
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    
    # Créer le service YouTube
    youtube = build('youtube', 'v3', credentials=creds)
    
    # Récupérer les vidéos
    print("📺 Récupération des vidéos de la chaîne...")
    
    request = youtube.search().list(
        part="snippet",
        forMine=True,
        type="video",
        maxResults=10,
        order="date"
    )
    
    response = request.execute()
    
    if 'items' in response:
        print(f"\n📋 Dernières {len(response['items'])} vidéos:")
        print("=" * 60)
        
        for item in response['items']:
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            published = item['snippet']['publishedAt']
            url = f"https://www.youtube.com/watch?v={video_id}"
            
            print(f"📺 {title}")
            print(f"🔗 {url}")
            print(f"📅 {published}")
            print("-" * 60)
    else:
        print("❌ Aucune vidéo trouvée")
    
    return True

# ============================================================================
# INTÉGRATION AVEC LE GÉNÉRATEUR
# ============================================================================

def integrate_with_generator():
    """Intègre l'upload YouTube avec le générateur de vidéos"""
    
    print("🔗 INTÉGRATION AVEC LE GÉNÉRATEUR DE VIDÉOS")
    print("=" * 50)
    
    # Vérifier si le générateur existe
    generator_path = Path("daily_video_generator.py")
    if not generator_path.exists():
        print("❌ Générateur de vidéos non trouvé")
        return False
    
    # Créer un script d'intégration
    integration_script = """#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

def generate_and_upload(topic="", slides=5, upload=True):
    \"\"\"Génère une vidéo et l'upload sur YouTube\"\"\"
    
    # Générer la vidéo
    print("🎬 Génération de la vidéo...")
    result = subprocess.run([
        sys.executable, "daily_video_generator.py", "generate",
        "--topic", topic,
        "--slides", str(slides),
        "--cleanup"
    ])
    
    if result.returncode != 0:
        print("❌ Erreur lors de la génération de la vidéo")
        return False
    
    if not upload:
        print("✅ Vidéo générée (upload désactivé)")
        return True
    
    # Trouver la vidéo générée
    output_dir = Path("output")
    video_files = list(output_dir.glob("daily_video_*.mp4"))
    
    if not video_files:
        print("❌ Aucune vidéo générée trouvée")
        return False
    
    latest_video = max(video_files, key=lambda x: x.stat().st_mtime)
    
    # Upload sur YouTube
    print("📺 Upload sur YouTube...")
    result = subprocess.run([
        sys.executable, "youtube_uploader.py", "upload",
        "--video", str(latest_video)
    ])
    
    return result.returncode == 0

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Génération et upload automatique")
    parser.add_argument("--topic", default="", help="Sujet de la vidéo")
    parser.add_argument("--slides", type=int, default=5, help="Nombre de slides")
    parser.add_argument("--no-upload", action="store_true", help="Désactiver l'upload")
    
    args = parser.parse_args()
    
    success = generate_and_upload(
        topic=args.topic,
        slides=args.slides,
        upload=not args.no_upload
    )
    
    sys.exit(0 if success else 1)
"""
    
    with open("generate_and_upload.py", "w", encoding="utf-8") as f:
        f.write(integration_script)
    
    # Rendre le script exécutable
    os.chmod("generate_and_upload.py", 0o755)
    
    print("✅ Script d'intégration créé: generate_and_upload.py")
    print("\n🚀 Utilisation:")
    print("   python generate_and_upload.py --topic 'Mon sujet' --slides 5")
    print("   python generate_and_upload.py --no-upload  # Génération seulement")
    
    return True

# ============================================================================
# INTERFACE PRINCIPALE
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Uploader YouTube automatique")
    subparsers = parser.add_subparsers(dest="command", help="Commandes disponibles")
    
    # Commande setup
    subparsers.add_parser("setup", help="Configurer l'API YouTube")
    
    # Commande upload
    upload_parser = subparsers.add_parser("upload", help="Uploader une vidéo")
    upload_parser.add_argument("--video", required=True, help="Chemin vers la vidéo")
    upload_parser.add_argument("--title", help="Titre de la vidéo")
    upload_parser.add_argument("--description", help="Description de la vidéo")
    upload_parser.add_argument("--tags", help="Tags séparés par des virgules")
    upload_parser.add_argument("--privacy", choices=["public", "unlisted", "private"], help="Statut de confidentialité")
    
    # Commande list
    subparsers.add_parser("list", help="Lister les vidéos de la chaîne")
    
    # Commande integrate
    subparsers.add_parser("integrate", help="Intégrer avec le générateur de vidéos")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == "setup":
        if not install_youtube_dependencies():
            sys.exit(1)
        if not setup_youtube():
            sys.exit(1)
    
    elif args.command == "upload":
        if not Path(args.video).exists():
            print(f"❌ Fichier vidéo non trouvé: {args.video}")
            sys.exit(1)
        
        tags = args.tags.split(",") if args.tags else None
        success = upload_to_youtube(
            video_path=args.video,
            title=args.title,
            description=args.description,
            tags=tags,
            privacy_status=args.privacy
        )
        sys.exit(0 if success else 1)
    
    elif args.command == "list":
        if not install_youtube_dependencies():
            sys.exit(1)
        success = list_youtube_videos()
        sys.exit(0 if success else 1)
    
    elif args.command == "integrate":
        success = integrate_with_generator()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()