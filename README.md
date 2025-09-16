# IA d'Étude — Générateur de supports

Une application simple pour étudier vos cours à partir de fichiers PDF, DOCX, TXT ou MD. Elle génère automatiquement :

- Résumé (FR)
- Mots-clés
- Flashcards (Q/A)
- Quiz QCM

Fonctionne hors-ligne (algos classiques). Option : amélioration LLM (OpenAI) si `OPENAI_API_KEY` est défini.

## Installation

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Optionnel : définir la clé OpenAI
```bash
export OPENAI_API_KEY="votre_clef"
```

## Utilisation — CLI

```bash
python -m src.study_ai.cli /chemin/vers/fichier_ou_dossier --llm --out ./sortie
```

Les fichiers générés : `resume.txt`, `mots_cles.txt`, `flashcards.txt`, `quiz.txt`.

## Utilisation — UI (Streamlit)

```bash
streamlit run app.py
```

Glissez-déposez votre fichier dans l'interface.

## Formats supportés

- PDF, DOCX, TXT, MD

## Notes

- Les algorithmes hors-ligne utilisent NLTK, Sumy et RAKE (FR).
- La qualité dépend de la qualité du texte extrait (PDF scannés non pris en charge).