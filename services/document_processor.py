import os
import asyncio
from pathlib import Path
from typing import Optional
import aiofiles
import PyPDF2
from docx import Document

class DocumentProcessor:
    """Classe pour traiter différents types de documents"""
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.docx', '.txt', '.md']
    
    async def extract_text(self, file_path: str) -> str:
        """Extraire le texte d'un fichier selon son format"""
        file_extension = Path(file_path).suffix.lower()
        
        if file_extension == '.pdf':
            return await self._extract_from_pdf(file_path)
        elif file_extension == '.docx':
            return await self._extract_from_docx(file_path)
        elif file_extension in ['.txt', '.md']:
            return await self._extract_from_text(file_path)
        else:
            raise ValueError(f"Format de fichier non supporté: {file_extension}")
    
    async def _extract_from_pdf(self, file_path: str) -> str:
        """Extraire le texte d'un fichier PDF"""
        def extract_pdf_sync():
            text = ""
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                return text
            except Exception as e:
                raise Exception(f"Erreur lors de la lecture du PDF: {str(e)}")
        
        # Exécuter dans un thread séparé pour éviter de bloquer
        return await asyncio.get_event_loop().run_in_executor(None, extract_pdf_sync)
    
    async def _extract_from_docx(self, file_path: str) -> str:
        """Extraire le texte d'un fichier Word"""
        def extract_docx_sync():
            try:
                doc = Document(file_path)
                text = ""
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
                return text
            except Exception as e:
                raise Exception(f"Erreur lors de la lecture du fichier Word: {str(e)}")
        
        return await asyncio.get_event_loop().run_in_executor(None, extract_docx_sync)
    
    async def _extract_from_text(self, file_path: str) -> str:
        """Extraire le texte d'un fichier texte"""
        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
                return await file.read()
        except UnicodeDecodeError:
            # Essayer avec un encodage différent
            async with aiofiles.open(file_path, 'r', encoding='latin-1') as file:
                return await file.read()
        except Exception as e:
            raise Exception(f"Erreur lors de la lecture du fichier texte: {str(e)}")
    
    def get_file_info(self, file_path: str) -> dict:
        """Obtenir des informations sur le fichier"""
        path = Path(file_path)
        return {
            "name": path.name,
            "extension": path.suffix,
            "size": path.stat().st_size if path.exists() else 0,
            "supported": path.suffix.lower() in self.supported_formats
        }
    
    async def clean_text(self, text: str) -> str:
        """Nettoyer et formater le texte extrait"""
        # Supprimer les lignes vides multiples
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line:  # Garder seulement les lignes non vides
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)