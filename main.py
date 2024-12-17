import os
from dotenv import load_dotenv
from src.quiz.generator import QuizGenerator
from src.video.generator import QuizVideoGenerator
from src.utils.youtube_uploader import YouTubeUploader
from src.quiz_topics import get_random_topic
from datetime import datetime

def generate_video_metadata(quiz_data_list, topic_info):
    """동영상 메타데이터 생성"""
    title = f"Fun {topic_info['name']} Quiz! | Test Your Knowledge 🎯"
    
    description_topics = [quiz["question"].replace("?", "").lower() for quiz in quiz_data_list]
    description = (
        f"Test your knowledge about {topic_info['name'].lower()} with this fun quiz!\n\n"
        f"In this quiz, you'll learn about:\n"
        f"✨ {description_topics[0]}\n"
        f"✨ {description_topics[1]}\n"
        f"✨ {description_topics[2]}\n\n"
        f"#quiz #learning #{topic_info['id']} #{topic_info['name'].lower().replace(' ', '')} #educational #shorts"
    )
    
    return title, description

def setup_directories():
    """필요한 디렉토리 생성"""
    directories = [
        "output",
        "output/date",
        "assets/images",
        "assets/audio",
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def main():
    try:
        # 환경 변수 로드
        load_dotenv()
        
        # 디렉토리 설정
        setup_directories()

        # 인스턴스 생성
        quiz_gen = QuizGenerator(os.getenv("CLAUDE_API_KEY"))
        video_gen = QuizVideoGenerator()
        youtube_uploader = YouTubeUploader()
        
        # 랜덤한 퀴즈 주제 선택
        topic_info = get_random_topic()
        print(f"\nSelected topic: {topic_info['name']} ({topic_info['id']})")
        
        # 퀴즈 생성
        quiz_data_list = quiz_gen.generate_quiz(
            topic_info['id'],
            count=3,
            prompt=topic_info['prompt']
        )
        
        if not quiz_data_list:
            print("Failed to generate quiz data")
            return
            
        # 비디오 생성
        print("Creating video...")
        video_file = video_gen.create_video(
            quiz_data_list, 
            category=f"{topic_info['name']} Quiz"
        )
        
        if not video_file:
            print("Failed to generate video")
            return
            
        print(f"Video created: {video_file}")
        
        # 배경음악과 TTS 추가
        print("\nAdding background music and TTS...")
        final_video = video_gen.add_background_music(video_file, quiz_data_list)  # quiz_data_list 추가
        
        if not final_video:
            print("Failed to add audio")
            return
            
        print(f"Final video with audio created: {final_video}")
        
        # 메타데이터 생성
        title, description = generate_video_metadata(quiz_data_list, topic_info)
        print("\nUploading to YouTube...")
        print(f"Title: {title}")
        print(f"Description:\n{description}\n")
        
        # YouTube 업로드
        video_id = youtube_uploader.upload_video(
            final_video,
            title=title,
            description=description,
            privacy_status="public"
        )
        
        if video_id:
            print(f"Video uploaded successfully! ID: {video_id}")
        else:
            print("Failed to upload video")
            
    except Exception as e:
        print(f"\nError during execution: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()