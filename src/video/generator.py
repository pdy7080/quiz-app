# src/video/generator.py
import os
from moviepy.editor import *
from moviepy.config import change_settings
import numpy as np
import random
import cv2
import traceback
import textwrap
import requests
from datetime import datetime
import shutil
from googleapiclient.discovery import build  # Google API 관련 import 추가

# ImageMagick 경로 설정
IMAGEMAGICK_BINARY = os.getenv('IMAGEMAGICK_BINARY', r'C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe')
change_settings({"IMAGEMAGICK_BINARY": IMAGEMAGICK_BINARY})

# src/video/generator.py 수정

class QuizUIElements:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Google API 키 설정
        self.GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
        self.GOOGLE_SEARCH_ENGINE_ID = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
        
        # 다양한 색상 조합 정의
        self.color_schemes = [
            {
                "name": "blue",
                "colors": {
                    "primary": (45, 85, 255),
                    "secondary": (25, 25, 112),
                    "accent": (255, 255, 255),
                    "button": (255, 255, 255),
                    "button_hover": (240, 240, 240),
                    "text_light": (255, 255, 255),
                    "text_dark": (33, 33, 33)
                }
            },
            {
                "name": "red",
                "colors": {
                    "primary": (255, 99, 71),
                    "secondary": (139, 0, 0),
                    "accent": (255, 255, 255),
                    "button": (255, 255, 255),
                    "button_hover": (240, 240, 240),
                    "text_light": (255, 255, 255),
                    "text_dark": (33, 33, 33)
                }
            },
            {
                "name": "green",
                "colors": {
                    "primary": (50, 205, 50),
                    "secondary": (0, 100, 0),
                    "accent": (255, 255, 255),
                    "button": (255, 255, 255),
                    "button_hover": (240, 240, 240),
                    "text_light": (255, 255, 255),
                    "text_dark": (33, 33, 33)
                }
            },
            {
                "name": "purple",
                "colors": {
                    "primary": (147, 112, 219),
                    "secondary": (75, 0, 130),
                    "accent": (255, 255, 255),
                    "button": (255, 255, 255),
                    "button_hover": (240, 240, 240),
                    "text_light": (255, 255, 255),
                    "text_dark": (33, 33, 33)
                }
            },
            {
                "name": "orange",
                "colors": {
                    "primary": (255, 165, 0),
                    "secondary": (184, 134, 11),
                    "accent": (255, 255, 255),
                    "button": (255, 255, 255),
                    "button_hover": (240, 240, 240),
                    "text_light": (255, 255, 255),
                    "text_dark": (33, 33, 33)
                }
            },
            {
                "name": "teal",
                "colors": {
                    "primary": (0, 206, 209),
                    "secondary": (0, 139, 139),
                    "accent": (255, 255, 255),
                    "button": (255, 255, 255),
                    "button_hover": (240, 240, 240),
                    "text_light": (255, 255, 255),
                    "text_dark": (33, 33, 33)
                }
            },
            {
                "name": "pink",
                "colors": {
                    "primary": (255, 192, 203),
                    "secondary": (199, 21, 133),
                    "accent": (255, 255, 255),
                    "button": (255, 255, 255),
                    "button_hover": (240, 240, 240),
                    "text_light": (255, 255, 255),
                    "text_dark": (33, 33, 33)
                }
            },
            {
                "name": "yellow",
                "colors": {
                    "primary": (240, 230, 140),
                    "secondary": (184, 134, 11),
                    "accent": (255, 255, 255),
                    "button": (255, 255, 255),
                    "button_hover": (240, 240, 240),
                    "text_light": (255, 255, 255),
                    "text_dark": (33, 33, 33)
                }
            },
            {
                "name": "pastel_blue",
                "colors": {
                    "primary": (95, 158, 160),
                    "secondary": (47, 79, 79),
                    "accent": (255, 255, 255),
                    "button": (255, 255, 255),
                    "button_hover": (240, 240, 240),
                    "text_light": (255, 255, 255),
                    "text_dark": (33, 33, 33)
                }
            },
            {
                "name": "lilac",
                "colors": {
                    "primary": (221, 160, 221),
                    "secondary": (148, 0, 211),
                    "accent": (255, 255, 255),
                    "button": (255, 255, 255),
                    "button_hover": (240, 240, 240),
                    "text_light": (255, 255, 255),
                    "text_dark": (33, 33, 33)
                }
            },
            {
                "name": "sky_blue",
                "colors": {
                    "primary": (135, 206, 250),
                    "secondary": (0, 0, 139),
                    "accent": (255, 255, 255),
                    "button": (255, 255, 255),
                    "button_hover": (240, 240, 240),
                    "text_light": (255, 255, 255),
                    "text_dark": (33, 33, 33)
                }
            },
            {
                "name": "turquoise",
                "colors": {
                    "primary": (64, 224, 208),
                    "secondary": (0, 128, 128),
                    "accent": (255, 255, 255),
                    "button": (255, 255, 255),
                    "button_hover": (240, 240, 240),
                    "text_light": (255, 255, 255),
                    "text_dark": (33, 33, 33)
                }
            },
            {
                "name": "peach",
                "colors": {
                    "primary": (255, 218, 185),
                    "secondary": (210, 105, 30),
                    "accent": (255, 255, 255),
                    "button": (255, 255, 255),
                    "button_hover": (240, 240, 240),
                    "text_light": (255, 255, 255),
                    "text_dark": (33, 33, 33)
                }
            },
            {
                "name": "lime",
                "colors": {
                    "primary": (152, 251, 152),
                    "secondary": (0, 128, 0),
                    "accent": (255, 255, 255),
                    "button": (255, 255, 255),
                    "button_hover": (240, 240, 240),
                    "text_light": (255, 255, 255),
                    "text_dark": (33, 33, 33)
                }
            },
            {
                "name": "violet",
                "colors": {
                    "primary": (238, 130, 238),
                    "secondary": (128, 0, 128),
                    "accent": (255, 255, 255),
                    "button": (255, 255, 255),
                    "button_hover": (240, 240, 240),
                    "text_light": (255, 255, 255),
                    "text_dark": (33, 33, 33)
                }
            },
            {
                "name": "salmon",
                "colors": {
                    "primary": (255, 160, 122),
                    "secondary": (178, 34, 34),
                    "accent": (255, 255, 255),
                    "button": (255, 255, 255),
                    "button_hover": (240, 240, 240),
                    "text_light": (255, 255, 255),
                    "text_dark": (33, 33, 33)
                }
            },
            {
                "name": "powder_blue",
                "colors": {
                    "primary": (176, 224, 230),
                    "secondary": (70, 130, 180),
                    "accent": (255, 255, 255),
                    "button": (255, 255, 255),
                    "button_hover": (240, 240, 240),
                    "text_light": (255, 255, 255),
                    "text_dark": (33, 33, 33)
                }
            },
            {
                "name": "light_pink",
                "colors": {
                    "primary": (255, 182, 193),
                    "secondary": (188, 143, 143),
                    "accent": (255, 255, 255),
                    "button": (255, 255, 255),
                    "button_hover": (240, 240, 240),
                    "text_light": (255, 255, 255),
                    "text_dark": (33, 33, 33)
                }
            },
            {
                "name": "sea_green",
                "colors": {
                    "primary": (143, 188, 143),
                    "secondary": (46, 139, 87),
                    "accent": (255, 255, 255),
                    "button": (255, 255, 255),
                    "button_hover": (240, 240, 240),
                    "text_light": (255, 255, 255),
                    "text_dark": (33, 33, 33)
                }
            },
            {
                "name": "thistle",
                "colors": {
                    "primary": (216, 191, 216),
                    "secondary": (153, 50, 204),
                    "accent": (255, 255, 255),
                    "button": (255, 255, 255),
                    "button_hover": (240, 240, 240),
                    "text_light": (255, 255, 255),
                    "text_dark": (33, 33, 33)
                }
            },
            {
                "name": "navajo_white",
                "colors": {
                    "primary": (255, 222, 173),
                    "secondary": (205, 133, 63),
                    "accent": (255, 255, 255),
                    "button": (255, 255, 255),
                    "button_hover": (240, 240, 240),
                    "text_light": (255, 255, 255),
                    "text_dark": (33, 33, 33)
                }
            },
            {
                "name": "pale_turquoise",
                "colors": {
                    "primary": (175, 238, 238),
                    "secondary": (0, 139, 139),
                    "accent": (255, 255, 255),
                    "button": (255, 255, 255),
                    "button_hover": (240, 240, 240),
                    "text_light": (255, 255, 255),
                    "text_dark": (33, 33, 33)
                }
            },
            {
                "name": "hot_pink",
                "colors": {
                    "primary": (255, 105, 180),
                    "secondary": (219, 112, 147),
                    "accent": (255, 255, 255),
                    "button": (255, 255, 255),
                    "button_hover": (240, 240, 240),
                    "text_light": (255, 255, 255),
                    "text_dark": (33, 33, 33)
                }
            },
            {
                "name": "light_blue",
                "colors": {
                    "primary": (173, 216, 230),
                    "secondary": (0, 0, 205),
                    "accent": (255, 255, 255),
                    "button": (255, 255, 255),
                    "button_hover": (240, 240, 240),
                    "text_light": (255, 255, 255),
                    "text_dark": (33, 33, 33)
                }
            },
            {
                "name": "light_green",
                "colors": {
                    "primary": (144, 238, 144),
                    "secondary": (34, 139, 34),
                    "accent": (255, 255, 255),
                    "button": (255, 255, 255),
                    "button_hover": (240, 240, 240),
                    "text_light": (255, 255, 255),
                    "text_dark": (33, 33, 33)
                }
            }
        ]
        
        # 랜덤하게 색상 선택
        self.current_scheme = random.choice(self.color_schemes)
        print(f"Selected color scheme: {self.current_scheme['name']}")


    def _interpolate_color(self, color1, color2, factor):
        """두 색상 사이의 중간 색상 계산"""
        return tuple(
            int(c1 + (c2 - c1) * factor)
            for c1, c2 in zip(color1, color2)
        )

    def create_geometric_background(self, frame_number):
        """현대적인 기하학적 패턴 배경"""
        bg = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # 기본 그라데이션
        for y in range(self.height):
            progress = y / self.height
            color = self._interpolate_color(
                self.current_scheme["colors"]["primary"],
                self.current_scheme["colors"]["secondary"],
                progress
            )
            bg[y, :] = color
        
        # 동적 육각형 패턴
        hex_size = 150
        hex_spacing = int(hex_size * 1.5)
        rows = self.height // hex_spacing + 2
        cols = self.width // hex_spacing + 2
        
        for row in range(rows):
            for col in range(cols):
                x = col * hex_spacing
                y = row * hex_spacing
                if col % 2:
                    y += hex_spacing // 2
                    
                # 육각형 회전 애니메이션
                angle = frame_number * 0.02 + (row + col) * 0.1
                points = []
                for i in range(6):
                    theta = angle + i * np.pi / 3
                    px = x + hex_size * np.cos(theta)
                    py = y + hex_size * np.sin(theta)
                    points.append([[int(px), int(py)]])
                
                points = np.array(points, dtype=np.int32)
                color = self._interpolate_color(
                    self.current_scheme["colors"]["primary"],
                    self.current_scheme["colors"]["accent"],
                    np.sin(angle) * 0.5 + 0.5
                )
                
                # 육각형 그리기
                overlay = bg.copy()
                cv2.fillPoly(overlay, [points], color)
                cv2.addWeighted(overlay, 0.3, bg, 0.7, 0, bg)
                cv2.polylines(bg, [points], True, color, 2, cv2.LINE_AA)
        
        return bg

    def get_image_for_quiz(self, keywords):
        """이미지 검색 및 대체 이미지 생성"""
        try:
            service = build("customsearch", "v1", developerKey=self.GOOGLE_API_KEY)
            
            enhanced_query = f"{keywords} high quality photo"
            result = service.cse().list(
                q=enhanced_query,
                cx=self.GOOGLE_SEARCH_ENGINE_ID,
                searchType='image',
                num=1,
                imgType='photo',
                safe='active'
            ).execute()
            
            if 'items' in result:
                image_url = result['items'][0]['link']
                print(f"Found image for keywords: {keywords}")
                
                image_data = requests.get(image_url).content
                image_array = np.asarray(bytearray(image_data), dtype=np.uint8)
                image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                
                if image is not None:
                    return cv2.resize(image, (800, 400))
                    
            print(f"Creating visual placeholder for: {keywords}")
            return self._create_fallback_image(keywords)
                
        except Exception as e:
            print(f"Error in get_image_for_quiz: {e}")
            return self._create_fallback_image(keywords)

    def _create_fallback_image(self, query, width=800, height=400):
        """시각적으로 더 매력적인 대체 이미지 생성"""
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        # 그라데이션 배경 생성
        for y in range(height):
            progress = y / height
            color = self._interpolate_color(
                self.current_scheme["colors"]["primary"],
                self.current_scheme["colors"]["secondary"],
                progress
            )
            image[y, :] = color
        
        # 장식적 요소 추가
        # 1. 반투명 오버레이 패턴
        pattern = np.zeros((height, width, 3), dtype=np.uint8)
        for i in range(0, width, 50):
            for j in range(0, height, 50):
                cv2.circle(pattern, (i, j), 20, self.current_scheme["colors"]["accent"], 1)
        image = cv2.addWeighted(image, 0.9, pattern, 0.1, 0)
        
        # 2. 중앙에 큰 아이콘 또는 심볼
        icon_size = min(width, height) // 3
        center_x = width // 2
        center_y = height // 2
        
        # 주제에 따른 간단한 아이콘 그리기
        keywords = query.lower()
        if any(word in keywords for word in ['food', 'dish', 'cuisine', 'meal']):
            # 음식 관련 - 접시 모양
            cv2.circle(image, (center_x, center_y), icon_size, (255, 255, 255), 2)
            cv2.circle(image, (center_x, center_y), icon_size-10, (255, 255, 255), 1)
        elif any(word in keywords for word in ['sport', 'game', 'play']):
            # 스포츠 관련 - 공 모양
            cv2.circle(image, (center_x, center_y), icon_size, (255, 255, 255), -1)
            cv2.circle(image, (center_x, center_y), icon_size, (200, 200, 200), 2)
        elif any(word in keywords for word in ['science', 'tech', 'technology']):
            # 과학/기술 관련 - 육각형 패턴
            for i in range(3):
                pts = np.array([
                    [center_x + int(icon_size * np.cos(angle + i * np.pi/3)) for angle in np.linspace(0, 2*np.pi, 7)],
                    [center_y + int(icon_size * np.sin(angle + i * np.pi/3)) for angle in np.linspace(0, 2*np.pi, 7)]
                ], np.int32).T
                cv2.polylines(image, [pts], True, (255, 255, 255), 2)
        else:
            # 기본 장식 - 동심원
            for r in range(0, icon_size, 20):
                cv2.circle(image, (center_x, center_y), r, (255, 255, 255), 1)
        
        # 3. 테두리 추가
        cv2.rectangle(image, (10, 10), (width-10, height-10), 
                    self.current_scheme["colors"]["accent"], 2)
        
        # 4. 부드러운 효과를 위한 블러
        image = cv2.GaussianBlur(image, (5, 5), 0)
        
        return image

    def create_modern_question_card(self, question_text, number, image=None, scale_factor=1.0):
        padding = int(30 * scale_factor)
        width = 800
        font = cv2.FONT_HERSHEY_DUPLEX
        font_scale = 1.6
        
        # 이미지 영역
        img_height = 350
        img_width = width - (padding * 2)
        
        if image is not None:
            resized_image = cv2.resize(image, (img_width, img_height))
        else:
            resized_image = self._create_fallback_image(img_width, img_height)
        
        # 텍스트 영역 설정
        line_height = int(45 * scale_factor)
        text_start_x = int(150 * scale_factor)
        max_text_width = width - text_start_x - padding
        
        # 텍스트 줄바꿈 처리
        words = question_text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            size = cv2.getTextSize(test_line, font, font_scale, 2)[0]
            if size[0] > max_text_width and current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                current_line.append(word)
        if current_line:
            lines.append(' '.join(current_line))
        
        # 텍스트 영역 높이 계산 (모든 값을 정수로 변환)
        text_height = int((len(lines) * line_height) + (padding * 1.5))
        
        # 카드 전체 높이 계산 (정수로 변환)
        height = int(img_height + text_height + padding * 2)
        
        # 카드 생성
        card = np.zeros((height, width, 3), dtype=np.uint8)
        card.fill(255)
        
        # 이미지 삽입
        image_y = padding
        card[image_y:image_y+img_height, padding:width-padding] = resized_image
        
        # 번호 배지
        circle_y = img_height + padding + text_height//3
        circle_x = int(70 * scale_factor)
        cv2.circle(card, 
                (circle_x, circle_y), 
                45,
                self.current_scheme["colors"]["primary"], 
                -1, 
                cv2.LINE_AA)
        
        cv2.putText(card, str(number),
                (circle_x-20, circle_y+15),
                font, 2.0,
                self.current_scheme["colors"]["text_light"], 
                2, 
                cv2.LINE_AA)
        
        # 질문 텍스트
        text_y = img_height + padding
        for line in lines:
            text_y += line_height
            cv2.putText(card, line,
                    (text_start_x, text_y),
                    font, font_scale,
                    self.current_scheme["colors"]["text_dark"], 
                    2, 
                    cv2.LINE_AA)
        
        return card

    def create_modern_button(self, letter, text, selected=False, scale_factor=1.0, dimmed=False):
        width = int(800 * scale_factor)
        height = int(80 * scale_factor)
        padding = int(25 * scale_factor)
        right_padding = 10
        margin = int(30 * scale_factor)
        
        # 버튼 생성
        total_height = height + (margin * 2)
        button = np.zeros((total_height, width, 3), dtype=np.uint8)
        button.fill(255)
        
        # 버튼 영역
        btn_top = margin
        btn_bottom = margin + height
        
        # 버튼 배경 색상
        if dimmed:
            color = tuple(map(lambda x: int(x * 0.7), self.current_scheme["colors"]["button"]))
        else:
            color = self.current_scheme["colors"]["primary"] if selected else self.current_scheme["colors"]["button"]
        
        # 버튼 배경 그리기
        cv2.rectangle(button,
                    (padding, btn_top),
                    (width - right_padding, btn_bottom),
                    color, -1, cv2.LINE_AA)
        
        # 레터 원형
        circle_radius = int(30 * scale_factor)
        circle_center = (padding + circle_radius + 10, margin + height//2)
        circle_color = (255, 255, 255) if selected else self.current_scheme["colors"]["primary"]
        
        if dimmed:
            circle_color = tuple(map(lambda x: int(x * 0.7), circle_color))
        
        cv2.circle(button, circle_center, circle_radius,
                circle_color, -1, cv2.LINE_AA)
        
        # 폰트 설정
        font = cv2.FONT_HERSHEY_DUPLEX
        base_font_scale = 1.4
        font_scale = base_font_scale * scale_factor
        
        # 레터 텍스트 색상
        if dimmed:
            letter_color = (180, 180, 180)
        else:
            letter_color = self.current_scheme["colors"]["primary"] if selected else (255, 255, 255)
        
        # 레터 텍스트 그리기
        letter_x = circle_center[0] - int(15 * scale_factor)
        letter_y = circle_center[1] + int(12 * scale_factor)
        cv2.putText(button, letter,
                (letter_x, letter_y),
                font, font_scale,
                letter_color, 2, cv2.LINE_AA)
        
        # 답안 텍스트 공간 계산
        text_x = padding + circle_radius * 2 + 30
        available_width = width - text_x - right_padding - 10
        
        # 텍스트 크기 계산 및 조정
        text_size = cv2.getTextSize(text, font, font_scale, 2)[0]
        if text_size[0] > available_width:
            font_scale *= (available_width / float(text_size[0]))
            text_size = cv2.getTextSize(text, font, font_scale, 2)[0]
        
        # 답안 텍스트 색상 설정
        if dimmed:
            text_color = (150, 150, 150)
        else:
            text_color = (255, 255, 255) if selected else (33, 33, 33)  # 선택됐을 때는 흰색으로
        
        # 텍스트 위치 계산 (수직 중앙 정렬)
        text_y = btn_top + (height + text_size[1]) // 2
        
        # 답안 텍스트 그리기 (선명하게)
        cv2.putText(button, text,
                (text_x, text_y),
                font, font_scale,
                text_color, 2, cv2.LINE_AA)
        
        return button
            
class QuizVideoGenerator:
    def __init__(self, output_path="output"):
        self.output_path = output_path
        self.width = 1080
        self.height = 1920
        self.fps = 30
        
        self.title_font = "Arial-Bold"
        self.text_font = "Arial"
        
        # UI 요소 초기화
        self.ui = QuizUIElements(self.width, self.height)

    def create_intro(self, category="Quiz Game"):
        duration = 5
        clips = []
        
        # 배경
        bg = self.create_animated_background(duration)
        clips.append(bg)
        
        # 타이틀 텍스트
        title = TextClip(
            category,
            fontsize=100,
            color='white',
            font=self.title_font,
            size=(self.width-200, None)
        ).set_position('center').set_duration(duration)
        clips.append(title)
        
        return CompositeVideoClip(clips, size=(self.width, self.height))

    def create_animated_background(self, duration):
        """배경 생성"""
        def make_frame(t):
            frame_number = int(t * self.fps)
            return self.ui.create_geometric_background(frame_number)
        return VideoClip(make_frame, duration=duration)

    def create_quiz_section(self, quiz_data, question_number):
        duration = 15
        clips = []
        
        # 배경
        bg = self.create_animated_background(duration)
        clips.append(bg)
        
        # 이미지 가져오기
        image = self.ui.get_image_for_quiz(quiz_data["image_keywords"])
        
        # 위치 및 여백 계산
        question_y = 150
        first_button_y = 900
        button_spacing = 180
        
        # 질문 카드
        question_position = ('center', question_y)
        question_card = ImageClip(
            self.ui.create_modern_question_card(
                question_text=quiz_data["question"],
                number=question_number,
                image=image
            )
        ).set_position(question_position).set_duration(duration)
        clips.append(question_card)
        
        # 답안 버튼들 생성
        options = [quiz_data["correct_answer"]] + quiz_data["wrong_answers"]
        random.shuffle(options)
        correct_index = options.index(quiz_data["correct_answer"])
        
        # 각 버튼 생성 및 배치
        for i, option in enumerate(options):
            button_y = first_button_y + (i * button_spacing)
            
            if option == quiz_data["correct_answer"]:
                # 정답 버튼
                # 1. 일반 상태
                normal_button = ImageClip(
                    self.ui.create_modern_button(chr(65+i), option)
                ).set_position(('center', button_y))
                normal_button = normal_button.set_start(0).set_duration(duration - 3)
                clips.append(normal_button)
                
                # 2. 정답 효과 (텍스트 포함)
                for j in range(3):
                    highlight_button = ImageClip(
                        self.ui.create_modern_button(
                            chr(65+i), 
                            option, 
                            selected=True,
                            scale_factor=1.2
                        )
                    ).set_position(('center', button_y))
                    
                    start_time = duration - 3 + j
                    highlight_button = highlight_button.set_start(start_time).set_duration(0.7)
                    clips.append(highlight_button)
                    
                    if j < 2:
                        normal_button = ImageClip(
                            self.ui.create_modern_button(
                                chr(65+i), 
                                option, 
                                selected=True
                            )
                        ).set_position(('center', button_y))
                        normal_button = normal_button.set_start(start_time + 0.7).set_duration(0.3)
                        clips.append(normal_button)
            else:
                # 오답 버튼
                # 1. 일반 상태
                normal_button = ImageClip(
                    self.ui.create_modern_button(chr(65+i), option)
                ).set_position(('center', button_y))
                normal_button = normal_button.set_start(0).set_duration(duration - 3)
                clips.append(normal_button)
                
                # 2. 흐린 상태 (버튼과 텍스트 모두 흐리게)
                dim_button = ImageClip(
                    self.ui.create_modern_button(
                        chr(65+i), 
                        option, 
                        dimmed=True
                    )
                ).set_position(('center', button_y))
                dim_button = dim_button.set_start(duration - 3).set_duration(3)
                clips.append(dim_button)
        
        return CompositeVideoClip(clips, size=(self.width, self.height))

    def create_outro(self, score):
        """아웃트로 생성"""
        duration = 5
        clips = []
        
        bg = self.create_animated_background(duration)
        clips.append(bg)
        
        score_text = TextClip(
            f"Final Score: {score}%",
            fontsize=80,
            color='white',
            font=self.title_font,
            size=(self.width, 200)
        ).set_position('center').set_duration(duration)
        clips.append(score_text)
        
        end_message = TextClip(
            "Thanks for playing!",
            fontsize=60,
            color='white',
            font=self.text_font,
            size=(self.width, 200)
        ).set_position(('center', self.height//2 + 100))
        end_message = end_message.set_duration(duration-1).set_start(1)
        clips.append(end_message)
        
        return CompositeVideoClip(clips, size=(self.width, self.height))

    def create_video(self, quiz_data_list, category="Quiz Game"):
        try:
            if not quiz_data_list:
                print("No quiz data provided")
                return None
                
            # quiz_data_list 저장
            self.quiz_data_list = quiz_data_list  # 여기에 저장
                
            clips = []
            
            # 인트로
            print("Creating intro...")
            intro = self.create_intro(category)
            clips.append(intro)
            
            # 퀴즈 섹션
            for i, quiz_data in enumerate(quiz_data_list, 1):
                print(f"Creating section for question {i}")
                section = self.create_quiz_section(quiz_data, i)
                if section:
                    clips.append(section)
            
            # 아웃트로
            print("Creating outro...")
            outro = self.create_outro(100)
            clips.append(outro)
            
            print(f"Concatenating {len(clips)} clips...")
            final_video = concatenate_videoclips(clips)
            
            # 1. 기존 파일명으로 저장
            original_output = os.path.join(self.output_path, "quiz_video.mp4")
            print(f"Writing original video to: {original_output}")
            final_video.write_videofile(
                original_output,
                fps=self.fps,
                codec='libx264',
                audio=False,
                threads=4
            )
            
            # 2. 날짜별 폴더에 복사본 저장
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            date_folder = os.path.join(self.output_path, "date")
            os.makedirs(date_folder, exist_ok=True)
            
            dated_output = os.path.join(date_folder, f"quiz_video_{timestamp}.mp4")
            print(f"Copying to dated archive: {dated_output}")
            import shutil
            shutil.copy2(original_output, dated_output)
            
            return original_output
        except Exception as e:
            print(f"Error creating video: {str(e)}")
            traceback.print_exc()
            return None

    # QuizVideoGenerator 클래스에서
    def add_background_music(self, video_path, quiz_data_list):
        try:
            from datetime import datetime
            video = VideoFileClip(video_path)
            
            # TTS 클립 생성
            tts_clips = []
            intro_duration = 5  # 인트로 길이
            question_duration = 15  # 각 질문 섹션 길이
            
            # 각 질문에 대한 TTS 생성 및 타이밍 설정
            for i, quiz_data in enumerate(quiz_data_list):
                # TTS 생성
                tts_audio = self.generate_tts(quiz_data["question"])
                if tts_audio:
                    print(f"Adding TTS for question {i+1}")
                    tts_clip = AudioFileClip(tts_audio)
                    
                    # 시작 시간 계산 (인트로 이후 각 섹션의 시작 부분)
                    start_time = intro_duration + (i * question_duration) + 1  # 1초 딜레이
                    
                    # TTS 볼륨 및 타이밍 설정
                    tts_clip = tts_clip.set_start(start_time).volumex(1.2)  # 볼륨 약간 증가
                    tts_clips.append(tts_clip)
            
            # 배경 음악
            music_path = os.path.join("assets", "audio", "christmas-spirit-265741.mp3")
            print(f"Loading audio from: {music_path}")
            background_music = AudioFileClip(music_path)
            
            if background_music.duration < video.duration:
                background_music = background_music.loop(duration=video.duration)
            else:
                background_music = background_music.subclip(0, video.duration)
            
            # 배경음악 볼륨을 더 낮게 설정
            background_music = background_music.volumex(0.1)
            
            # 음성과 배경음악 합성
            print("Combining audio tracks...")
            final_audio = CompositeAudioClip([background_music] + tts_clips)
            final_video = video.set_audio(final_audio)
            
            # 파일 저장
            original_output = os.path.join(self.output_path, "quiz_video_with_audio.mp4")
            print(f"Saving video with audio to: {original_output}")
            final_video.write_videofile(
                original_output,
                fps=self.fps,
                codec='libx264',
                audio_codec='aac',
                threads=4
            )
            
            # 날짜별 저장
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            date_folder = os.path.join(self.output_path, "date")
            dated_output = os.path.join(date_folder, f"quiz_video_{timestamp}_with_audio.mp4")
            print(f"Copying to dated archive: {dated_output}")
            shutil.copy2(original_output, dated_output)
            
            # 리소스 정리
            video.close()
            background_music.close()
            for clip in tts_clips:
                clip.close()
                
            # 임시 TTS 파일들 정리
            for clip in tts_clips:
                try:
                    os.remove(clip.filename)
                except:
                    pass
            
            return original_output
                
        except Exception as e:
            print(f"Error adding audio: {e}")
            traceback.print_exc()
            return None

    def generate_tts(self, text):
        """Google TTS를 사용한 음성 생성"""
        try:
            from gtts import gTTS
            import tempfile
            
            # 임시 파일 생성
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                # 영어로 TTS 생성 (속도는 slow=False로 설정)
                tts = gTTS(text=text, lang='en', slow=False)
                tts.save(temp_file.name)
                return temp_file.name
                
        except Exception as e:
            print(f"Error generating TTS: {e}")
            return None