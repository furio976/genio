import schedule
import time
import threading
from datetime import datetime, timedelta
from content_generator import ContentGenerator
from video_generator import VideoGenerator
from config import Config
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('video_ai.log'),
        logging.StreamHandler()
    ]
)

class VideoScheduler:
    def __init__(self):
        self.content_generator = ContentGenerator()
        self.video_generator = VideoGenerator()
        self.is_running = False
        self.scheduler_thread = None
        
    def generate_daily_video(self):
        """Generate today's video"""
        try:
            logging.info("Début de la génération vidéo quotidienne")
            
            # Validate configuration
            Config.validate_config()
            
            # Check if today's video already exists
            today_filename = Config.get_daily_filename()
            today_path = os.path.join(Config.OUTPUT_DIRECTORY, today_filename)
            
            if os.path.exists(today_path):
                logging.info(f"La vidéo d'aujourd'hui existe déjà: {today_path}")
                return today_path
            
            # Generate content
            content_data = self.content_generator.generate_daily_content()
            
            if not content_data:
                logging.error("Échec de la génération du contenu")
                return False
            
            # Create video
            video_path = self.video_generator.create_video(content_data)
            
            if video_path:
                # Get video info
                video_info = self.video_generator.get_video_info(video_path)
                
                logging.info(f"Vidéo générée avec succès!")
                logging.info(f"Titre: {content_data['title']}")
                logging.info(f"Chemin: {video_path}")
                
                if video_info:
                    logging.info(f"Durée: {video_info['duration']:.1f}s")
                    logging.info(f"Taille du fichier: {video_info['file_size'] / (1024*1024):.1f} MB")
                
                return video_path
            else:
                logging.error("Échec de la création de la vidéo")
                return False
                
        except Exception as e:
            logging.error(f"Erreur lors de la génération quotidienne: {e}")
            return False
    
    def setup_daily_schedule(self):
        """Setup the daily schedule for video generation"""
        schedule_time = Config.DAILY_SCHEDULE_TIME
        
        # Clear existing jobs
        schedule.clear()
        
        # Schedule daily video generation
        schedule.every().day.at(schedule_time).do(self.generate_daily_video)
        
        logging.info(f"Planification configurée pour {schedule_time} chaque jour")
    
    def run_scheduler(self):
        """Run the scheduler in a loop"""
        self.setup_daily_schedule()
        
        logging.info("Démarrage du planificateur...")
        logging.info(f"Prochaine exécution: {schedule.next_run()}")
        
        while self.is_running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def start(self):
        """Start the scheduler in a separate thread"""
        if self.is_running:
            logging.warning("Le planificateur est déjà en cours d'exécution")
            return
        
        self.is_running = True
        self.scheduler_thread = threading.Thread(target=self.run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        logging.info("Planificateur démarré en arrière-plan")
    
    def stop(self):
        """Stop the scheduler"""
        self.is_running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        
        logging.info("Planificateur arrêté")
    
    def generate_now(self):
        """Generate a video immediately"""
        logging.info("Génération immédiate demandée")
        return self.generate_daily_video()
    
    def get_schedule_info(self):
        """Get information about scheduled jobs"""
        jobs = schedule.get_jobs()
        info = {
            'scheduled_time': Config.DAILY_SCHEDULE_TIME,
            'next_run': schedule.next_run() if jobs else None,
            'is_running': self.is_running,
            'total_jobs': len(jobs)
        }
        return info
    
    def reschedule(self, new_time):
        """Reschedule the daily video generation"""
        try:
            # Validate time format
            datetime.strptime(new_time, '%H:%M')
            
            # Update config (this would need to be persisted to .env)
            Config.DAILY_SCHEDULE_TIME = new_time
            
            # Setup new schedule
            self.setup_daily_schedule()
            
            logging.info(f"Replanification réussie pour {new_time}")
            return True
            
        except ValueError:
            logging.error(f"Format d'heure invalide: {new_time}. Utilisez HH:MM")
            return False

class VideoSchedulerManager:
    """Manager class to handle the video scheduler with additional utilities"""
    
    def __init__(self):
        self.scheduler = VideoScheduler()
    
    def run_interactive(self):
        """Run the scheduler with interactive commands"""
        print("=== IA Génératrice de Vidéos Quotidiennes ===")
        print("Commandes disponibles:")
        print("  start    - Démarrer le planificateur")
        print("  stop     - Arrêter le planificateur")
        print("  now      - Générer une vidéo maintenant")
        print("  status   - Voir le statut du planificateur")
        print("  schedule - Replanifier l'heure quotidienne")
        print("  quit     - Quitter")
        print()
        
        try:
            while True:
                command = input("Commande: ").strip().lower()
                
                if command == 'start':
                    self.scheduler.start()
                    
                elif command == 'stop':
                    self.scheduler.stop()
                    
                elif command == 'now':
                    result = self.scheduler.generate_now()
                    if result:
                        print(f"Vidéo générée: {result}")
                    else:
                        print("Échec de la génération")
                        
                elif command == 'status':
                    info = self.scheduler.get_schedule_info()
                    print(f"Statut: {'En cours' if info['is_running'] else 'Arrêté'}")
                    print(f"Heure planifiée: {info['scheduled_time']}")
                    print(f"Prochaine exécution: {info['next_run']}")
                    
                elif command == 'schedule':
                    new_time = input("Nouvelle heure (HH:MM): ").strip()
                    if self.scheduler.reschedule(new_time):
                        print(f"Replanifié pour {new_time}")
                    else:
                        print("Échec de la replanification")
                        
                elif command in ['quit', 'exit', 'q']:
                    self.scheduler.stop()
                    print("Au revoir!")
                    break
                    
                else:
                    print("Commande inconnue")
                    
        except KeyboardInterrupt:
            self.scheduler.stop()
            print("\nArrêt du programme")

if __name__ == "__main__":
    import os
    
    manager = VideoSchedulerManager()
    manager.run_interactive()