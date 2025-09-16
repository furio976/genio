from typing import List, Dict

from .text_utils import split_sentences, get_top_keywords


def _candidate_statements(sentences: List[str]) -> List[str]:
	candidates = []
	for s in sentences:
		if 50 <= len(s) <= 240 and s[-1] == ".":
			candidates.append(s)
	return candidates[:50]


def generate_flashcards(text: str, num_cards: int = 12) -> List[Dict[str, str]]:
	sentences = split_sentences(text)
	candidates = _candidate_statements(sentences)
	keywords = get_top_keywords(text, top_k=50)

	cards: List[Dict[str, str]] = []
	for i, sentence in enumerate(candidates):
		if len(cards) >= num_cards:
			break
		# Try to form a cloze deletion using a keyword
		missing = next((k for k in keywords if k.lower() in sentence.lower()), None)
		if missing and len(missing) >= 4:
			prompt = sentence.replace(missing, "____")
			cards.append({
				"question": f"Complétez: {prompt}",
				"answer": missing,
			})
		else:
			cards.append({
				"question": f"Question: {sentence}",
				"answer": sentence,
			})
	return cards