# src/audio/tts_generator.py
from google.cloud import texttospeech
from pydub import AudioSegment
import os

class AudioGenerator:
    def __init__(self, language_code="en-US"):
        self.client = texttospeech.TextToSpeechClient()
        self.language_code = language_code
        self.voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name="en-US-Neural2-D",
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

    def generate_tts(self, text, output_path):
        """TTS 생성"""
        synthesis_input = texttospeech.SynthesisInput(text=text)
        response = self.client.synthesize_speech(
            input=synthesis_input,
            voice=self.voice,
            audio_config=self.audio_config
        )

        with open(output_path, "wb") as out:
            out.write(response.audio_content)
        return output_path

    def create_quiz_audio(self, quiz_data, base_path):
        """퀴즈 오디오 생성"""
        audio_paths = {
            'question': self.generate_tts(
                quiz_data['question'],
                os.path.join(base_path, f"question_{quiz_data['id']}.mp3")
            ),
            'answer': self.generate_tts(
                f"The answer is {quiz_data['answer']}",
                os.path.join(base_path, f"answer_{quiz_data['id']}.mp3")
            ),
            'fact': self.generate_tts(
                quiz_data['fun_fact'],
                os.path.join(base_path, f"fact_{quiz_data['id']}.mp3")
            )
        }
        return audio_paths

# src/audio/audio_mixer.py
class AudioMixer:
    def __init__(self, base_path="assets/audio"):
        self.base_path = base_path
        self.bgm_path = os.path.join(base_path, "bgm")
        self.effects_path = os.path.join(base_path, "effects")

    def load_bgm(self, filename):
        """배경 음악 로드"""
        return AudioSegment.from_file(os.path.join(self.bgm_path, filename))

    def load_effect(self, effect_name):
        """효과음 로드"""
        return AudioSegment.from_file(os.path.join(self.effects_path, effect_name))

    def create_quiz_section_audio(self, tts_paths, duration=15000):
        """퀴즈 섹션 오디오 생성"""
        # 기본 배경음악
        bgm = self.load_bgm("quiz_bgm.mp3")
        bgm = bgm[:duration]
        bgm = bgm - 20  # 배경음악 볼륨 낮춤

        # TTS 로드
        question = AudioSegment.from_file(tts_paths['question'])
        answer = AudioSegment.from_file(tts_paths['answer'])
        fact = AudioSegment.from_file(tts_paths['fact'])

        # 효과음 로드
        timer_tick = self.load_effect("timer_tick.mp3")
        correct_sound = self.load_effect("correct.mp3")

        # 최종 오디오 생성
        final_audio = bgm
        
        # 질문 추가 (0초)
        final_audio = final_audio.overlay(question, position=0)
        
        # 타이머 효과음 추가 (4-8초)
        for i in range(4):
            final_audio = final_audio.overlay(timer_tick, position=4000 + (i * 1000))
        
        # 정답 효과음 및 나레이션 추가 (8초)
        final_audio = final_audio.overlay(correct_sound, position=8000)
        final_audio = final_audio.overlay(answer, position=8500)
        
        # 재미있는 사실 추가 (11초)
        final_audio = final_audio.overlay(fact, position=11000)

        return final_audio

    def create_full_video_audio(self, quiz_data_list):
        """전체 비디오 오디오 생성"""
        # 인트로 음악
        intro = self.load_bgm("intro.mp3")[:8000]
        
        # 퀴즈 섹션 오디오
        quiz_sections_audio = []
        for quiz_data in quiz_data_list:
            section_audio = self.create_quiz_section_audio(quiz_data['audio_paths'])
            quiz_sections_audio.append(section_audio)
        
        # 아웃트로 음악
        outro = self.load_bgm("outro.mp3")[:7000]
        
        # 전체 오디오 합치기
        final_audio = intro
        for section_audio in quiz_sections_audio:
            final_audio += section_audio
        final_audio += outro

        return final_audio