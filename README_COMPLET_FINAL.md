# 🎬 SYSTÈME COMPLET DE GÉNÉRATION ET PUBLICATION VIDÉO

Un système complet pour générer et publier automatiquement des vidéos quotidiennes sur YouTube.

## 🚀 INSTALLATION RAPIDE

### 1. Installation complète
```bash
# Cloner ou télécharger les fichiers
# Puis installer tout le système
python3 daily_video_generator.py install
```

### 2. Configuration YouTube
```bash
# Configurer l'API YouTube
python3 youtube_uploader.py setup
```

### 3. Intégration complète
```bash
# Créer le script d'intégration
python3 youtube_uploader.py integrate
```

### 4. Test complet
```bash
# Test de génération + upload
python3 generate_and_upload.py --topic "Test complet" --slides 3
```

## 📁 STRUCTURE COMPLÈTE

```
/workspace/
├── daily_video_generator.py    # Générateur de vidéos (tout-en-un)
├── youtube_uploader.py         # Uploader YouTube
├── generate_and_upload.py      # Script d'intégration (créé automatiquement)
├── .venv/                      # Environnement Python
├── output/                     # Vidéos générées
│   └── daily_video_YYYY-MM-DD.mp4
├── client_secrets.json         # Identifiants Google (à créer)
├── youtube_config.json         # Configuration YouTube (créé automatiquement)
├── token.json                  # Token d'authentification (créé automatiquement)
├── cron.log                    # Logs des exécutions automatiques
└── README_*.md                 # Documentations
```

## 🎯 FONCTIONNALITÉS COMPLÈTES

### 🎬 Générateur de vidéos
- ✅ **Installation automatique** : Toutes les dépendances
- ✅ **Génération de vidéos** : Format vertical 1080x1920
- ✅ **Slides automatiques** : Texte et images générés
- ✅ **Narration TTS** : Synthèse vocale en français
- ✅ **Assemblage vidéo** : H.264 + AAC optimisé
- ✅ **Planification cron** : Génération quotidienne automatique

### 📺 Publication YouTube
- ✅ **Upload automatique** : API YouTube Data v3
- ✅ **Métadonnées personnalisables** : Titre, description, tags
- ✅ **Authentification OAuth** : Sécurisé et automatique
- ✅ **Gestion des erreurs** : Retry et logs détaillés
- ✅ **Intégration complète** : Génération + upload en une commande

### 🔧 Gestion du système
- ✅ **Configuration interactive** : Setup guidé
- ✅ **Test intégré** : Vérification complète
- ✅ **Logs détaillés** : Suivi de toutes les opérations
- ✅ **Gestion d'erreurs** : Messages clairs et solutions
- ✅ **Portable** : Fonctionne sur n'importe quel Linux

## 🚀 UTILISATION COMPLÈTE

### Installation et configuration
```bash
# 1. Installation complète
python3 daily_video_generator.py install

# 2. Configuration YouTube
python3 youtube_uploader.py setup

# 3. Intégration
python3 youtube_uploader.py integrate
```

### Génération manuelle
```bash
# Vidéo seulement
python3 daily_video_generator.py generate --topic "Mon sujet" --slides 5

# Vidéo + upload YouTube
python3 generate_and_upload.py --topic "Mon sujet" --slides 5
```

### Planification automatique
```bash
# Configuration cron pour génération + upload
crontab -e

# Ajouter cette ligne pour 9h chaque jour:
0 9 * * * cd /workspace && /workspace/.venv/bin/python /workspace/generate_and_upload.py --topic "Actualités du jour" --slides 5 >> /workspace/cron.log 2>&1
```

## 📊 SPÉCIFICATIONS TECHNIQUES

### Format de sortie
- **Résolution** : 1080x1920 (format vertical 9:16)
- **Codec vidéo** : H.264
- **Codec audio** : AAC
- **FPS** : 30 images/seconde
- **Qualité** : Optimisée pour YouTube et réseaux sociaux

### Dépendances automatiques
- **Système** : Python 3.8+, ffmpeg, espeak-ng, libespeak1
- **Python** : moviepy, Pillow, pyttsx3, numpy, imageio, google-api-python-client

### APIs utilisées
- **YouTube Data v3** : Upload et gestion des vidéos
- **OAuth 2.0** : Authentification sécurisée

