import re
from typing import List, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS


FRENCH_STOP_WORDS = {
	"alors", "au", "aucuns", "aussi", "autre", "avant", "avec", "avoir", "bon", "car", "ce",
	"cela", "ces", "ceux", "chaque", "ci", "comme", "comment", "dans", "des", "du", "dedans",
	"dehors", "depuis", "devrait", "doit", "donc", "dos", "droite", "début", "elle", "elles",
	"en", "encore", "essai", "est", "et", "eu", "fait", "faites", "fois", "font", "force", "haut",
	"hors", "ici", "il", "ils", "je", "juste", "la", "le", "les", "leur", "là", "ma", "maintenant",
	"mais", "mes", "mine", "moins", "mon", "mot", "même", "ni", "nommés", "notre", "nous", "nouveaux",
	"ou", "où", "par", "parce", "parole", "pas", "personnes", "peut", "peu", "pièces", "plupart",
	"pour", "pourquoi", "quand", "que", "quel", "quelle", "quelles", "quels", "qui", "sa", "sans",
	"ses", "seulement", "si", "sien", "son", "sont", "sous", "soyez", "sujet", "sur", "ta", "tandis",
	"tellement", "tels", "tes", "ton", "tous", "tout", "trop", "très", "tu", "voient", "vont", "votre",
	"vous", "vu", "ça", "étaient", "état", "étions", "été", "être",
}

COMBINED_STOP_WORDS = set(ENGLISH_STOP_WORDS) | FRENCH_STOP_WORDS


def clean_text(text: str) -> str:
	text = re.sub(r"\r\n?|\n", "\n", text)
	text = re.sub(r"\t", " ", text)
	text = re.sub(r"\s+", " ", text)
	text = re.sub(r"\s*\n\s*", "\n", text)
	return text.strip()


def split_sentences(text: str) -> List[str]:
	# Simple sentence split for FR/EN
	# Avoid splitting on initials or numbers by a basic heuristic
	pattern = r"(?<=[.!?])\s+(?=[A-ZÀÂÄÇÉÈÊËÎÏÔÖÙÛÜŸ])"
	sentences = re.split(pattern, text)
	# Fallback if only one very long sentence
	if len(sentences) <= 1 and len(text) > 500:
		sentences = re.split(r";|:\s| - ", text)
	return [s.strip() for s in sentences if s and len(s.strip()) > 1]


def get_top_keywords(text: str, top_k: int = 20) -> List[str]:
	vectorizer = TfidfVectorizer(
		lowercase=True,
		stop_words=list(COMBINED_STOP_WORDS),
		token_pattern=r"(?u)\b[\w-]{3,}\b",
	)
	try:
		X = vectorizer.fit_transform([text])
	except ValueError:
		return []
	scores = X.toarray()[0]
	features = vectorizer.get_feature_names_out()
	pairs: List[Tuple[str, float]] = list(zip(features, scores))
	pairs.sort(key=lambda x: x[1], reverse=True)
	return [w for w, _ in pairs[:top_k]]