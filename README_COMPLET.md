# 🎬 Générateur de Vidéo Quotidienne Automatique

Un système complet pour générer automatiquement des vidéos verticales quotidiennes avec slides et narration TTS.

## 🚀 Installation Rapide

### 1. Installation des dépendances
```bash
./install_dependencies.sh
```

### 2. Test du générateur
```bash
source .venv/bin/activate
python generate_daily_video.py --topic "Mon premier test" --slides 3
```

### 3. Configuration de la planification automatique
```bash
./setup_cron.sh
```

## 📁 Structure du Projet

```
/workspace/
├── generate_daily_video.py      # Script principal exécutable
├── install_dependencies.sh      # Installation automatique
├── setup_cron.sh               # Configuration cron
├── requirements.txt            # Dépendances Python
├── daily_video/               # Module principal
│   ├── __init__.py
│   ├── content.py             # Génération de contenu
│   ├── slides.py              # Création des slides (PIL)
│   ├── tts.py                 # Synthèse vocale (espeak-ng)
│   ├── video.py               # Assemblage vidéo (moviepy)
│   └── cli.py                 # Interface en ligne de commande
├── output/                    # Vidéos générées
│   └── daily_video_YYYY-MM-DD.mp4
└── README_COMPLET.md          # Cette documentation
```

## 🎯 Fonctionnalités

- ✅ **Génération automatique** de vidéos verticales (1080x1920)
- ✅ **Slides avec texte** générés avec PIL
- ✅ **Narration TTS** en français (espeak-ng + pyttsx3)
- ✅ **Assemblage vidéo** avec moviepy (H.264 + AAC)
- ✅ **Planification cron** pour génération quotidienne
- ✅ **Nettoyage automatique** des fichiers temporaires
- ✅ **Logs détaillés** pour le suivi

## 🛠️ Utilisation

### Génération manuelle
```bash
# Activer l'environnement
source .venv/bin/activate

# Génération basique
python generate_daily_video.py

# Avec options personnalisées
python generate_daily_video.py \
  --topic "Actualités du jour" \
  --slides 7 \
  --out /chemin/sortie \
  --basename ma_video \
  --cleanup
```

### Options disponibles
- `--topic` : Sujet de la vidéo (défaut: date du jour)
- `--slides` : Nombre de slides (défaut: 5)
- `--out` : Dossier de sortie (défaut: output)
- `--basename` : Nom de base du fichier (défaut: daily_video)
- `--cleanup` : Supprimer les fichiers temporaires

### Planification automatique
```bash
# Configuration interactive
./setup_cron.sh

# Ou configuration manuelle
crontab -e
# Ajouter: 0 9 * * * cd /workspace && /workspace/.venv/bin/python /workspace/generate_daily_video.py --topic "Actu du jour" --slides 5 --out /workspace/output --basename daily_video --cleanup >> /workspace/cron.log 2>&1
```

## 📊 Spécifications Techniques

### Format de sortie
- **Résolution** : 1080x1920 (9:16 vertical)
- **Codec vidéo** : H.264
- **Codec audio** : AAC
- **FPS** : 30
- **Qualité** : Optimisée pour les réseaux sociaux

### Dépendances système
- Python 3.8+
- ffmpeg
- espeak-ng
- libespeak1
- libportaudio2

### Dépendances Python
- moviepy==1.0.3
- Pillow==10.4.0
- pyttsx3==2.90
- numpy==1.26.4
- imageio==2.35.1
- imageio-ffmpeg==0.5.1

## 🔧 Personnalisation

### Modifier le contenu
Éditez `daily_video/content.py` pour personnaliser la génération de contenu :
```python
def generate_daily_script(topic: str | None = None, num_slides: int = 5) -> List[Dict[str, str]]:
    # Votre logique personnalisée ici
    pass
```

### Modifier l'apparence des slides
Éditez `daily_video/slides.py` pour changer :
- Couleurs de fond et de texte
- Polices et tailles
- Marges et espacement
- Format des slides

### Modifier la voix TTS
Éditez `daily_video/tts.py` pour ajuster :
- Vitesse de parole
- Voix utilisée
- Paramètres audio

## 📝 Logs et Monitoring

### Fichiers de log
- `cron.log` : Logs des exécutions automatiques
- Console : Logs détaillés lors de l'exécution manuelle

### Vérification du statut
```bash
# Vérifier les tâches cron
crontab -l

# Voir les logs récents
tail -f cron.log

# Lister les vidéos générées
ls -la output/
```

## 🚨 Dépannage

### Problèmes courants

**Erreur TTS :**
```bash
sudo apt-get install -y espeak-ng libespeak1
```

**Erreur ffmpeg :**
```bash
sudo apt-get install -y ffmpeg
```

**Erreur PIL :**
```bash
pip install --upgrade Pillow
```

**Problème de permissions :**
```bash
chmod +x *.sh *.py
```

### Test de l'installation
```bash
# Test complet
source .venv/bin/activate
python generate_daily_video.py --topic "Test" --slides 2 --cleanup

# Vérifier la vidéo générée
ffprobe output/daily_video_*.mp4
```

## 📈 Améliorations Possibles

- **Intégration API** : Ajouter des sources de contenu externes
- **Templates** : Créer des modèles de slides personnalisables
- **Upload automatique** : Publier directement sur YouTube/TikTok
- **Analytics** : Suivi des performances des vidéos
- **Interface web** : Dashboard de gestion
- **Multi-langues** : Support de plusieurs langues

## 📞 Support

Pour toute question ou problème :
1. Vérifiez les logs dans `cron.log`
2. Testez manuellement avec `python generate_daily_video.py`
3. Vérifiez que toutes les dépendances sont installées
4. Consultez la documentation des modules utilisés

---

**🎉 Votre générateur de vidéo quotidienne est prêt !**