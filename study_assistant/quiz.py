from typing import List, Dict
import random

from .text_utils import split_sentences, get_top_keywords


def _distractors(keywords: List[str], correct: str, k: int = 3) -> List[str]:
	alts = [w for w in keywords if w.lower() != correct.lower() and len(w) >= 4]
	random.shuffle(alts)
	return alts[:k]


def generate_quiz(text: str, num_questions: int = 8) -> List[Dict[str, object]]:
	sentences = split_sentences(text)
	keywords = get_top_keywords(text, top_k=80)
	questions: List[Dict[str, object]] = []

	for s in sentences:
		if len(questions) >= num_questions:
			break
		correct = next((k for k in keywords if k.lower() in s.lower() and len(k) >= 4), None)
		if not correct:
			continue
		prompt = s.replace(correct, "____")
		choices = [correct] + _distractors(keywords, correct, k=3)
		random.shuffle(choices)
		questions.append({
			"question": f"Complétez: {prompt}",
			"choices": choices,
			"answer": correct,
		})

	# If too few questions, synthesize from keywords
	while len(questions) < num_questions and keywords:
		correct = keywords.pop(0)
		choices = [correct] + _distractors(keywords, correct, k=3)
		random.shuffle(choices)
		questions.append({
			"question": f"Quel terme correspond le mieux au sujet du cours ?", 
			"choices": choices,
			"answer": correct,
		})

	return questions