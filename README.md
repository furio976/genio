# Générateur de vidéo quotidienne

Ce projet crée automatiquement une vidéo verticale (1080x1920) composée de slides avec texte et une narration synthèse vocale.

## Fonctionnalités
- Génération de script simple en français (titre + texte par slide)
- Rendu d'images (slides) avec PIL
- TTS local via pyttsx3 (offline)
- Assemblage vidéo avec moviepy (H.264 + AAC)
- Nom de fichier daté, ex: `daily_video_2025-09-18.mp4`

## Installation
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Sur Linux, assurez-vous d'avoir `ffmpeg` installé:
```bash
sudo apt-get update && sudo apt-get install -y ffmpeg
```

## Utilisation
```bash
python main.py --topic "Mon sujet" --slides 5 --out output --basename daily_video
```

La vidéo sera écrite dans `output/daily_video_YYYY-MM-DD.mp4` et les artefacts (images, audio) dans `output/YYYY-MM-DD/`.

## Planification quotidienne (cron)
Éditez la crontab:
```bash
crontab -e
```
Ajoutez une ligne pour exécuter chaque jour à 9h (adapter le chemin et l'environnement):
```bash
0 9 * * * cd /workspace && /workspace/.venv/bin/python /workspace/main.py --topic "Actu du jour" --slides 5 --out /workspace/output --basename daily_video >> /workspace/cron.log 2>&1
```

## Remarques
- pyttsx3 utilise les voix système. Sur certains environnements serveurs, l'audio TTS peut nécessiter des paquets supplémentaires.
- Vous pouvez remplacer `pyttsx3` par une API TTS si besoin.