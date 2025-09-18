## Générateur de vidéo quotidienne (FR)

Crée une vidéo verticale (1080x1920) avec texte du jour et voix off française.

### Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Aucune installation système de ffmpeg n'est nécessaire: `imageio-ffmpeg` télécharge un binaire portable automatiquement.

### Utilisation

```bash
source .venv/bin/activate
python video_daily/generate_video.py
# Ou avec votre texte
python video_daily/generate_video.py --texte "Votre texte inspirant ici"
# Fichier de sortie par défaut: videos/video_YYYY-MM-DD.mp4
```

Options utiles:
- `--font /chemin/ma_police.ttf` pour une police personnalisée
- `--sujet productivité` pour influencer le texte auto
- `--sortie /chemin/ma_video.mp4` pour définir le fichier de sortie

### Planifier tous les jours (cron)

```bash
crontab -e
# Tous les jours à 9h
0 9 * * * cd /workspace && . .venv/bin/activate && python video_daily/generate_video.py >> cron.log 2>&1
```