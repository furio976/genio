# 🎬 GÉNÉRATEUR DE VIDÉO QUOTIDIENNE - TOUT EN UN

Un script Python unique qui fait tout : installation, génération, planification et gestion des vidéos quotidiennes automatiques.

## 🚀 UTILISATION ULTRA-SIMPLE

### 1. Installation complète
```bash
python3 daily_video_generator.py install
```

### 2. Test du système
```bash
python3 daily_video_generator.py test
```

### 3. Génération manuelle
```bash
python3 daily_video_generator.py generate --topic "Mon sujet" --slides 5
```

### 4. Configuration automatique quotidienne
```bash
python3 daily_video_generator.py setup
```

## ✨ FONCTIONNALITÉS COMPLÈTES

### 🔧 Installation automatique
- ✅ Vérification des dépendances système
- ✅ Installation automatique (Ubuntu/Debian)
- ✅ Création de l'environnement Python
- ✅ Installation des packages requis
- ✅ Configuration complète en une commande

### 🎬 Génération de vidéos
- ✅ Vidéos verticales 1080x1920 (9:16)
- ✅ Slides avec texte automatique
- ✅ Narration TTS en français
- ✅ Assemblage vidéo H.264 + AAC
- ✅ Nettoyage automatique des fichiers temporaires

### ⏰ Planification automatique
- ✅ Configuration interactive du cron
- ✅ Choix de l'heure de génération
- ✅ Personnalisation du contenu
- ✅ Logs automatiques
- ✅ Gestion des erreurs

### 🛠️ Gestion du système
- ✅ Test complet du système
- ✅ Vérification des dépendances
- ✅ Logs détaillés
- ✅ Gestion d'erreurs robuste

## 📋 COMMANDES DISPONIBLES

### `install` - Installation complète
```bash
python3 daily_video_generator.py install
```
- Installe toutes les dépendances système
- Crée l'environnement Python virtuel
- Installe les packages Python requis
- Configure le système complet

### `generate` - Génération de vidéo
```bash
python3 daily_video_generator.py generate [OPTIONS]
```

**Options :**
- `--topic "Sujet"` : Sujet de la vidéo (défaut: date du jour)
- `--slides 5` : Nombre de slides (défaut: 5)
- `--out output` : Dossier de sortie (défaut: output)
- `--basename daily_video` : Nom de base du fichier
- `--cleanup` : Supprimer les fichiers temporaires

**Exemples :**
```bash
# Génération basique
python3 daily_video_generator.py generate

# Avec options personnalisées
python3 daily_video_generator.py generate --topic "Actualités" --slides 7 --cleanup

# Sortie personnalisée
python3 daily_video_generator.py generate --out /chemin/sortie --basename ma_video
```

### `setup` - Configuration cron
```bash
python3 daily_video_generator.py setup
```
- Configuration interactive
- Choix de l'heure de génération
- Personnalisation du contenu
- Installation automatique du cron

### `test` - Test du système
```bash
python3 daily_video_generator.py test
```
- Test complet du système
- Génération d'une vidéo de test
- Vérification de tous les composants
- Nettoyage automatique

## 📊 SPÉCIFICATIONS TECHNIQUES

### Format de sortie
- **Résolution** : 1080x1920 (format vertical 9:16)
- **Codec vidéo** : H.264
- **Codec audio** : AAC
- **FPS** : 30 images/seconde
- **Qualité** : Optimisée pour les réseaux sociaux

### Dépendances automatiques
- **Système** : Python 3.8+, ffmpeg, espeak-ng, libespeak1
- **Python** : moviepy, Pillow, pyttsx3, numpy, imageio

### Structure des fichiers
```
/workspace/
├── daily_video_generator.py    # Script principal (tout-en-un)
├── .venv/                      # Environnement Python (créé automatiquement)
├── output/                     # Vidéos générées
│   └── daily_video_YYYY-MM-DD.mp4
└── cron.log                    # Logs des exécutions automatiques
```

## 🎯 EXEMPLES D'UTILISATION

### Installation et test complet
```bash
# 1. Installation
python3 daily_video_generator.py install

# 2. Test
python3 daily_video_generator.py test

# 3. Configuration automatique
python3 daily_video_generator.py setup
```

### Génération manuelle
```bash
# Vidéo simple
python3 daily_video_generator.py generate

# Vidéo personnalisée
python3 daily_video_generator.py generate \
  --topic "Actualités du jour" \
  --slides 7 \
  --cleanup

# Sortie personnalisée
python3 daily_video_generator.py generate \
  --out /home/user/videos \
  --basename actualites \
  --topic "News du jour"
```

### Planification quotidienne
```bash
# Configuration interactive
python3 daily_video_generator.py setup

# Résultat : vidéo générée automatiquement tous les jours à l'heure choisie
```

## 🔧 PERSONNALISATION

### Modifier le contenu
Éditez la fonction `generate_daily_script()` dans le script pour personnaliser :
- Sources de contenu
- Format des slides
- Longueur des textes
- Sujets par défaut

### Modifier l'apparence
Éditez les constantes en haut du script :
```python
DEFAULT_SIZE = (1080, 1920)      # Résolution
BACKGROUND_COLOR = (18, 18, 18)  # Couleur de fond
TITLE_COLOR = (255, 255, 255)    # Couleur des titres
TEXT_COLOR = (220, 220, 220)     # Couleur du texte
MARGIN = 80                       # Marges
```

### Modifier la voix TTS
Éditez la fonction `synthesize_audios()` pour ajuster :
- Vitesse de parole (`-s` pour espeak-ng)
- Voix utilisée (`-v` pour espeak-ng)
- Volume (`-a` pour espeak-ng)

## 📝 LOGS ET MONITORING

### Fichiers de log
- **Console** : Logs détaillés lors de l'exécution manuelle
- **cron.log** : Logs des exécutions automatiques
- **Erreurs** : Affichage des erreurs avec solutions

### Vérification du statut
```bash
# Vérifier les tâches cron
crontab -l

# Voir les logs récents
tail -f cron.log

# Lister les vidéos générées
ls -la output/

# Tester le système
python3 daily_video_generator.py test
```

## 🚨 DÉPANNAGE

### Problèmes courants

**Erreur de permissions :**
```bash
chmod +x daily_video_generator.py
```

**Dépendances manquantes :**
```bash
python3 daily_video_generator.py install
```

**Test du système :**
```bash
python3 daily_video_generator.py test
```

**Vérification des logs :**
```bash
tail -f cron.log
```

### Support
1. Exécutez `python3 daily_video_generator.py test`
2. Vérifiez les logs dans `cron.log`
3. Consultez les messages d'erreur détaillés
4. Réinstallez si nécessaire : `python3 daily_video_generator.py install`

## 🎉 AVANTAGES DU TOUT-EN-UN

- ✅ **Un seul fichier** : Tout le système dans un script
- ✅ **Installation automatique** : Zéro configuration manuelle
- ✅ **Interface simple** : Commandes claires et intuitives
- ✅ **Gestion d'erreurs** : Messages d'erreur détaillés
- ✅ **Logs complets** : Suivi de toutes les opérations
- ✅ **Test intégré** : Vérification automatique du système
- ✅ **Portable** : Fonctionne sur n'importe quel Linux
- ✅ **Autonome** : Aucune dépendance externe requise

---

**🎬 Votre générateur de vidéo quotidienne tout-en-un est prêt !**

Un seul fichier, une installation, et vous générez des vidéos automatiquement tous les jours !