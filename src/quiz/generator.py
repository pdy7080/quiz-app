import json
from anthropic import Anthropic
import re

class QuizGenerator:
    def __init__(self, api_key):
        self.client = Anthropic(api_key=api_key)

    def generate_quiz(self, topic, count=5, prompt=None):
        try:
            prompt = f"""Create {count} quiz questions about {topic}.
            IMPORTANT: Return only a JSON array, no additional text or explanations.
            
            Format each question exactly like this example:
            [
                {{
                    "question": "What is this unique sport feature shown in the image?",
                    "correct_answer": "Answer",
                    "wrong_answers": ["Wrong1", "Wrong2", "Wrong3"],
                    "fun_fact": "Interesting fact about this answer",
                    "image_keywords": "specific descriptive keywords for image search"
                }}
            ]
            
            Each question should be visual and interesting.
            Include specific image_keywords that will help find a relevant image.
            Ensure all answers are clear and concise."""

            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=2000,
                temperature=0.7,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # JSON 배열 추출 시도
            content = str(response.content[0].text if isinstance(response.content, list) else response.content)
            print(f"Response content: {content}")

            # JSON 배열 찾기
            json_match = re.search(r'\[\s*{.*?}\s*\]', content, re.DOTALL)
            if json_match:
                try:
                    quiz_data = json.loads(json_match.group())
                    if self._validate_quiz_data(quiz_data):
                        print(f"Generated valid quiz data: {quiz_data}")
                        return quiz_data[:count]
                except json.JSONDecodeError as e:
                    print(f"JSON parsing error: {str(e)}")
                    
            return self._get_fallback_quiz(count)

        except Exception as e:
            print(f"Error generating quiz: {str(e)}")
            return self._get_fallback_quiz(count)

    def _validate_quiz_data(self, quiz_data):
        """퀴즈 데이터 유효성 검사"""
        if not isinstance(quiz_data, list):
            return False
            
        try:
            for quiz in quiz_data:
                # 필수 필드 확인
                if not all(key in quiz for key in ["question", "correct_answer", "wrong_answers", "fun_fact"]):
                    return False
                    
                # wrong_answers 검증
                if not isinstance(quiz["wrong_answers"], list) or len(quiz["wrong_answers"]) != 3:
                    return False
                    
                # 텍스트 필드 검증
                if not all(isinstance(quiz[field], str) for field in ["question", "correct_answer", "fun_fact"]):
                    return False
                    
                # 오답 텍스트 검증
                if not all(isinstance(ans, str) for ans in quiz["wrong_answers"]):
                    return False
                    
            return True
            
        except Exception as e:
            print(f"Validation error: {str(e)}")
            return False

    def _get_fallback_quiz(self, count):
        fallback = [{
            "question": "Which sport is shown in this dynamic image?",
            "correct_answer": "Soccer",
            "wrong_answers": ["Basketball", "Tennis", "Golf"],
            "fun_fact": "Soccer is the most popular sport in the world with over 4 billion fans.",
            "image_keywords": "soccer football match stadium goal sport action"
        }]
        return fallback * min(count, 5)