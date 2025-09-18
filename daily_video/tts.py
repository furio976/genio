from typing import List
import os
import shutil
import subprocess

try:
	import pyttsx3  # type: ignore
except Exception:  # pragma: no cover
	pyttsx3 = None  # type: ignore


def _synthesize_with_espeak_ng(texts: List[str], out_dir: str) -> List[str]:
	paths: List[str] = []
	for idx, text in enumerate(texts, start=1):
		path = os.path.join(out_dir, f"audio_{idx:02d}.wav")
		# -w: output wav, -s: speed (wpm), -v: voice, -a: amplitude
		cmd = [
			"espeak-ng",
			"-w", path,
			"-s", "170",
			"-v", "fr+f3",
			"-a", "200",
			text,
		]
		subprocess.run(cmd, check=True)
		paths.append(path)
	return paths


def _synthesize_with_pyttsx3(texts: List[str], out_dir: str) -> List[str]:
	if pyttsx3 is None:
		raise RuntimeError("pyttsx3 non disponible et espeak-ng introuvable")
	engine = pyttsx3.init()
	engine.setProperty('rate', 170)
	engine.setProperty('volume', 1.0)
	# Try to select a French voice if available
	for v in engine.getProperty('voices'):
		if hasattr(v, 'languages') and v.languages and any('fr' in str(lang).lower() for lang in v.languages):
			engine.setProperty('voice', v.id)
			break

	paths: List[str] = []
	for idx, text in enumerate(texts, start=1):
		path = os.path.join(out_dir, f"audio_{idx:02d}.wav")
		engine.save_to_file(text, path)
		engine.runAndWait()
		paths.append(path)
	engine.stop()
	return paths


def synthesize_audios(texts: List[str], out_dir: str) -> List[str]:
	os.makedirs(out_dir, exist_ok=True)
	if shutil.which("espeak-ng") is not None:
		return _synthesize_with_espeak_ng(texts, out_dir)
	return _synthesize_with_pyttsx3(texts, out_dir)