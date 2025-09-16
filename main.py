from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import json
from pathlib import Path
from typing import List, Optional
import aiofiles
from datetime import datetime

from services.document_processor import DocumentProcessor
from services.ai_study_assistant import AIStudyAssistant
from models.study_models import StudySession, Question, Summary

app = FastAPI(title="IA d'Étude Personnalisée", version="1.0.0")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Créer les dossiers nécessaires
os.makedirs("uploads", exist_ok=True)
os.makedirs("static", exist_ok=True)
os.makedirs("sessions", exist_ok=True)

# Monter les fichiers statiques
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialiser les services
document_processor = DocumentProcessor()
ai_assistant = AIStudyAssistant()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Page d'accueil de l'application"""
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload et traitement d'un fichier de cours"""
    try:
        # Vérifier le type de fichier
        allowed_extensions = ['.pdf', '.docx', '.txt', '.md']
        file_extension = Path(file.filename).suffix.lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Type de fichier non supporté. Types acceptés: {', '.join(allowed_extensions)}"
            )
        
        # Sauvegarder le fichier
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = f"uploads/{filename}"
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Traiter le document
        extracted_text = await document_processor.extract_text(file_path)
        
        # Créer une session d'étude
        session_id = f"session_{timestamp}"
        study_session = StudySession(
            id=session_id,
            filename=file.filename,
            content=extracted_text,
            created_at=datetime.now()
        )
        
        # Sauvegarder la session
        session_path = f"sessions/{session_id}.json"
        async with aiofiles.open(session_path, 'w', encoding='utf-8') as f:
            await f.write(study_session.model_dump_json(indent=2))
        
        return {
            "session_id": session_id,
            "filename": file.filename,
            "content_length": len(extracted_text),
            "message": "Fichier traité avec succès!"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement: {str(e)}")

@app.get("/sessions")
async def get_sessions():
    """Récupérer toutes les sessions d'étude"""
    sessions = []
    sessions_dir = Path("sessions")
    
    if sessions_dir.exists():
        for session_file in sessions_dir.glob("*.json"):
            async with aiofiles.open(session_file, 'r', encoding='utf-8') as f:
                content = await f.read()
                session_data = json.loads(content)
                sessions.append({
                    "id": session_data["id"],
                    "filename": session_data["filename"],
                    "created_at": session_data["created_at"]
                })
    
    return {"sessions": sessions}

@app.post("/study/{session_id}/summary")
async def generate_summary(session_id: str):
    """Générer un résumé du cours"""
    try:
        session = await load_session(session_id)
        summary = await ai_assistant.generate_summary(session.content)
        
        return {
            "session_id": session_id,
            "summary": summary,
            "type": "summary"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération du résumé: {str(e)}")

@app.post("/study/{session_id}/questions")
async def generate_questions(
    session_id: str, 
    num_questions: int = Form(5),
    difficulty: str = Form("medium")
):
    """Générer des questions d'étude"""
    try:
        session = await load_session(session_id)
        questions = await ai_assistant.generate_questions(
            session.content, 
            num_questions=num_questions,
            difficulty=difficulty
        )
        
        return {
            "session_id": session_id,
            "questions": questions,
            "type": "questions"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération des questions: {str(e)}")

@app.post("/study/{session_id}/quiz")
async def generate_quiz(
    session_id: str,
    num_questions: int = Form(10),
    question_type: str = Form("mixed")  # multiple_choice, true_false, mixed
):
    """Générer un quiz interactif"""
    try:
        session = await load_session(session_id)
        quiz = await ai_assistant.generate_quiz(
            session.content,
            num_questions=num_questions,
            question_type=question_type
        )
        
        return {
            "session_id": session_id,
            "quiz": quiz,
            "type": "quiz"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération du quiz: {str(e)}")

@app.post("/study/{session_id}/explain")
async def explain_concept(session_id: str, concept: str = Form(...)):
    """Expliquer un concept spécifique du cours"""
    try:
        session = await load_session(session_id)
        explanation = await ai_assistant.explain_concept(session.content, concept)
        
        return {
            "session_id": session_id,
            "concept": concept,
            "explanation": explanation,
            "type": "explanation"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'explication: {str(e)}")

@app.post("/study/{session_id}/flashcards")
async def generate_flashcards(session_id: str, num_cards: int = Form(15)):
    """Générer des cartes mémoire"""
    try:
        session = await load_session(session_id)
        flashcards = await ai_assistant.generate_flashcards(session.content, num_cards)
        
        return {
            "session_id": session_id,
            "flashcards": flashcards,
            "type": "flashcards"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération des cartes: {str(e)}")

async def load_session(session_id: str) -> StudySession:
    """Charger une session d'étude"""
    session_path = f"sessions/{session_id}.json"
    
    if not os.path.exists(session_path):
        raise HTTPException(status_code=404, detail="Session non trouvée")
    
    async with aiofiles.open(session_path, 'r', encoding='utf-8') as f:
        content = await f.read()
        session_data = json.loads(content)
        return StudySession(**session_data)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)