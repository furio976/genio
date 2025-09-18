# 📺 UPLOADER YOUTUBE AUTOMATIQUE

Script pour publier automatiquement les vidéos générées sur YouTube avec l'API YouTube Data v3.

## 🚀 INSTALLATION ET CONFIGURATION

### 1. Configuration de l'API YouTube
```bash
python3 youtube_uploader.py setup
```

### 2. Obtenir les identifiants Google
1. Allez sur [Google Cloud Console](https://console.developers.google.com/)
2. Créez un nouveau projet ou sélectionnez un projet existant
3. Activez l'API YouTube Data v3
4. Créez des identifiants OAuth 2.0
5. Téléchargez le fichier JSON des identifiants
6. Renommez-le en `client_secrets.json` et placez-le dans ce dossier

### 3. Configuration interactive
Le script vous demandera :
- Nom de la chaîne
- Titre par défaut des vidéos
- Description par défaut
- Tags par défaut
- Statut de confidentialité (public/unlisted/private)

## 📋 COMMANDES DISPONIBLES

### `setup` - Configuration initiale
```bash
python3 youtube_uploader.py setup
```
- Installe les dépendances Python
- Configure l'API YouTube
- Sauvegarde la configuration

### `upload` - Upload d'une vidéo
```bash
python3 youtube_uploader.py upload --video "chemin/vers/video.mp4"
```

**Options :**
- `--title "Mon titre"` : Titre personnalisé
- `--description "Ma description"` : Description personnalisée
- `--tags "tag1,tag2,tag3"` : Tags personnalisés
- `--privacy public|unlisted|private` : Statut de confidentialité

**Exemples :**
```bash
# Upload basique
python3 youtube_uploader.py upload --video "output/daily_video_2025-09-18.mp4"

# Upload avec options personnalisées
python3 youtube_uploader.py upload \
  --video "output/daily_video_2025-09-18.mp4" \
  --title "Actualités du 18 septembre 2025" \
  --description "Vidéo quotidienne générée automatiquement" \
  --tags "actualités,quotidien,auto" \
  --privacy unlisted
```

### `list` - Lister les vidéos
```bash
python3 youtube_uploader.py list
```
Affiche les 10 dernières vidéos de la chaîne.

### `integrate` - Intégration avec le générateur
```bash
python3 youtube_uploader.py integrate
```
Crée un script `generate_and_upload.py` qui combine génération et upload.

## 🔗 INTÉGRATION COMPLÈTE

### Script d'intégration automatique
```bash
# Créer le script d'intégration
python3 youtube_uploader.py integrate

# Générer et uploader automatiquement
python3 generate_and_upload.py --topic "Actualités du jour" --slides 5

# Génération seulement (sans upload)
python3 generate_and_upload.py --topic "Test" --slides 3 --no-upload
```

### Planification complète avec cron
```bash
# Configuration du cron pour génération + upload
crontab -e

# Ajouter cette ligne pour 9h chaque jour:
0 9 * * * cd /workspace && /workspace/.venv/bin/python /workspace/generate_and_upload.py --topic "Actualités du jour" --slides 5 >> /workspace/cron.log 2>&1
```

## 📊 FONCTIONNALITÉS

### Upload automatique
- ✅ Authentification OAuth 2.0
- ✅ Métadonnées personnalisables
- ✅ Gestion des erreurs
- ✅ Progression de l'upload
- ✅ URLs de retour

### Configuration flexible
- ✅ Titre par défaut avec variables (date)
- ✅ Description par défaut
- ✅ Tags par défaut
- ✅ Statut de confidentialité
- ✅ Sauvegarde de la configuration

### Intégration complète
- ✅ Script d'intégration automatique
- ✅ Génération + upload en une commande
- ✅ Compatible avec le générateur de vidéos
- ✅ Planification cron complète

## 🛠️ DÉPENDANCES

### Python packages
- `google-api-python-client`
- `google-auth-httplib2`
- `google-auth-oauthlib`

### Fichiers requis
- `client_secrets.json` : Identifiants OAuth 2.0 de Google
- `youtube_config.json` : Configuration sauvegardée (créé automatiquement)
- `token.json` : Token d'authentification (créé automatiquement)

## 🔧 PERSONNALISATION

### Modifier la configuration
Éditez `youtube_config.json` :
```json
{
  "channel_name": "Ma Chaîne",
  "default_title": "Actualités du {date}",
  "default_description": "Vidéo quotidienne du {date}",
  "default_tags": ["actualités", "quotidien", "auto"],
  "privacy_status": "unlisted"
}
```

### Variables disponibles
- `{date}` : Date actuelle (YYYY-MM-DD)
- `{time}` : Heure actuelle
- `{channel}` : Nom de la chaîne

## 📝 LOGS ET MONITORING

### Fichiers de log
- **Console** : Logs détaillés de l'upload
- **cron.log** : Logs des exécutions automatiques
- **YouTube Studio** : Gestion des vidéos uploadées

### Vérification du statut
```bash
# Lister les vidéos uploadées
python3 youtube_uploader.py list

# Vérifier les logs
tail -f cron.log

# Tester l'upload
python3 youtube_uploader.py upload --video "test.mp4"
```

## 🚨 DÉPANNAGE

### Problèmes courants

**Erreur d'authentification :**
```bash
# Supprimer le token et reconfigurer
rm token.json
python3 youtube_uploader.py setup
```

**Erreur d'API :**
- Vérifiez que l'API YouTube Data v3 est activée
- Vérifiez les identifiants OAuth 2.0
- Vérifiez les quotas de l'API

**Erreur d'upload :**
- Vérifiez la taille de la vidéo (max 128GB)
- Vérifiez le format (MP4 recommandé)
- Vérifiez la connexion internet

### Test de l'installation
```bash
# Test complet
python3 youtube_uploader.py setup
python3 youtube_uploader.py list
```

## 🎯 EXEMPLE COMPLET

### Installation et configuration
```bash
# 1. Configuration YouTube
python3 youtube_uploader.py setup

# 2. Intégration avec le générateur
python3 youtube_uploader.py integrate

# 3. Test complet
python3 generate_and_upload.py --topic "Test YouTube" --slides 3
```

### Planification quotidienne
```bash
# Configuration cron pour génération + upload automatique
crontab -e

# Ajouter:
0 9 * * * cd /workspace && /workspace/.venv/bin/python /workspace/generate_and_upload.py --topic "Actualités du jour" --slides 5 >> /workspace/cron.log 2>&1
```

## 📈 AVANTAGES

- ✅ **Upload automatique** : Publie directement sur YouTube
- ✅ **Configuration simple** : Interface interactive
- ✅ **Intégration complète** : Compatible avec le générateur
- ✅ **Planification** : Upload quotidien automatique
- ✅ **Flexibilité** : Métadonnées personnalisables
- ✅ **Monitoring** : Suivi des uploads

---

**📺 Votre système de publication YouTube automatique est prêt !**

Générez et publiez des vidéos quotidiennes automatiquement sur YouTube !