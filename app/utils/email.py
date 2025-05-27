from flask import render_template, current_app
from flask_mail import Message
from app import mail
from threading import Thread
import logging

def send_async_email(app, msg):
    """Send email asynchronously"""
    with app.app_context():
        try:
            mail.send(msg)
            logging.info(f"Email sent successfully to {msg.recipients}")
        except Exception as e:
            logging.error(f"Failed to send email: {str(e)}")

def send_email(subject, sender, recipients, text_body, html_body):
    """Send email with both text and HTML versions"""
    try:
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = text_body
        msg.html = html_body
        
        # Send email asynchronously
        Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
        return True
    except Exception as e:
        logging.error(f"Error creating email: {str(e)}")
        return False

def send_absence_notification(etudiant, absence):
    """Send notification email for new absence"""
    user = etudiant.user
    module = absence.module
    
    if not current_app.config.get('MAIL_DEFAULT_SENDER'):
        logging.warning("No default sender configured for emails")
        return False
    
    return send_email(
        subject='Nouvelle absence enregistrée',
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[user.email],
        text_body=render_template('email/absence_notification.txt',
                                 user=user,
                                 absence=absence,
                                 module=module),
        html_body=render_template('email/absence_notification.html',
                                 user=user,
                                 absence=absence,
                                 module=module)
    )

def send_justification_notification(absence, accepted):
    """Send notification email for justification response"""
    etudiant = absence.etudiant
    user = etudiant.user
    module = absence.module
    
    if not current_app.config.get('MAIL_DEFAULT_SENDER'):
        logging.warning("No default sender configured for emails")
        return False
    
    if accepted:
        subject = 'Justificatif accepté'
        template = 'justification_accepted'
    else:
        subject = 'Justificatif refusé'
        template = 'justification_rejected'
    
    return send_email(
        subject=subject,
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[user.email],
        text_body=render_template(f'email/{template}.txt',
                                 user=user,
                                 absence=absence,
                                 module=module),
        html_body=render_template(f'email/{template}.html',
                                 user=user,
                                 absence=absence,
                                 module=module)
    )

def send_reminder_notification(etudiant, absences):
    """Send reminder email for unjustified absences"""
    user = etudiant.user
    
    if not current_app.config.get('MAIL_DEFAULT_SENDER'):
        logging.warning("No default sender configured for emails")
        return False
    
    return send_email(
        subject='Rappel: Absences non justifiées',
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[user.email],
        text_body=render_template('email/reminder.txt',
                                 user=user,
                                 absences=absences),
        html_body=render_template('email/reminder.html',
                                 user=user,
                                 absences=absences)
    )

def send_welcome_email(user, password):
    """Send welcome email to new user"""
    if not current_app.config.get('MAIL_DEFAULT_SENDER'):
        logging.warning("No default sender configured for emails")
        return False
    
    return send_email(
        subject='Bienvenue dans le système de gestion des absences',
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[user.email],
        text_body=render_template('email/welcome.txt',
                                 user=user,
                                 password=password),
        html_body=render_template('email/welcome.html',
                                 user=user,
                                 password=password)
    )

def test_email_configuration():
    """Test email configuration"""
    try:
        with mail.connect() as conn:
            logging.info("Email configuration test successful")
            return True
    except Exception as e:
        logging.error(f"Email configuration test failed: {str(e)}")
        return False
