import random

QUIZ_TOPICS = {
    "animals": "Animals",
    "science": "Science",
    "history": "History",
    "culture": "Culture",
    "geography": "Geography",
    "space": "Space",
    "technology": "Technology",
    "nature": "Nature",
    "famous_people": "Famous People",
    "inventions": "Inventions",
    "art": "Art",
    "food": "Food",
    "sports": "Sports",
    "music": "Music",
    "literature": "Literature",
    "ancient_civilizations": "Ancient Civilizations"
}

def get_random_topic():
    """랜덤한 퀴즈 주제 선택"""
    topic, topic_name = random.choice(list(QUIZ_TOPICS.items()))
    return {
        "id": topic,
        "name": topic_name,
        "prompt": f"Create interesting and educational quiz questions about {topic_name}. "
                 f"Questions should be diverse and not too similar to each other. "
                 f"Include surprising and engaging fun facts that viewers might not know."
    }