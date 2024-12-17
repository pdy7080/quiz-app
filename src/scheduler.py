# src/scheduler.py
import os
import time
import schedule
import traceback
from datetime import datetime, timedelta
from dotenv import load_dotenv
from src.quiz.generator import QuizGenerator
from src.video.generator import QuizVideoGenerator
from src.utils.youtube_uploader import YouTubeUploader
from src.quiz_topics import get_random_topic

# YouTube API 관련 imports
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

class QuizScheduler:
    def __init__(self):
        # 환경 변수 로드
        load_dotenv()
        
        # 디렉토리 생성
        self.setup_directories()
        
        # 인스턴스 생성
        self.quiz_gen = QuizGenerator(os.getenv("CLAUDE_API_KEY"))
        self.video_gen = QuizVideoGenerator()
        self.youtube_uploader = YouTubeUploader()
        
        # 일일 업로드 제한 관리
        self.daily_upload_count = 0
        self.last_upload_date = None
        self.MAX_DAILY_UPLOADS = 5

    def setup_directories(self):
        """필요한 디렉토리 생성"""
        directories = [
            "output",
            "output/date",
            "assets/images",
            "assets/audio",
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def reset_daily_count(self):
        """매일 자정에 업로드 카운트 초기화"""
        current_date = datetime.now().date()
        if self.last_upload_date != current_date:
            self.daily_upload_count = 0
            self.last_upload_date = current_date
            print(f"Reset daily upload count for {current_date}")

    def generate_metadata(self, quiz_data_list, topic_info):
        """메타데이터 생성"""
        description_topics = [quiz["question"].replace("?", "").lower() for quiz in quiz_data_list]
        description = (
            f"Test your knowledge about {topic_info['name'].lower()} with this fun quiz!\n\n"
            f"In this quiz, you'll learn about:\n"
            f"✨ {description_topics[0]}\n"
            f"✨ {description_topics[1]}\n"
            f"✨ {description_topics[2]}\n\n"
            f"#quiz #learning #{topic_info['id']} "
            f"#{topic_info['name'].lower().replace(' ', '')} "
            f"#educational #shorts #1minuteknowledge"
        )
        
        title = f"Fun {topic_info['name']} Quiz! | Test Your Knowledge 🎯"
        
        return title, description
        
    def create_and_upload_quiz(self):
        """퀴즈 생성 및 업로드 작업"""
        try:
            current_time = datetime.now()
            print(f"\nStarting scheduled task at {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # 일일 업로드 카운트 체크
            self.reset_daily_count()
            if self.daily_upload_count >= self.MAX_DAILY_UPLOADS:
                print(f"Daily upload limit ({self.MAX_DAILY_UPLOADS}) reached. Skipping upload.")
                return
            
            # 랜덤 주제 선택
            topic_info = get_random_topic()
            print(f"Selected topic: {topic_info['name']} ({topic_info['id']})")
            
            # 퀴즈 생성
            quiz_data_list = self.quiz_gen.generate_quiz(
                topic_info['id'],
                count=3,
                prompt=topic_info['prompt']
            )
            
            if not quiz_data_list:
                print("Failed to generate quiz data")
                return
            
            # 비디오 생성
            print("Creating video...")
            video_file = self.video_gen.create_video(quiz_data_list, category=f"{topic_info['name']} Quiz")
            
            if not video_file:
                print("Failed to generate video")
                return
                
            print(f"Video created: {video_file}")
            
            # 배경음악과 TTS 추가
            print("\nAdding background music and TTS...")
            final_video = self.video_gen.add_background_music(video_file, quiz_data_list)
            
            if not final_video:
                print("Failed to add audio")
                return
                
            print(f"Final video with audio created: {final_video}")
            
            # 일일 업로드 제한 체크
            if self.daily_upload_count >= self.MAX_DAILY_UPLOADS:
                print("Daily upload limit reached. Skipping upload.")
                return
            
            # 메타데이터 생성 및 업로드
            title, description = self.generate_metadata(quiz_data_list, topic_info)
            print("\nUploading to YouTube...")
            print(f"Title: {title}")
            print(f"Description:\n{description}")
            
            video_id = self.youtube_uploader.upload_video(
                final_video,
                title=title,
                description=description,
                privacy_status="public"
            )
            
            if video_id:
                self.daily_upload_count += 1
                print(f"Video uploaded successfully! ID: {video_id}")
                print(f"Daily uploads: {self.daily_upload_count}/{self.MAX_DAILY_UPLOADS}")
            else:
                print("Failed to upload video")
                
        except Exception as e:
            print(f"Error during scheduled task: {str(e)}")
            traceback.print_exc()

def run_scheduler():
    scheduler = QuizScheduler()
    
    schedule.every().day.at("08:50").do(scheduler.create_and_upload_quiz)
    schedule.every().day.at("16:00").do(scheduler.create_and_upload_quiz)

    
    print("Scheduler started...")
    print("Scheduled upload times: 08:50, 16:00")
    print(f"Maximum daily uploads: {scheduler.MAX_DAILY_UPLOADS}")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\nScheduler stopped by user")
    except Exception as e:
        print(f"\nScheduler stopped due to error: {str(e)}")