## 🔧 PERSONNALISATION

### Contenu des vidéos
Éditez `daily_video_generator.py` :
```python
def generate_daily_script(topic: str = None, num_slides: int = 5):
    # Votre logique personnalisée ici
    pass
```

### Apparence des slides
Modifiez les constantes dans `daily_video_generator.py` :
```python
DEFAULT_SIZE = (1080, 1920)      # Résolution
BACKGROUND_COLOR = (18, 18, 18)  # Couleur de fond
TITLE_COLOR = (255, 255, 255)    # Couleur des titres
TEXT_COLOR = (220, 220, 220)     # Couleur du texte
```

### Métadonnées YouTube
Éditez `youtube_config.json` :
```json
{
  "default_title": "Actualités du {date}",
  "default_description": "Vidéo quotidienne du {date}",
  "default_tags": ["actualités", "quotidien", "auto"],
  "privacy_status": "unlisted"
}
```

## 📝 MONITORING ET LOGS

### Fichiers de log
- **Console** : Logs détaillés lors de l'exécution manuelle
- **cron.log** : Logs des exécutions automatiques
- **YouTube Studio** : Gestion des vidéos uploadées

### Vérification du statut
```bash
# Test du système
python3 daily_video_generator.py test

# Liste des vidéos YouTube
python3 youtube_uploader.py list

# Vérifier les logs
tail -f cron.log

# Vérifier les tâches cron
crontab -l
```

## 🚨 DÉPANNAGE

### Problèmes courants

**Erreur de génération :**
```bash
python3 daily_video_generator.py test
```

**Erreur d'upload :**
```bash
python3 youtube_uploader.py setup
```

**Problème de permissions :**
```bash
chmod +x *.py
```

**Réinstallation complète :**
```bash
rm -rf .venv output/* *.json
python3 daily_video_generator.py install
python3 youtube_uploader.py setup
```

## 🎯 EXEMPLES D'UTILISATION

### Workflow quotidien automatique
```bash
# 1. Installation (une seule fois)
python3 daily_video_generator.py install
python3 youtube_uploader.py setup
python3 youtube_uploader.py integrate

# 2. Configuration cron (une seule fois)
crontab -e
# Ajouter: 0 9 * * * cd /workspace && /workspace/.venv/bin/python /workspace/generate_and_upload.py --topic "Actualités du jour" --slides 5 >> /workspace/cron.log 2>&1

# 3. Le système fonctionne automatiquement !
# - Génération quotidienne à 9h
# - Upload automatique sur YouTube
# - Logs dans cron.log
```

### Workflow manuel
```bash
# Génération seule
python3 daily_video_generator.py generate --topic "Mon sujet" --slides 5

# Upload seul
python3 youtube_uploader.py upload --video "output/daily_video_2025-09-18.mp4"

# Génération + upload
python3 generate_and_upload.py --topic "Mon sujet" --slides 5
```

## 📈 AMÉLIORATIONS POSSIBLES

- **Sources de contenu** : Intégration d'APIs d'actualités
- **Templates** : Modèles de slides personnalisables
- **Multi-plateformes** : Upload sur TikTok, Instagram, etc.
- **Analytics** : Suivi des performances des vidéos
- **Interface web** : Dashboard de gestion
- **Multi-langues** : Support de plusieurs langues
- **Thumbnails** : Génération automatique de miniatures
- **Playlists** : Organisation automatique des vidéos

## 🎉 AVANTAGES DU SYSTÈME COMPLET

- ✅ **Automatisation complète** : Génération + publication sans intervention
- ✅ **Installation simple** : Une seule commande pour tout installer
- ✅ **Configuration guidée** : Interface interactive pour la configuration
- ✅ **Gestion d'erreurs** : Retry automatique et logs détaillés
- ✅ **Portable** : Fonctionne sur n'importe quel Linux
- ✅ **Évolutif** : Facilement personnalisable et extensible
- ✅ **Professionnel** : Qualité YouTube et réseaux sociaux
- ✅ **Fiable** : Testé et robuste

---

**🎬 Votre système complet de génération et publication vidéo est prêt !**

Générez et publiez automatiquement des vidéos quotidiennes sur YouTube sans aucune intervention manuelle !