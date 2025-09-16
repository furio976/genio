from __future__ import annotations

import os
from typing import List, Tuple

try:
	from openai import OpenAI  # type: ignore
except Exception:  # pragma: no cover
	OpenAI = None  # type: ignore


class LLMClient:
	"""Thin wrapper for OpenAI, optional at runtime."""

	def __init__(self) -> None:
		self.api_key = os.getenv("OPENAI_API_KEY")
		self.enabled = bool(self.api_key and OpenAI)
		self.client = OpenAI(api_key=self.api_key) if self.enabled else None

	def enhance_summary(self, text: str, language: str = "fr") -> str:
		if not self.enabled:
			return ""
		prompt = (
			"Tu es un tuteur pédagogique. Résume clairement en français (200-300 mots):\n\n"
			+ text[:6000]
		)
		resp = self.client.chat.completions.create(
			model="gpt-4o-mini",
			messages=[{"role": "user", "content": prompt}],
			temperature=0.4,
		)
		return resp.choices[0].message.content.strip()

	def generate_flashcards(self, text: str, language: str = "fr", count: int = 20) -> List[Tuple[str, str]]:
		if not self.enabled:
			return []
		prompt = (
			"Génère des flashcards QA en français. Format: une par ligne 'Q|||A'.\n"
			"Q commence par 'Qu'est-ce que' ou 'Définir'. A = réponse courte.\n\n"
			+ text[:6000]
		)
		resp = self.client.chat.completions.create(
			model="gpt-4o-mini",
			messages=[{"role": "user", "content": prompt}],
			temperature=0.3,
		)
		lines = resp.choices[0].message.content.splitlines()
		cards: List[Tuple[str, str]] = []
		for line in lines:
			if "|||" in line:
				q, a = line.split("|||", 1)
				cards.append((q.strip(), a.strip()))
				if len(cards) >= count:
					break
		return cards

	def generate_quiz(self, text: str, language: str = "fr", count: int = 10):
		if not self.enabled:
			return []
		prompt = (
			"Crée un quiz QCM en français. Format: 'Question|||A;B;C;D|||BonneRéponse'.\n\n"
			+ text[:6000]
		)
		resp = self.client.chat.completions.create(
			model="gpt-4o-mini",
			messages=[{"role": "user", "content": prompt}],
			temperature=0.3,
		)
		lines = resp.choices[0].message.content.splitlines()
		quiz = []
		for line in lines:
			if "|||" in line:
				try:
					q, opts, ans = line.split("|||", 2)
					options = [o.strip() for o in opts.split(";") if o.strip()]
					quiz.append((q.strip(), options, ans.strip()))
					if len(quiz) >= count:
						break
				except Exception:
					continue
		return quiz