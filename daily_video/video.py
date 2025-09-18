from typing import List
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import os


def assemble_video(slide_paths: List[str], audio_paths: List[str], out_path: str) -> str:
	if len(slide_paths) != len(audio_paths):
		raise ValueError("slide_paths and audio_paths must have the same length")

	clips: List[ImageClip] = []
	for img_path, audio_path in zip(slide_paths, audio_paths):
		audio = AudioFileClip(audio_path)
		img_clip = ImageClip(img_path).set_duration(audio.duration).set_audio(audio)
		# Ensure proper size for portrait 1080x1920
		img_clip = img_clip.set_fps(30)
		clips.append(img_clip)

	final = concatenate_videoclips(clips, method="compose")
	os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
	final.write_videofile(out_path, fps=30, codec="libx264", audio_codec="aac")
	return out_path