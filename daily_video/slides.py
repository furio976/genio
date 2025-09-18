from typing import List, Dict, Tuple
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os


DEFAULT_SIZE: Tuple[int, int] = (1080, 1920)  # portrait 9:16
BACKGROUND_COLOR = (18, 18, 18)
TITLE_COLOR = (255, 255, 255)
TEXT_COLOR = (220, 220, 220)
MARGIN = 80


def _load_font(size: int) -> ImageFont.FreeTypeFont:
	# Try to load a common font; fall back to default
	for font_name in [
		"DejaVuSans-Bold.ttf",
		"Arial.ttf",
		"LiberationSans-Bold.ttf",
	]:
		try:
			return ImageFont.truetype(font_name, size=size)
		except Exception:
			continue
	return ImageFont.load_default()


def render_slides(slides: List[Dict[str, str]], out_dir: str) -> List[str]:
	os.makedirs(out_dir, exist_ok=True)
	paths: List[str] = []

	for idx, slide in enumerate(slides, start=1):
		img = Image.new("RGB", DEFAULT_SIZE, BACKGROUND_COLOR)
		draw = ImageDraw.Draw(img)

		title_font = _load_font(72)
		body_font = _load_font(44)

		# Title
		title = slide.get("title", "")
		title_wrapped = textwrap.fill(title, width=18)
		draw.text((MARGIN, MARGIN), title_wrapped, font=title_font, fill=TITLE_COLOR)

		# Body text below title
		bbox = draw.multiline_textbbox((MARGIN, MARGIN), title_wrapped, font=title_font)
		title_height = bbox[3] - bbox[1]
		body_y = MARGIN + title_height + 40
		body = slide.get("text", "")
		body_wrapped = textwrap.fill(body, width=28)
		draw.multiline_text((MARGIN, body_y), body_wrapped, font=body_font, fill=TEXT_COLOR, spacing=8)

		path = os.path.join(out_dir, f"slide_{idx:02d}.png")
		img.save(path)
		paths.append(path)

	return paths