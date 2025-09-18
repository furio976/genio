import openai
import random
from datetime import datetime
from config import Config

class ContentGenerator:
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        
    def generate_daily_topic(self):
        """Generate a topic for today's video"""
        topics_prompts = {
            'general': [
                "un fait intéressant sur la nature",
                "une découverte scientifique récente",
                "un conseil de vie quotidienne",
                "une histoire inspirante",
                "un phénomène naturel fascinant"
            ],
            'tech': [
                "une innovation technologique récente",
                "l'impact de l'IA sur notre quotidien",
                "une tendance tech émergente",
                "un gadget révolutionnaire",
                "l'évolution des réseaux sociaux"
            ],
            'education': [
                "une leçon d'histoire méconnue",
                "un concept scientifique expliqué simplement",
                "une langue étrangère intéressante",
                "une compétence utile à apprendre",
                "un livre qui change la vie"
            ],
            'entertainment': [
                "un film culte à redécouvrir",
                "une série tendance à regarder",
                "un jeu vidéo innovant",
                "un artiste émergent à suivre",
                "une tendance culturelle actuelle"
            ]
        }
        
        category = Config.VIDEO_TOPIC_CATEGORY
        if category not in topics_prompts:
            category = 'general'
            
        topic_prompt = random.choice(topics_prompts[category])
        return topic_prompt
    
    def generate_script(self, topic):
        """Generate a video script based on the topic"""
        prompt = f"""
        Crée un script pour une vidéo YouTube de {Config.VIDEO_DURATION} secondes sur le sujet suivant: {topic}.
        
        Le script doit être:
        - Engageant et captivant dès les premières secondes
        - Informatif et éducatif
        - Adapté à un public francophone
        - Structuré avec une introduction, un développement et une conclusion
        - Écrit dans un style conversationnel et accessible
        - D'environ 150-200 mots pour une durée de {Config.VIDEO_DURATION} secondes
        
        Format de réponse:
        TITRE: [Titre accrocheur de la vidéo]
        
        SCRIPT:
        [Le script complet avec des indications de timing si nécessaire]
        
        MOTS-CLÉS: [5-7 mots-clés pertinents séparés par des virgules]
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Tu es un créateur de contenu expert spécialisé dans la création de scripts vidéo engageants et informatifs."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Erreur lors de la génération du script: {e}")
            return self._get_fallback_script(topic)
    
    def _get_fallback_script(self, topic):
        """Fallback script in case of API failure"""
        today = datetime.now().strftime('%d %B %Y')
        return f"""
        TITRE: Découverte du jour - {topic}
        
        SCRIPT:
        Salut à tous ! Aujourd'hui, le {today}, nous allons explorer {topic}.
        
        C'est un sujet fascinant qui mérite notre attention. Dans cette courte vidéo, 
        nous allons découvrir ensemble les aspects les plus intéressants de ce sujet.
        
        Cette information pourrait changer votre perspective et enrichir vos connaissances.
        N'hésitez pas à partager cette vidéo si elle vous a plu !
        
        À bientôt pour une nouvelle découverte !
        
        MOTS-CLÉS: découverte, apprentissage, culture, éducation, français
        """
    
    def parse_script_content(self, script_content):
        """Parse the generated script to extract title, script, and keywords"""
        lines = script_content.strip().split('\n')
        
        title = ""
        script = ""
        keywords = ""
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('TITRE:'):
                title = line.replace('TITRE:', '').strip()
                current_section = 'title'
            elif line.startswith('SCRIPT:'):
                current_section = 'script'
                continue
            elif line.startswith('MOTS-CLÉS:'):
                keywords = line.replace('MOTS-CLÉS:', '').strip()
                current_section = 'keywords'
            elif current_section == 'script' and line:
                script += line + ' '
        
        return {
            'title': title or f"Vidéo du jour - {datetime.now().strftime('%d/%m/%Y')}",
            'script': script.strip() or "Contenu généré automatiquement pour aujourd'hui.",
            'keywords': keywords or "vidéo, quotidien, contenu"
        }
    
    def generate_daily_content(self):
        """Generate complete content for today's video"""
        print("Génération du contenu quotidien...")
        
        # Generate topic
        topic = self.generate_daily_topic()
        print(f"Sujet généré: {topic}")
        
        # Generate script
        script_content = self.generate_script(topic)
        parsed_content = self.parse_script_content(script_content)
        
        print(f"Titre: {parsed_content['title']}")
        print(f"Script généré ({len(parsed_content['script'])} caractères)")
        
        return parsed_content