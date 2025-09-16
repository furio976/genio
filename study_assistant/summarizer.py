from typing import List

from .text_utils import clean_text, split_sentences, COMBINED_STOP_WORDS
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


def _score_sentences(sentences: List[str]) -> List[float]:
	if not sentences:
		return []
	vectorizer = TfidfVectorizer(
		lowercase=True,
		stop_words=list(COMBINED_STOP_WORDS),
		norm="l2",
		token_pattern=r"(?u)\b[\w-]{3,}\b",
	)
	X = vectorizer.fit_transform(sentences)
	scores = np.asarray(X.mean(axis=1)).ravel()
	return scores.tolist()


def summarize_text(text: str, max_sentences: int = 8) -> str:
	text = clean_text(text)
	sentences = split_sentences(text)
	if len(sentences) <= max_sentences:
		return " ".join(sentences)
	scores = _score_sentences(sentences)
	idx = np.argsort(scores)[-max_sentences:]
	idx_sorted = sorted(idx.tolist())
	selected = [sentences[i] for i in idx_sorted]
	return " ".join(selected)