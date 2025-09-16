import os
import json
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

from models.study_models import (
    Question, Quiz, Summary, Flashcard, Explanation, 
    QuestionType, DifficultyLevel
)

load_dotenv()

class AIStudyAssistant:
    """Assistant IA pour générer du contenu d'étude personnalisé"""
    
    def __init__(self):
        self.openai_client = None
        self._initialize_ai()
    
    def _initialize_ai(self):
        """Initialiser le client OpenAI"""
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            self.openai_client = OpenAI(api_key=api_key)
        else:
            print("⚠️ Clé API OpenAI non trouvée. Utilisation du mode démo.")
            self.openai_client = None
    
    async def generate_summary(self, content: str) -> Summary:
        """Générer un résumé du contenu"""
        if not self.openai_client:
            return self._generate_demo_summary(content)
        
        try:
            prompt = f"""
            Analysez le contenu suivant et créez un résumé structuré en français :

            CONTENU:
            {content[:4000]}  # Limiter pour éviter les tokens excessifs

            Veuillez fournir :
            1. Un résumé général (200-300 mots)
            2. Les points clés (5-8 points)
            3. Les sujets principaux couverts

            Répondez au format JSON avec les clés : summary, key_points, topics_covered
            """
            
            response = await self._call_openai(prompt)
            result = json.loads(response)
            
            return Summary(
                content=result.get('summary', ''),
                key_points=result.get('key_points', []),
                topics_covered=result.get('topics_covered', []),
                word_count=len(result.get('summary', '').split())
            )
            
        except Exception as e:
            print(f"Erreur lors de la génération du résumé: {e}")
            return self._generate_demo_summary(content)
    
    async def generate_questions(
        self, 
        content: str, 
        num_questions: int = 5,
        difficulty: str = "medium"
    ) -> List[Question]:
        """Générer des questions d'étude"""
        if not self.openai_client:
            return self._generate_demo_questions(content, num_questions)
        
        try:
            prompt = f"""
            Basé sur le contenu suivant, créez {num_questions} questions d'étude de niveau {difficulty} en français :

            CONTENU:
            {content[:4000]}

            Créez des questions variées (QCM, vrai/faux, questions ouvertes).
            Pour chaque question, fournissez :
            - La question
            - Le type (multiple_choice, true_false, open_ended)
            - Les options (si QCM)
            - La réponse correcte
            - Une explication

            Répondez au format JSON avec une liste de questions.
            """
            
            response = await self._call_openai(prompt)
            questions_data = json.loads(response)
            
            questions = []
            for i, q_data in enumerate(questions_data.get('questions', [])):
                question = Question(
                    id=f"q_{i+1}",
                    question=q_data.get('question', ''),
                    type=QuestionType(q_data.get('type', 'open_ended')),
                    options=q_data.get('options'),
                    correct_answer=q_data.get('correct_answer', ''),
                    explanation=q_data.get('explanation', ''),
                    difficulty=DifficultyLevel(difficulty)
                )
                questions.append(question)
            
            return questions
            
        except Exception as e:
            print(f"Erreur lors de la génération des questions: {e}")
            return self._generate_demo_questions(content, num_questions)
    
    async def generate_quiz(
        self, 
        content: str, 
        num_questions: int = 10,
        question_type: str = "mixed"
    ) -> Quiz:
        """Générer un quiz interactif"""
        questions = await self.generate_questions(content, num_questions)
        
        quiz = Quiz(
            id=f"quiz_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            title="Quiz sur le cours",
            questions=questions,
            total_questions=len(questions),
            estimated_time=len(questions) * 2  # 2 minutes par question
        )
        
        return quiz
    
    async def generate_flashcards(self, content: str, num_cards: int = 15) -> List[Flashcard]:
        """Générer des cartes mémoire"""
        if not self.openai_client:
            return self._generate_demo_flashcards(content, num_cards)
        
        try:
            prompt = f"""
            Créez {num_cards} cartes mémoire basées sur le contenu suivant :

            CONTENU:
            {content[:4000]}

            Chaque carte doit avoir :
            - Une face (terme, concept ou question courte)
            - Un dos (définition, explication ou réponse)
            - Une catégorie si applicable

            Répondez au format JSON avec une liste de cartes.
            """
            
            response = await self._call_openai(prompt)
            cards_data = json.loads(response)
            
            flashcards = []
            for card_data in cards_data.get('flashcards', []):
                flashcard = Flashcard(
                    front=card_data.get('front', ''),
                    back=card_data.get('back', ''),
                    category=card_data.get('category'),
                    difficulty=DifficultyLevel.MEDIUM
                )
                flashcards.append(flashcard)
            
            return flashcards
            
        except Exception as e:
            print(f"Erreur lors de la génération des cartes: {e}")
            return self._generate_demo_flashcards(content, num_cards)
    
    async def explain_concept(self, content: str, concept: str) -> Explanation:
        """Expliquer un concept spécifique"""
        if not self.openai_client:
            return self._generate_demo_explanation(concept)
        
        try:
            prompt = f"""
            Basé sur le contenu du cours suivant, expliquez le concept "{concept}" de manière détaillée :

            CONTENU:
            {content[:4000]}

            Fournissez :
            - Une explication claire et détaillée
            - Des exemples pratiques
            - Des concepts connexes

            Répondez au format JSON.
            """
            
            response = await self._call_openai(prompt)
            result = json.loads(response)
            
            return Explanation(
                concept=concept,
                explanation=result.get('explanation', ''),
                examples=result.get('examples', []),
                related_concepts=result.get('related_concepts', [])
            )
            
        except Exception as e:
            print(f"Erreur lors de l'explication: {e}")
            return self._generate_demo_explanation(concept)
    
    async def _call_openai(self, prompt: str) -> str:
        """Appeler l'API OpenAI"""
        def make_request():
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Vous êtes un assistant d'étude expert. Répondez toujours en français et au format JSON demandé."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            return response.choices[0].message.content
        
        return await asyncio.get_event_loop().run_in_executor(None, make_request)
    
    # Méthodes de démonstration (sans API)
    def _generate_demo_summary(self, content: str) -> Summary:
        """Générer un résumé de démonstration"""
        words = content.split()[:50]
        demo_summary = " ".join(words) + "..."
        
        return Summary(
            content=f"[MODE DÉMO] Résumé du contenu : {demo_summary}",
            key_points=[
                "Point clé 1 identifié dans le contenu",
                "Point clé 2 extrait du document",
                "Point clé 3 important à retenir"
            ],
            topics_covered=["Sujet principal", "Concept important", "Théorie abordée"],
            word_count=len(demo_summary.split())
        )
    
    def _generate_demo_questions(self, content: str, num_questions: int) -> List[Question]:
        """Générer des questions de démonstration"""
        questions = []
        for i in range(num_questions):
            question = Question(
                id=f"demo_q_{i+1}",
                question=f"[DÉMO] Question {i+1} basée sur le contenu du cours ?",
                type=QuestionType.MULTIPLE_CHOICE if i % 2 == 0 else QuestionType.OPEN_ENDED,
                options=["Option A", "Option B", "Option C", "Option D"] if i % 2 == 0 else None,
                correct_answer="Option A" if i % 2 == 0 else "Réponse ouverte attendue",
                explanation=f"Explication pour la question {i+1}",
                difficulty=DifficultyLevel.MEDIUM
            )
            questions.append(question)
        return questions
    
    def _generate_demo_flashcards(self, content: str, num_cards: int) -> List[Flashcard]:
        """Générer des cartes de démonstration"""
        flashcards = []
        for i in range(num_cards):
            flashcard = Flashcard(
                front=f"[DÉMO] Concept {i+1}",
                back=f"Définition ou explication du concept {i+1} basée sur le contenu",
                category="Général",
                difficulty=DifficultyLevel.MEDIUM
            )
            flashcards.append(flashcard)
        return flashcards
    
    def _generate_demo_explanation(self, concept: str) -> Explanation:
        """Générer une explication de démonstration"""
        return Explanation(
            concept=concept,
            explanation=f"[MODE DÉMO] Explication détaillée du concept '{concept}' basée sur le contenu du cours.",
            examples=[
                f"Exemple 1 illustrant {concept}",
                f"Exemple 2 pratique de {concept}"
            ],
            related_concepts=[
                "Concept connexe 1",
                "Concept connexe 2"
            ]
        )