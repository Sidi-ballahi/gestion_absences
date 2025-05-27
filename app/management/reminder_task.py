from app import create_app
from app.models.models import db, Etudiant, Absence
from app.utils.notifications import send_reminder_notifications
from datetime import datetime, timedelta
import logging

def send_weekly_reminders():
    """Send weekly reminders for unjustified absences"""
    app = create_app()
    
    with app.app_context():
        try:
            # Get all students with unjustified absences older than 3 days
            cutoff_date = datetime.now().date() - timedelta(days=3)
            
            # Query students with unjustified absences
            etudiants_with_absences = {}
            
            absences = Absence.query.filter(
                Absence.statut == 'non_justifiee',
                Absence.date <= cutoff_date
            ).all()
            
            for absence in absences:
                etudiant = absence.etudiant
                if etudiant not in etudiants_with_absences:
                    etudiants_with_absences[etudiant] = []
                etudiants_with_absences[etudiant].append(absence)
            
            if etudiants_with_absences:
                send_reminder_notifications(etudiants_with_absences)
                logging.info(f"Sent reminders to {len(etudiants_with_absences)} students")
            else:
                logging.info("No students with unjustified absences found")
                
        except Exception as e:
            logging.error(f"Error sending reminders: {str(e)}")

if __name__ == "__main__":
    send_weekly_reminders()
