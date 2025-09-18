#!/usr/bin/env python3
import argparse
import datetime as dt
import os
import random
import subprocess
import sys
import textwrap
from pathlib import Path

from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg as iio_ffmpeg


DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent.parent / "videos"
WORK_DIR = Path(__file__).resolve().parent.parent / "output"
FALLBACK_FONT_PATHS = [
	"/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
	"/usr/share/fonts/truetype/freefont/FreeSans.ttf",
	"/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
]


def ensure_directories() -> None:
	DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
	WORK_DIR.mkdir(parents=True, exist_ok=True)


def choose_font(preferred_path: str | None, size: int) -> ImageFont.FreeTypeFont:
	candidate_paths: list[str] = []
	if preferred_path:
		candidate_paths.append(preferred_path)
	candidate_paths.extend(FALLBACK_FONT_PATHS)
	for path in candidate_paths:
		if os.path.exists(path):
			return ImageFont.truetype(path, size=size)
	return ImageFont.load_default()


def generate_gradient_background(width: int, height: int) -> Image.Image:
	top_color = (11, 18, 32)
	bottom_color = (24, 39, 71)
	image = Image.new("RGB", (width, height), top_color)
	draw = ImageDraw.Draw(image)
	for y in range(height):
		r = int(top_color[0] + (bottom_color[0] - top_color[0]) * y / height)
		g = int(top_color[1] + (bottom_color[1] - top_color[1]) * y / height)
		b = int(top_color[2] + (bottom_color[2] - top_color[2]) * y / height)
		draw.line([(0, y), (width, y)], fill=(r, g, b))
	return image


def draw_text_card(base_img: Image.Image, title: str, body: str, font_path: str | None) -> Image.Image:
	img = base_img.copy()
	draw = ImageDraw.Draw(img)

	w, h = img.size
	margin = int(w * 0.08)
	title_font = choose_font(font_path, size=int(w * 0.08))
	body_font = choose_font(font_path, size=int(w * 0.055))

	title_bbox = draw.textbbox((0, 0), title, font=title_font)
	title_height = title_bbox[3] - title_bbox[1]
	draw.text((margin, margin), title, fill=(235, 242, 255), font=title_font)

	wrapped = textwrap.fill(body, width=28)
	lines = wrapped.splitlines()
	y = margin + title_height + int(h * 0.03)
	for line in lines:
		line_bbox = draw.textbbox((0, 0), line, font=body_font)
		line_height = line_bbox[3] - line_bbox[1]
		draw.text((margin, y), line, fill=(220, 230, 245), font=body_font)
		y += line_height + int(h * 0.01)

	date_text = dt.date.today().isoformat()
	footer_font = choose_font(font_path, size=int(w * 0.045))
	date_bbox = draw.textbbox((0, 0), date_text, font=footer_font)
	date_w = date_bbox[2] - date_bbox[0]
	draw.text((w - margin - date_w, h - margin - (date_bbox[3] - date_bbox[1])), date_text, fill=(200, 210, 225), font=footer_font)

	return img


def synthesize_tts(text: str, lang: str, audio_path: Path) -> None:
	tts = gTTS(text=text, lang=lang)
	audio_path.parent.mkdir(parents=True, exist_ok=True)
	tts.save(str(audio_path))


def build_video(still_image: Path, audio_file: Path, output_path: Path) -> None:
	ffmpeg_path = iio_ffmpeg.get_ffmpeg_exe()
	cmd = [
		ffmpeg_path,
		"-y",
		"-loop", "1",
		"-framerate", "30",
		"-i", str(still_image),
		"-i", str(audio_file),
		"-c:v", "libx264",
		"-preset", "veryfast",
		"-crf", "23",
		"-vf", "scale=1080:1920,format=yuv420p",
		"-pix_fmt", "yuv420p",
		"-tune", "stillimage",
		"-c:a", "aac",
		"-b:a", "128k",
		"-shortest",
		"-movflags", "+faststart",
		str(output_path),
	]
	completed = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
	if completed.returncode != 0:
		raise RuntimeError(f"ffmpeg failed with code {completed.returncode}:\n{completed.stdout}")


def default_phrases() -> list[str]:
	return [
		"Chaque jour est une nouvelle chance de faire mieux.",
		"Le secret pour avancer est de commencer.",
		"Petit à petit, l'oiseau fait son nid.",
		"Crois en toi et tout devient possible.",
		"La constance bat toujours le talent, quand le talent n'est pas constant.",
		"Un pas à la fois suffit pour parcourir le chemin.",
	]


def make_text(topic: str | None) -> str:
	if topic:
		return f"Pensée du jour sur {topic} : " + random.choice(default_phrases())
	return "Pensée du jour : " + random.choice(default_phrases())


def main() -> int:
	parser = argparse.ArgumentParser(description="Génère une vidéo verticale quotidienne avec TTS FR")
	parser.add_argument("--texte", dest="texte", type=str, default=None, help="Texte à vocaliser (optionnel)")
	parser.add_argument("--sujet", dest="sujet", type=str, default=None, help="Thème facultatif pour la phrase par défaut")
	parser.add_argument("--sortie", dest="sortie", type=Path, default=None, help="Chemin du fichier vidéo de sortie")
	parser.add_argument("--font", dest="font", type=str, default=None, help="Chemin d'une police .ttf à utiliser")
	parser.add_argument("--lang", dest="lang", type=str, default="fr", help="Code langue TTS (par défaut: fr)")

	args = parser.parse_args()

	ensure_directories()

	text = args.texte or make_text(args.sujet)

	width, height = 1080, 1920
	background = generate_gradient_background(width, height)
	card = draw_text_card(background, title="Pensée du jour", body=text, font_path=args.font)

	still_path = WORK_DIR / "frame.png"
	card.save(still_path)

	audio_path = WORK_DIR / "audio.mp3"
	synthesize_tts(text, lang=args.lang, audio_path=audio_path)

	if args.sortie is not None:
		output_path = Path(args.sortie)
		output_path.parent.mkdir(parents=True, exist_ok=True)
	else:
		date_str = dt.date.today().isoformat()
		output_path = DEFAULT_OUTPUT_DIR / f"video_{date_str}.mp4"

	build_video(still_image=still_path, audio_file=audio_path, output_path=output_path)
	print(f"Vidéo générée : {output_path}")
	return 0


if __name__ == "__main__":
	sys.exit(main())