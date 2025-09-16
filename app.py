import streamlit as st

from study_assistant.loader import load_uploaded_file
from study_assistant.text_utils import clean_text
from study_assistant.summarizer import summarize_text
from study_assistant.flashcards import generate_flashcards
from study_assistant.quiz import generate_quiz
from study_assistant.plan import generate_study_plan

st.set_page_config(page_title="Assistant d'étude", layout="wide")

st.title("Assistant d'étude – Révisez vos cours automatiquement")
st.write("Déposez votre fichier de cours et générez un résumé, des fiches, un quiz et un plan.")

uploaded = st.file_uploader("Déposez un fichier (.pdf, .docx, .pptx, .txt, .md)", type=["pdf", "docx", "pptx", "txt", "md"]) 

if uploaded:
	with st.spinner("Lecture du document…"):
		try:
			text = load_uploaded_file(uploaded, uploaded.name)
		except Exception as e:
			st.error(f"Erreur de lecture: {e}")
			st.stop()

	text = clean_text(text)

	col1, col2 = st.columns([1, 1])
	with col1:
		st.subheader("Résumé")
		max_sentences = st.slider("Nombre de phrases", min_value=3, max_value=15, value=8)
		summary = summarize_text(text, max_sentences=max_sentences)
		st.write(summary)

	with col2:
		st.subheader("Fiches de révision")
		num_cards = st.slider("Nombre de fiches", min_value=4, max_value=30, value=12)
		cards = generate_flashcards(text, num_cards=num_cards)
		for i, card in enumerate(cards, 1):
			with st.expander(f"Fiche {i}"):
				st.markdown(f"**Question**: {card['question']}")
				st.markdown(f"**Réponse**: {card['answer']}")

	st.subheader("Quiz QCM")
	num_q = st.slider("Nombre de questions", min_value=3, max_value=20, value=8)
	questions = generate_quiz(text, num_questions=num_q)
	score = 0
	for idx, q in enumerate(questions, 1):
		choice = st.radio(q["question"], q["choices"], index=None, key=f"q_{idx}")
		if choice is not None and choice == q["answer"]:
			score += 1
	st.info(f"Score provisoire: {score}/{len(questions)}")

	st.subheader("Plan de révision")
	days = st.slider("Jours de révision", min_value=3, max_value=21, value=7)
	daily = st.slider("Minutes par jour", min_value=20, max_value=120, value=45, step=5)
	plan = generate_study_plan(text, total_days=days, daily_minutes=daily)
	for item in plan:
		st.markdown(f"**{item['day']}** — {item['objective']}\n\n{item['tips']}")
else:
	st.info("Chargez un document pour commencer.")