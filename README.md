# 🎥 IA Génératrice de Vidéos Quotidiennes

Une intelligence artificielle qui génère automatiquement des vidéos éducatives chaque jour en français.

## ✨ Fonctionnalités

- **Génération automatique de contenu** : Utilise OpenAI GPT-4 pour créer des scripts originaux
- **Synthèse vocale** : Convertit le texte en audio avec Google Text-to-Speech
- **Création vidéo** : Génère des vidéos avec arrière-plans colorés et typographie
- **Planification quotidienne** : Génère automatiquement une vidéo chaque jour
- **Catégories personnalisables** : Tech, éducation, divertissement, général
- **Interface interactive** : Contrôle facile via ligne de commande

## 🚀 Installation

### Prérequis

- Python 3.8 ou plus récent
- Clé API OpenAI
- Connexion Internet

### Étapes d'installation

1. **Cloner le projet**
```bash
git clone <url-du-repo>
cd ia-video-generator
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configuration**
```bash
# Copier le fichier de configuration
cp .env.example .env

# Éditer .env avec vos paramètres
nano .env
```

4. **Configurer votre clé API OpenAI**
Dans le fichier `.env`, ajoutez votre clé API :
```
OPENAI_API_KEY=sk-votre-cle-api-ici
```

## ⚙️ Configuration

Le fichier `.env` contient tous les paramètres configurables :

```env
# Clé API OpenAI (OBLIGATOIRE)
OPENAI_API_KEY=your_openai_api_key_here

# Paramètres vidéo
VIDEO_DURATION=60          # Durée en secondes
VIDEO_WIDTH=1920           # Largeur en pixels
VIDEO_HEIGHT=1080          # Hauteur en pixels
VIDEO_FPS=30              # Images par seconde

# Paramètres de contenu
CONTENT_LANGUAGE=fr        # Langue du contenu
VIDEO_TOPIC_CATEGORY=general  # Catégorie : general, tech, news, education, entertainment
DAILY_SCHEDULE_TIME=09:00  # Heure de génération quotidienne (HH:MM)

# Répertoires
OUTPUT_DIRECTORY=./videos  # Dossier de sortie des vidéos
TEMP_DIRECTORY=./temp     # Dossier temporaire

# Synthèse vocale
TTS_LANGUAGE=fr           # Langue TTS
TTS_VOICE_SPEED=1.0       # Vitesse de la voix
```

## 🎮 Utilisation

### Mode interactif (recommandé)

```bash
python main.py
```

Commandes disponibles :
- `start` - Démarrer le planificateur quotidien
- `stop` - Arrêter le planificateur
- `now` - Générer une vidéo immédiatement
- `status` - Voir le statut du système
- `schedule` - Modifier l'heure de génération
- `quit` - Quitter le programme

### Génération immédiate

```bash
python main.py --generate-now
```

### Mode daemon (arrière-plan)

```bash
python main.py --daemon
```

### Voir le statut

```bash
python main.py --status
```

## 📁 Structure du projet

```
ia-video-generator/
├── main.py                 # Point d'entrée principal
├── config.py               # Configuration du système
├── content_generator.py    # Génération de contenu IA
├── video_generator.py      # Création des vidéos
├── scheduler.py            # Planification quotidienne
├── requirements.txt        # Dépendances Python
├── .env.example           # Exemple de configuration
├── README.md              # Documentation
├── videos/                # Vidéos générées (créé automatiquement)
└── temp/                  # Fichiers temporaires (créé automatiquement)
```

## 🎯 Types de contenu

### Catégories disponibles

- **general** : Faits intéressants, découvertes, conseils de vie
- **tech** : Innovations technologiques, IA, gadgets
- **education** : Histoire, science, langues, compétences
- **entertainment** : Films, séries, jeux, culture

### Personnalisation

Modifiez `VIDEO_TOPIC_CATEGORY` dans `.env` pour changer la catégorie par défaut.

## 📊 Fonctionnement

1. **Génération du sujet** : L'IA choisit un sujet selon la catégorie
2. **Création du script** : GPT-4 génère un script engageant
3. **Synthèse vocale** : Conversion du texte en audio français
4. **Création visuelle** : Génération d'un arrière-plan coloré avec titre
5. **Assemblage vidéo** : Combinaison audio/vidéo avec MoviePy
6. **Sauvegarde** : Vidéo finale sauvée dans le dossier `videos/`

## 🔧 Dépannage

### Erreurs courantes

**"OPENAI_API_KEY is required"**
- Vérifiez que votre clé API est correctement configurée dans `.env`

**"ModuleNotFoundError"**
- Installez les dépendances : `pip install -r requirements.txt`

**"Permission denied"**
- Vérifiez les permissions des dossiers `videos/` et `temp/`

**Problèmes de synthèse vocale**
- Vérifiez votre connexion Internet
- La langue doit être supportée par gTTS

### Logs

Les logs sont sauvegardés dans `video_ai.log` pour diagnostic.

## 🎨 Personnalisation avancée

### Modifier les couleurs d'arrière-plan

Éditez `video_generator.py`, fonction `create_background_image()` :

```python
colors = [
    [(64, 128, 255), (128, 64, 255)],  # Bleu vers Violet
    [(255, 128, 64), (255, 64, 128)],  # Orange vers Rose
    # Ajoutez vos couleurs ici
]
```

### Ajouter de nouvelles catégories

Dans `content_generator.py`, modifiez `topics_prompts` :

```python
topics_prompts = {
    'votre_categorie': [
        "sujet 1 pour votre catégorie",
        "sujet 2 pour votre catégorie",
    ]
}
```

### Personnaliser les prompts IA

Modifiez la fonction `generate_script()` dans `content_generator.py` pour ajuster le style de contenu.

## 📈 Améliorations futures

- [ ] Support de plusieurs langues
- [ ] Intégration avec YouTube API pour upload automatique
- [ ] Génération d'images avec DALL-E
- [ ] Sous-titres automatiques
- [ ] Interface web
- [ ] Analytics et métriques
- [ ] Templates vidéo personnalisables

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

Pour obtenir de l'aide :

1. Consultez cette documentation
2. Vérifiez les logs dans `video_ai.log`
3. Ouvrez une issue sur GitHub

## 🎉 Remerciements

- OpenAI pour l'API GPT-4
- Google pour gTTS (Text-to-Speech)
- L'équipe MoviePy pour la manipulation vidéo
- La communauté Python pour les excellentes bibliothèques