# 🎯 Démonstration de l'IA d'Étude

## 🚀 Comment utiliser l'application

### 1. Démarrage rapide
```bash
# Méthode 1 : Script automatique
./start.sh

# Méthode 2 : Manuel
source venv/bin/activate
python main.py
```

### 2. Accès à l'application
Ouvrez votre navigateur et allez sur : **http://localhost:8000**

### 3. Test avec le fichier d'exemple
Un fichier de test `test_cours.txt` est fourni avec un cours de mathématiques sur les fonctions.

## 📋 Fonctionnalités disponibles

### 📁 Upload de fichiers
- **Glissez-déposez** votre fichier dans la zone prévue
- **Formats supportés** : PDF, DOCX, TXT, MD
- **Traitement automatique** du contenu

### 🎯 Génération de contenu d'étude

#### 📄 Résumés intelligents
- Résumé structuré du contenu
- Points clés automatiquement extraits
- Sujets principaux identifiés

#### ❓ Questions d'étude
- Questions à choix multiples
- Questions vrai/faux
- Questions ouvertes
- Explications détaillées

#### 🎲 Quiz interactifs
- Quiz personnalisables (5-15 questions)
- Différents niveaux de difficulté
- Correction automatique

#### 🃏 Cartes mémoire (Flashcards)
- Recto : concept/terme
- Verso : définition/explication
- Interface interactive

## 💡 Modes de fonctionnement

### 🎭 Mode Démo (par défaut)
- **Aucune configuration requise**
- Contenu d'exemple généré
- Parfait pour tester l'interface

### 🤖 Mode IA Complet
1. Obtenez une clé API OpenAI sur [openai.com](https://openai.com)
2. Créez un fichier `.env` :
```bash
cp .env.example .env
# Éditez .env et ajoutez votre clé
```
3. Redémarrez l'application

## 🎪 Exemple d'utilisation

### Étape 1 : Upload
1. Ouvrez http://localhost:8000
2. Glissez le fichier `test_cours.txt` dans la zone d'upload
3. Attendez le traitement (quelques secondes)

### Étape 2 : Génération de contenu
Une fois le fichier traité, vous verrez une carte avec le nom du fichier.
Cliquez sur :

- **📄 Résumé** → Obtenir un résumé structuré
- **❓ Questions** → Générer 8 questions variées  
- **🎯 Quiz** → Créer un quiz de 10 questions
- **🃏 Cartes** → Générer 12 flashcards

### Étape 3 : Étudier
- Les résultats s'affichent dans une popup élégante
- Pour les flashcards : cliquez pour révéler la réponse
- Tout le contenu est sauvegardé dans vos sessions

## 🔧 Personnalisation

### Paramètres ajustables
- **Nombre de questions** : 5-20
- **Niveau de difficulté** : facile, moyen, difficile  
- **Type de quiz** : QCM, vrai/faux, mixte
- **Nombre de cartes** : 10-25

### Structure des fichiers
```
workspace/
├── uploads/     → Fichiers uploadés
├── sessions/    → Sessions sauvegardées  
├── static/      → Interface web
├── services/    → Logique métier
└── models/      → Modèles de données
```

## 🎨 Interface utilisateur

### Design moderne
- **Responsive** : fonctionne sur mobile/desktop
- **Drag & Drop** : interface intuitive
- **Animations fluides** : expérience agréable
- **Mode sombre** : confort visuel

### Fonctionnalités UX
- **Progress bar** lors de l'upload
- **Notifications** de succès/erreur
- **Modales élégantes** pour les résultats
- **Historique** des sessions

## 🚀 Cas d'usage

### 👨‍🎓 Étudiants
- Révision rapide avant examens
- Création de fiches de révision
- Auto-évaluation avec quiz

### 👩‍🏫 Enseignants  
- Génération de questions d'évaluation
- Création de supports pédagogiques
- Analyse de contenu de cours

### 📚 Professionnels
- Formation continue
- Mémorisation de concepts clés
- Préparation de présentations

## 🎯 Prochaines étapes

Une fois que vous maîtrisez l'application :

1. **Testez avec vos propres fichiers** de cours
2. **Configurez une clé API** pour l'IA complète
3. **Explorez les différents paramètres** disponibles
4. **Organisez vos sessions** par matière

---

**🎉 Bonne étude avec votre IA personnalisée !**