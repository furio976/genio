from datetime import date
from typing import List, Dict


def generate_daily_script(topic: str | None = None, num_slides: int = 5) -> List[Dict[str, str]]:
	"""Generate a simple script: a list of dicts with title and text."""
	if not topic or topic.strip() == "":
		# Default topic uses today's date
		topic = f"Faits marquants du {date.today().isoformat()}"

	slides: List[Dict[str, str]] = []
	for i in range(1, num_slides + 1):
		slides.append({
			"title": f"{topic} — Partie {i}",
			"text": (
				f"Voici un point clé numéro {i} sur le sujet '{topic}'. "
				"Ceci est un texte généré automatiquement pour la vidéo du jour."
			)
		})
	return slides