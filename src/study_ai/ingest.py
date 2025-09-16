from __future__ import annotations

import os
from typing import List

from pypdf import PdfReader
from docx import Document


def read_text_from_file(input_path: str) -> str:
	"""Read text content from PDF, DOCX, or TXT file.

	Args:
		input_path: Absolute path to the input file.

	Returns:
		Extracted text content as a single string.
	"""
	if not os.path.isfile(input_path):
		raise FileNotFoundError(f"File not found: {input_path}")

	extension = os.path.splitext(input_path)[1].lower()
	if extension == ".pdf":
		return _read_pdf(input_path)
	elif extension in {".docx"}:
		return _read_docx(input_path)
	elif extension in {".txt", ".md"}:
		with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
			return f.read()
	else:
		raise ValueError(
			f"Unsupported file type: {extension}. Supported: PDF, DOCX, TXT, MD"
		)


def _read_pdf(input_path: str) -> str:
	reader = PdfReader(input_path)
	texts: List[str] = []
	for page in reader.pages:
		try:
			texts.append(page.extract_text() or "")
		except Exception:
			# Skip problematic pages but continue
			continue
	return "\n\n".join(texts)


def _read_docx(input_path: str) -> str:
	doc = Document(input_path)
	paras = [p.text.strip() for p in doc.paragraphs if p.text and p.text.strip()]
	return "\n".join(paras)