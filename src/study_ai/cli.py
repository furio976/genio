from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import List

from rich.console import Console
from rich.table import Table

from .ingest import read_text_from_file
from .processing import build_study_artifacts
from .llm import LLMClient

console = Console()


def process_file(input_path: str, use_llm: bool = False, out_dir: str | None = None) -> None:
	text = read_text_from_file(input_path)
	artifacts = build_study_artifacts(text, language="french")

	if use_llm:
		llm = LLMClient()
		if llm.enabled:
			enhanced = llm.enhance_summary(text)
			if enhanced:
				artifacts.summary = enhanced

	_out_dir = out_dir or (str(Path(input_path).with_suffix("")) + "_study")
	Path(_out_dir).mkdir(parents=True, exist_ok=True)

	# Write outputs
	(Path(_out_dir) / "resume.txt").write_text(artifacts.summary, encoding="utf-8")
	(Path(_out_dir) / "mots_cles.txt").write_text("\n".join(artifacts.keywords), encoding="utf-8")
	(Path(_out_dir) / "flashcards.txt").write_text(
		"\n".join([f"Q: {q}\nA: {a}" for q, a in artifacts.flashcards]), encoding="utf-8"
	)
	quiz_lines: List[str] = []
	for q, options, ans in artifacts.quiz_mcq:
		quiz_lines.append(q)
		for idx, opt in enumerate(options):
			letter = chr(ord("A") + idx)
			quiz_lines.append(f"  {letter}) {opt}")
		quiz_lines.append(f"Réponse: {ans}")
		quiz_lines.append("")
	(Path(_out_dir) / "quiz.txt").write_text("\n".join(quiz_lines), encoding="utf-8")

	console.print(f"[green]Fichiers générés dans[/green] {_out_dir}")


def main() -> None:
	parser = argparse.ArgumentParser(description="Génère des supports d'étude à partir d'un fichier.")
	parser.add_argument("input", help="Chemin vers un fichier ou un dossier")
	parser.add_argument("--llm", action="store_true", help="Activer l'amélioration via OpenAI si disponible")
	parser.add_argument("--out", help="Dossier de sortie", default=None)
	args = parser.parse_args()

	input_path = args.input
	if os.path.isdir(input_path):
		for root, _, files in os.walk(input_path):
			for f in files:
				if os.path.splitext(f)[1].lower() in {".pdf", ".docx", ".txt", ".md"}:
					process_file(os.path.join(root, f), use_llm=args.llm, out_dir=args.out)
	elif os.path.isfile(input_path):
		process_file(input_path, use_llm=args.llm, out_dir=args.out)
	else:
		console.print(f"[red]Chemin invalide:[/red] {input_path}")


if __name__ == "__main__":
	main()