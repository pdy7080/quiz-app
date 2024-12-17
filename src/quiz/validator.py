# src/quiz/validator.py
class QuizValidator:
    @staticmethod
    def validate_quiz_data(quiz_data):
        """퀴즈 데이터 검증"""
        required_fields = ['question', 'answer', 'fun_fact']
        
        if not all(field in quiz_data for field in required_fields):
            raise ValueError("Missing required fields in quiz data")
            
        if len(quiz_data['question']) > 100:
            raise ValueError("Question too long")
            
        if len(quiz_data['answer']) > 50:
            raise ValueError("Answer too long")
            
        if len(quiz_data['fun_fact']) > 150:
            raise ValueError("Fun fact too long")
            
        return True