import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
    UNSPLASH_API_KEY = os.getenv('UNSPLASH_API_KEY')