from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional, Tuple

from rake_nltk import Rake
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.utils import get_stop_words

import nltk

# Ensure required NLTK data is available
for resource in ["punkt", "punkt_tab", "stopwords"]:
	try:
		if resource == "punkt":
			nltk.data.find("tokenizers/punkt")
		elif resource == "punkt_tab":
			nltk.data.find("tokenizers/punkt_tab")
		else:
			nltk.data.find(f"corpora/{resource}")
	except LookupError:
		try:
			nltk.download(resource, quiet=True)
		except Exception:
			pass


@dataclass
class StudyArtifacts:
	summary: str
	keywords: List[str]
	flashcards: List[Tuple[str, str]]  # (front, back)
	quiz_mcq: List[Tuple[str, List[str], str]]  # (question, options, answer)


def summarize_text(text: str, language: str = "french", max_sentences: int = 8) -> str:
	language = language.lower()
	parser = PlaintextParser.from_string(text, Tokenizer(language))
	stemmer = Stemmer(language)
	summarizer = LexRankSummarizer(stemmer)
	summarizer.stop_words = get_stop_words(language)

	sentences = summarizer(parser.document, max_sentences)
	return " ".join(str(s) for s in sentences)


def extract_keywords(text: str, language: str = "french", max_keywords: int = 20) -> List[str]:
	# Configure RAKE with French stopwords via NLTK
	rake = Rake(language=language)
	rake.extract_keywords_from_text(text)
	phrases = rake.get_ranked_phrases()[: max_keywords * 2]
	# Normalize: keep 1-3 word phrases, title-case for flashcard quality
	cleaned: List[str] = []
	for p in phrases:
		p = p.strip()
		if 1 <= len(p.split()) <= 4 and len(p) > 2:
			cleaned.append(p)
	# Deduplicate while preserving order
	seen = set()
	ordered: List[str] = []
	for k in cleaned:
		key = k.lower()
		if key not in seen:
			seen.add(key)
			ordered.append(k)
	return ordered[:max_keywords]


def generate_flashcards(text: str, keywords: List[str], max_cards: int = 20) -> List[Tuple[str, str]]:
	sentences = _split_sentences(text)
	cards: List[Tuple[str, str]] = []
	for kw in keywords:
		definition = _find_best_context_sentence(sentences, kw)
		if definition:
			front = f"Qu'est-ce que: {kw}?"
			back = definition
			cards.append((front, back))
		if len(cards) >= max_cards:
			break
	return cards


def generate_quiz(text: str, keywords: List[str], num_questions: int = 10) -> List[Tuple[str, List[str], str]]:
	sentences = _split_sentences(text)
	quiz: List[Tuple[str, List[str], str]] = []
	distractors_pool = [k for k in keywords]
	for kw in keywords:
		ctx = _find_best_context_sentence(sentences, kw)
		if not ctx:
			continue
		question, answer = _cloze_from_sentence(ctx, kw)
		options = _build_options(answer, distractors_pool)
		quiz.append((question, options, answer))
		if len(quiz) >= num_questions:
			break
	return quiz


def build_study_artifacts(text: str, language: str = "french") -> StudyArtifacts:
	text = _normalize_whitespace(text)
	summary = summarize_text(text, language=language)
	keywords = extract_keywords(text, language=language)
	flashcards = generate_flashcards(text, keywords)
	quiz_mcq = generate_quiz(text, keywords)
	return StudyArtifacts(summary=summary, keywords=keywords, flashcards=flashcards, quiz_mcq=quiz_mcq)


# ---------------- Internal helpers ----------------

def _normalize_whitespace(text: str) -> str:
	return re.sub(r"\s+", " ", text).strip()


def _split_sentences(text: str) -> List[str]:
	try:
		tokenizer = nltk.data.load("tokenizers/punkt/french.pickle")
		return tokenizer.tokenize(text)
	except LookupError:
		# Attempt to download required data at runtime
		nltk.download("punkt", quiet=True)
		try:
			nltk.download("punkt_tab", quiet=True)
		except Exception:
			pass
		tokenizer = nltk.data.load("tokenizers/punkt/french.pickle")
		return tokenizer.tokenize(text)


def _find_best_context_sentence(sentences: List[str], keyword: str) -> Optional[str]:
	keyword_lc = keyword.lower()
	best: Optional[str] = None
	best_len = 10**9
	for s in sentences:
		if keyword_lc in s.lower():
			l = len(s)
			if l < best_len:
				best = s
				best_len = l
	return best


def _cloze_from_sentence(sentence: str, keyword: str) -> Tuple[str, str]:
	pattern = re.compile(re.escape(keyword), re.IGNORECASE)
	answer = keyword
	question = pattern.sub("_____", sentence)
	return (f"Complétez: {question}", answer)


def _build_options(answer: str, pool: List[str]) -> List[str]:
	candidates = []
	for k in pool:
		if k.lower() != answer.lower() and len(k.split()) == len(answer.split()):
			candidates.append(k)
	options = [answer]
	options.extend(candidates[:3])
	# Pad if needed
	while len(options) < 4 and pool:
		k = pool.pop(0)
		if k.lower() != answer.lower():
			options.append(k)
	return options