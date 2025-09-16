from __future__ import annotations

import tempfile
from pathlib import Path

import streamlit as st

from src.study_ai.ingest import read_text_from_file
from src.study_ai.processing import build_study_artifacts
from src.study_ai.llm import LLMClient

st.set_page_config(page_title="IA d'Étude", page_icon="📚", layout="wide")

st.title("📚 IA d'Étude — Générateur de supports")
st.write("Déposez un fichier de cours (PDF, DOCX, TXT, MD).")

use_llm = st.toggle("Améliorer avec OpenAI (optionnel)")

uploaded = st.file_uploader("Fichier de cours", type=["pdf", "docx", "txt", "md"], accept_multiple_files=False)

if uploaded is not None:
	with tempfile.TemporaryDirectory() as tmpd:
		tmp_path = Path(tmpd) / uploaded.name
		with open(tmp_path, "wb") as f:
			f.write(uploaded.getbuffer())
		text = read_text_from_file(str(tmp_path))
		artifacts = build_study_artifacts(text, language="french")

		if use_llm:
			llm = LLMClient()
			if llm.enabled:
				enhanced = llm.enhance_summary(text)
				if enhanced:
					artifacts.summary = enhanced

		st.subheader("Résumé")
		st.write(artifacts.summary or "(Résumé court non disponible)")

		col1, col2 = st.columns(2)
		with col1:
			st.subheader("Mots-clés")
			st.write("\n".join(artifacts.keywords))
		with col2:
			st.subheader("Flashcards")
			for q, a in artifacts.flashcards:
				with st.expander(q):
					st.write(a)

		st.subheader("Quiz QCM")
		for q, options, ans in artifacts.quiz_mcq:
			st.markdown(f"**{q}**")
			for idx, opt in enumerate(options):
				letter = chr(ord('A') + idx)
				st.write(f"{letter}) {opt}")
			st.caption(f"Réponse: {ans}")