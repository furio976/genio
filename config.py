import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Video Settings
    VIDEO_DURATION = int(os.getenv('VIDEO_DURATION', 60))
    VIDEO_WIDTH = int(os.getenv('VIDEO_WIDTH', 1920))
    VIDEO_HEIGHT = int(os.getenv('VIDEO_HEIGHT', 1080))
    VIDEO_FPS = int(os.getenv('VIDEO_FPS', 30))
    
    # Content Settings
    CONTENT_LANGUAGE = os.getenv('CONTENT_LANGUAGE', 'fr')
    VIDEO_TOPIC_CATEGORY = os.getenv('VIDEO_TOPIC_CATEGORY', 'general')
    DAILY_SCHEDULE_TIME = os.getenv('DAILY_SCHEDULE_TIME', '09:00')
    
    # Directory Settings
    OUTPUT_DIRECTORY = os.getenv('OUTPUT_DIRECTORY', './videos')
    TEMP_DIRECTORY = os.getenv('TEMP_DIRECTORY', './temp')
    
    # TTS Settings
    TTS_LANGUAGE = os.getenv('TTS_LANGUAGE', 'fr')
    TTS_VOICE_SPEED = float(os.getenv('TTS_VOICE_SPEED', 1.0))
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        os.makedirs(cls.OUTPUT_DIRECTORY, exist_ok=True)
        os.makedirs(cls.TEMP_DIRECTORY, exist_ok=True)
        
    @classmethod
    def get_daily_filename(cls):
        """Generate filename for today's video"""
        today = datetime.now().strftime('%Y-%m-%d')
        return f"video_{today}.mp4"
        
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required. Please set it in your .env file.")
        
        return True