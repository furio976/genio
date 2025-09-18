import os
import random
from datetime import datetime
from gtts import gTTS
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import requests
from config import Config

class VideoGenerator:
    def __init__(self):
        Config.ensure_directories()
        
    def text_to_speech(self, text, output_path):
        """Convert text to speech using gTTS"""
        try:
            tts = gTTS(
                text=text, 
                lang=Config.TTS_LANGUAGE, 
                slow=False
            )
            tts.save(output_path)
            print(f"Audio généré: {output_path}")
            return True
        except Exception as e:
            print(f"Erreur lors de la génération audio: {e}")
            return False
    
    def create_background_image(self, title, width=1920, height=1080):
        """Create a background image with gradient and title"""
        # Create gradient background
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        # Generate random gradient colors
        colors = [
            [(64, 128, 255), (128, 64, 255)],  # Blue to Purple
            [(255, 128, 64), (255, 64, 128)],  # Orange to Pink
            [(128, 255, 64), (64, 255, 128)],  # Green gradient
            [(255, 64, 64), (255, 128, 64)],   # Red to Orange
            [(64, 255, 255), (64, 128, 255)]   # Cyan to Blue
        ]
        
        color_pair = random.choice(colors)
        start_color, end_color = color_pair
        
        # Create vertical gradient
        for y in range(height):
            ratio = y / height
            r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Add title text
        try:
            # Try to use a nice font, fallback to default if not available
            font_size = 72
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # Wrap text if too long
        words = title.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            bbox = draw.textbbox((0, 0), test_line, font=font)
            text_width = bbox[2] - bbox[0]
            
            if text_width > width - 200:  # Leave margin
                if current_line:
                    lines.append(current_line)
                    current_line = word
                else:
                    lines.append(word)
            else:
                current_line = test_line
        
        if current_line:
            lines.append(current_line)
        
        # Draw text lines
        total_height = len(lines) * (font_size + 10)
        start_y = (height - total_height) // 2
        
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (width - text_width) // 2
            y = start_y + i * (font_size + 10)
            
            # Draw text shadow
            draw.text((x + 3, y + 3), line, font=font, fill=(0, 0, 0, 128))
            # Draw main text
            draw.text((x, y), line, font=font, fill=(255, 255, 255))
        
        return img
    
    def create_video(self, content_data):
        """Create video from content data"""
        title = content_data['title']
        script = content_data['script']
        
        print(f"Création de la vidéo: {title}")
        
        # File paths
        audio_path = os.path.join(Config.TEMP_DIRECTORY, "audio.mp3")
        background_path = os.path.join(Config.TEMP_DIRECTORY, "background.png")
        output_path = os.path.join(Config.OUTPUT_DIRECTORY, Config.get_daily_filename())
        
        try:
            # Generate audio
            if not self.text_to_speech(script, audio_path):
                return False
            
            # Create background image
            background_img = self.create_background_image(title, Config.VIDEO_WIDTH, Config.VIDEO_HEIGHT)
            background_img.save(background_path)
            
            # Load audio to get duration
            audio_clip = AudioFileClip(audio_path)
            audio_duration = audio_clip.duration
            
            # Create video clip
            background_clip = ImageClip(background_path, duration=audio_duration)
            background_clip = background_clip.set_fps(Config.VIDEO_FPS)
            
            # Combine video and audio
            final_video = background_clip.set_audio(audio_clip)
            
            # Write final video
            final_video.write_videofile(
                output_path,
                fps=Config.VIDEO_FPS,
                audio_codec='aac',
                codec='libx264',
                temp_audiofile=os.path.join(Config.TEMP_DIRECTORY, 'temp-audio.m4a'),
                remove_temp=True,
                verbose=False,
                logger=None
            )
            
            # Cleanup
            audio_clip.close()
            background_clip.close()
            final_video.close()
            
            # Remove temporary files
            if os.path.exists(audio_path):
                os.remove(audio_path)
            if os.path.exists(background_path):
                os.remove(background_path)
            
            print(f"Vidéo créée avec succès: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Erreur lors de la création de la vidéo: {e}")
            return False
    
    def add_subtitles(self, video_path, script, output_path=None):
        """Add subtitles to video (optional enhancement)"""
        if not output_path:
            output_path = video_path.replace('.mp4', '_with_subtitles.mp4')
        
        try:
            video = VideoFileClip(video_path)
            
            # Simple subtitle implementation
            # Split script into chunks based on duration
            words = script.split()
            duration = video.duration
            words_per_second = len(words) / duration
            
            subtitle_clips = []
            chunk_duration = 3  # 3 seconds per subtitle
            words_per_chunk = int(words_per_second * chunk_duration)
            
            for i in range(0, len(words), words_per_chunk):
                chunk_words = words[i:i + words_per_chunk]
                chunk_text = ' '.join(chunk_words)
                
                start_time = i / words_per_second
                end_time = min(start_time + chunk_duration, duration)
                
                if start_time < duration:
                    txt_clip = TextClip(
                        chunk_text,
                        fontsize=40,
                        color='white',
                        font='Arial-Bold',
                        stroke_color='black',
                        stroke_width=2
                    ).set_position(('center', 'bottom')).set_start(start_time).set_end(end_time)
                    
                    subtitle_clips.append(txt_clip)
            
            # Composite video with subtitles
            final_video = CompositeVideoClip([video] + subtitle_clips)
            final_video.write_videofile(output_path, verbose=False, logger=None)
            
            video.close()
            final_video.close()
            
            return output_path
            
        except Exception as e:
            print(f"Erreur lors de l'ajout des sous-titres: {e}")
            return video_path
    
    def get_video_info(self, video_path):
        """Get information about the generated video"""
        if not os.path.exists(video_path):
            return None
        
        try:
            video = VideoFileClip(video_path)
            info = {
                'path': video_path,
                'duration': video.duration,
                'fps': video.fps,
                'size': video.size,
                'file_size': os.path.getsize(video_path)
            }
            video.close()
            return info
        except Exception as e:
            print(f"Erreur lors de la récupération des infos vidéo: {e}")
            return None