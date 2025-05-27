from app.models.models import db, Notification, User
from flask import current_app
from app.utils.email import send_email
from threading import Thread

def create_notification(user_id, message, notification_type):
    """Create a new notification for a user"""
    notification = Notification(
        user_id=user_id,
        message=message,
        type=notification_type
    )
    db.session.add(notification)
    db.session.commit()
    return notification

def send_absence_notification_complete(etudiant, absence):
    """Send complete notification (in-app + email) for new absence"""
    # Create in-app notification
    create_notification(
        user_id=etudiant.user_id,
        message=f"Une absence a été enregistrée pour le module {absence.module.nom} du {absence.date.strftime('%d/%m/%Y')}",
        notification_type='nouvelle_absence'
    )
    
    # Send email notification
    from app.utils.email import send_absence_notification
    send_absence_notification(etudiant, absence)

def send_justification_notification_complete(absence, accepted, raison=None):
    """Send complete notification (in-app + email) for justification response"""
    etudiant = absence.etudiant
    
    if accepted:
        message = f"Votre justificatif pour l'absence du {absence.date.strftime('%d/%m/%Y')} a été accepté"
        notification_type = 'justificatif_valide'
    else:
        message = f"Votre justificatif pour l'absence du {absence.date.strftime('%d/%m/%Y')} a été refusé"
        if raison:
            message += f". Raison: {raison}"
        notification_type = 'justificatif_refuse'
    
    # Create in-app notification
    create_notification(
        user_id=etudiant.user_id,
        message=message,
        notification_type=notification_type
    )
    
    # Send email notification
    from app.utils.email import send_justification_notification
    send_justification_notification(absence, accepted)

def send_reminder_notifications(etudiants_absences):
    """Send reminder notifications for unjustified absences"""
    for etudiant, absences in etudiants_absences.items():
        # Create in-app notification
        create_notification(
            user_id=etudiant.user_id,
            message=f"Vous avez {len(absences)} absence(s) non justifiée(s). Veuillez soumettre vos justificatifs.",
            notification_type='rappel'
        )
        
        # Send email notification
        from app.utils.email import send_reminder_notification
        send_reminder_notification(etudiant, absences)

def notify_responsables_new_justification(absence):
    """Notify all responsables when a new justification is submitted"""
    responsables = User.query.filter_by(role='responsable').all()
    
    for responsable in responsables:
        create_notification(
            user_id=responsable.id,
            message=f"Nouveau justificatif soumis par {absence.etudiant.prenom} {absence.etudiant.nom} pour le {absence.date.strftime('%d/%m/%Y')}",
            notification_type='nouveau_justificatif'
        )

def get_unread_notifications_count(user_id):
    """Get count of unread notifications for a user"""
    return Notification.query.filter_by(user_id=user_id, lue=False).count()

def mark_notification_as_read(notification_id, user_id):
    """Mark a specific notification as read"""
    notification = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
    if notification:
        notification.lue = True
        db.session.commit()
        return True
    return False

def mark_all_notifications_as_read(user_id):
    """Mark all notifications as read for a user"""
    Notification.query.filter_by(user_id=user_id, lue=False).update({'lue': True})
    db.session.commit()
