from typing import List, Dict
import math

from .text_utils import split_sentences


def generate_study_plan(text: str, total_days: int = 7, daily_minutes: int = 45) -> List[Dict[str, str]]:
	sentences = split_sentences(text)
	if not sentences:
		return []
	chunks = max(1, total_days)
	per_chunk = math.ceil(len(sentences) / chunks)
	plan: List[Dict[str, str]] = []
	for day in range(chunks):
		start = day * per_chunk
		end = min((day + 1) * per_chunk, len(sentences))
		if start >= end:
			break
		plan.append({
			"day": f"Jour {day+1}",
			"objective": f"Relire {end - start} phrases (~{daily_minutes} min)",
			"tips": "- Faire 10 min de quiz\n- Refaire les flashcards\n- Noter 3 points clés",
		})
	return plan