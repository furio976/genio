from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    OPEN_ENDED = "open_ended"
    FILL_IN_BLANK = "fill_in_blank"

class StudySession(BaseModel):
    id: str
    filename: str
    content: str
    created_at: datetime
    metadata: Optional[Dict[str, Any]] = {}

class Question(BaseModel):
    id: Optional[str] = None
    question: str
    type: QuestionType
    options: Optional[List[str]] = None  # Pour les QCM
    correct_answer: str
    explanation: Optional[str] = None
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM

class Quiz(BaseModel):
    id: str
    title: str
    questions: List[Question]
    total_questions: int
    estimated_time: int  # en minutes

class Summary(BaseModel):
    content: str
    key_points: List[str]
    topics_covered: List[str]
    word_count: int

class Flashcard(BaseModel):
    front: str  # Question ou terme
    back: str   # Réponse ou définition
    category: Optional[str] = None
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM

class Explanation(BaseModel):
    concept: str
    explanation: str
    examples: List[str] = []
    related_concepts: List[str] = []

class StudyMaterial(BaseModel):
    session_id: str
    type: str  # summary, questions, quiz, flashcards, explanation
    content: Any
    created_at: datetime