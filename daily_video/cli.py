import argparse
import os
from datetime import date
from daily_video.content import generate_daily_script
from daily_video.slides import render_slides
from daily_video.tts import synthesize_audios
from daily_video.video import assemble_video


def run():
	parser = argparse.ArgumentParser(description="Générateur de vidéo quotidienne")
	parser.add_argument("--topic", type=str, default="", help="Sujet de la vidéo")
	parser.add_argument("--slides", type=int, default=5, help="Nombre de slides")
	parser.add_argument("--out", type=str, default="output", help="Dossier de sortie")
	parser.add_argument("--basename", type=str, default="daily_video", help="Nom de base du fichier vidéo")
	args = parser.parse_args()

	script = generate_daily_script(topic=args.topic, num_slides=args.slides)

	date_str = date.today().strftime("%Y-%m-%d")
	work_dir = os.path.join(args.out, date_str)
	img_dir = os.path.join(work_dir, "images")
	audio_dir = os.path.join(work_dir, "audio")
	video_path = os.path.join(args.out, f"{args.basename}_{date_str}.mp4")

	slide_paths = render_slides(script, img_dir)
	texts = [s.get("text", "") for s in script]
	audio_paths = synthesize_audios(texts, audio_dir)

	assembled = assemble_video(slide_paths, audio_paths, video_path)
	print(f"Vidéo générée: {assembled}")