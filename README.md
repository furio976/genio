# Assistant d'étude (Streamlit)

Une application simple pour réviser à partir de vos cours (PDF, DOCX, PPTX, TXT, MD) :
- Résumé automatique
- Fiches de révision (Q/R)
- Quiz QCM
- Plan de révision

## Installation

Prérequis: Python 3.10+

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Lancer l'application

```bash
streamlit run app.py
```

## Formats supportés
- .pdf
- .docx
- .pptx
- .txt
- .md

## Note
Ce projet réalise un résumé extractif simple et des générateurs "rule-based" pour les fiches/quiz/plan. Aucune clé d'API n'est requise.