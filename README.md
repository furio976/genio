# 🧠 IA d'Étude Personnalisée

Une application web intelligente qui analyse vos fichiers de cours et génère automatiquement du contenu d'étude personnalisé : résumés, questions, quiz, et cartes mémoire.

## ✨ Fonctionnalités

- **📁 Upload de fichiers** : Supporte PDF, DOCX, TXT, et Markdown
- **📝 Résumés automatiques** : Génération de résumés structurés avec points clés
- **❓ Questions d'étude** : Création de questions variées (QCM, vrai/faux, ouvertes)
- **🎯 Quiz interactifs** : Quiz personnalisés avec correction automatique
- **🃏 Cartes mémoire** : Flashcards pour la mémorisation
- **💡 Explications** : Explications détaillées de concepts spécifiques
- **🎨 Interface moderne** : Design responsive et intuitive

## 🚀 Installation

### Prérequis
- Python 3.8+
- Une clé API OpenAI (optionnelle, mode démo disponible)

### Étapes d'installation

1. **Cloner le projet**
```bash
git clone <votre-repo>
cd ia-etude
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configuration (optionnel)**
```bash
cp .env.example .env
# Éditer .env et ajouter votre clé API OpenAI
```

4. **Lancer l'application**
```bash
python main.py
```

L'application sera accessible sur `http://localhost:8000`

## 📖 Utilisation

### 1. Upload d'un fichier
- Glissez-déposez votre fichier de cours dans la zone d'upload
- Ou cliquez pour sélectionner un fichier
- Formats supportés : PDF, DOCX, TXT, MD

### 2. Génération de contenu d'étude
Une fois le fichier traité, vous pouvez :

- **📄 Résumé** : Obtenir un résumé structuré avec points clés
- **❓ Questions** : Générer des questions d'étude variées
- **🎯 Quiz** : Créer un quiz interactif
- **🃏 Cartes** : Générer des flashcards pour la mémorisation

### 3. Gestion des sessions
- Toutes vos sessions sont sauvegardées
- Accès rapide à vos fichiers précédents
- Historique complet de vos études

## 🔧 Configuration API

### Avec OpenAI (recommandé)
1. Créez un compte sur [OpenAI](https://openai.com)
2. Obtenez votre clé API
3. Ajoutez-la dans le fichier `.env` :
```env
OPENAI_API_KEY=votre_clé_api_ici
```

### Mode démo (sans API)
L'application fonctionne en mode démo sans clé API, avec du contenu d'exemple.

## 📁 Structure du projet

```
ia-etude/
├── main.py                 # Application FastAPI principale
├── requirements.txt        # Dépendances Python
├── .env.example           # Configuration d'exemple
├── models/
│   └── study_models.py    # Modèles de données
├── services/
│   ├── document_processor.py  # Traitement des documents
│   └── ai_study_assistant.py  # Assistant IA
├── static/
│   └── index.html         # Interface utilisateur
├── uploads/               # Fichiers uploadés
├── sessions/              # Sessions sauvegardées
└── README.md             # Documentation
```

## 🎯 Types de contenu générés

### Résumés
- Résumé général du contenu
- Points clés essentiels
- Sujets principaux couverts

### Questions d'étude
- Questions à choix multiples
- Questions vrai/faux
- Questions ouvertes
- Avec explications détaillées

### Quiz interactifs
- Quiz personnalisables
- Correction automatique
- Feedback détaillé

### Cartes mémoire
- Recto : concept/question
- Verso : définition/réponse
- Catégorisation automatique

## 🔒 Sécurité et confidentialité

- Les fichiers sont traités localement
- Aucune donnée n'est partagée sans votre consentement
- Sessions stockées en local
- Possibilité de supprimer vos données

## 🐛 Dépannage

### Erreurs courantes

**Erreur d'upload de fichier**
- Vérifiez le format (PDF, DOCX, TXT, MD)
- Assurez-vous que le fichier n'est pas corrompu

**Erreur de génération de contenu**
- Vérifiez votre clé API OpenAI
- Le mode démo fonctionne sans API

**Problèmes d'affichage**
- Actualisez la page
- Vérifiez votre connexion internet

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Améliorer la documentation

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 🆘 Support

Pour toute question ou problème :
1. Consultez cette documentation
2. Vérifiez les issues existantes
3. Créez une nouvelle issue si nécessaire

---

**Bonne étude ! 📚✨**