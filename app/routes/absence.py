# from flask import Blueprint, render_template, redirect, url_for, flash, request
# from flask_login import login_required, current_user
# from app.models.models import db, Absence, Etudiant, Module, Specialite, Annee, Notification, User
# from datetime import datetime
# from app.utils.email import send_absence_notification
# import os
# from app import Config

# absence = Blueprint('absence', __name__)

# @absence.route('/absences')
# @login_required
# def index():
#     if current_user.role != 'responsable':
#         flash('Accès non autorisé', 'danger')
#         return redirect(url_for('dashboard.index'))
    
#     # Get filter parameters
#     specialite_id = request.args.get('specialite_id', type=int)
#     annee_id = request.args.get('annee_id', type=int)
#     module_id = request.args.get('module_id', type=int)
#     statut = request.args.get('statut')
#     date_debut = request.args.get('date_debut')
#     date_fin = request.args.get('date_fin')
    
#     # Base query
#     query = Absence.query.join(Etudiant).join(Module)
    
#     # Apply filters
#     if specialite_id:
#         query = query.filter(Etudiant.specialite_id == specialite_id)
    
#     if annee_id:
#         query = query.filter(Etudiant.annee_id == annee_id)
    
#     if module_id:
#         query = query.filter(Absence.module_id == module_id)
    
#     if statut:
#         query = query.filter(Absence.statut == statut)
    
#     if date_debut:
#         date_debut = datetime.strptime(date_debut, '%Y-%m-%d').date()
#         query = query.filter(Absence.date >= date_debut)
    
#     if date_fin:
#         date_fin = datetime.strptime(date_fin, '%Y-%m-%d').date()
#         query = query.filter(Absence.date <= date_fin)
    
#     # Get data for filters
#     specialites = Specialite.query.all()
#     annees = Annee.query.all()
#     modules = Module.query.all()
    
#     # Get absences with pagination
#     page = request.args.get('page', 1, type=int)
#     absences = query.order_by(Absence.date.desc()).paginate(page=page, per_page=20)
    
#     return render_template('absence/index.html', 
#                           title='Gestion des Absences',
#                           absences=absences,
#                           specialites=specialites,
#                           annees=annees,
#                           modules=modules,
#                           selected_specialite=specialite_id,
#                           selected_annee=annee_id,
#                           selected_module=module_id,
#                           selected_statut=statut,
#                           date_debut=date_debut,
#                           date_fin=date_fin)

# @absence.route('/absences/ajouter', methods=['GET', 'POST'])
# @login_required
# def ajouter():
#     if current_user.role != 'responsable':
#         flash('Accès non autorisé', 'danger')
#         return redirect(url_for('dashboard.index'))
    
#     if request.method == 'POST':
#         etudiant_id = request.form.get('etudiant_id', type=int)
#         module_id = request.form.get('module_id', type=int)
#         date = request.form.get('date')
#         heure_debut = request.form.get('heure_debut')
#         heure_fin = request.form.get('heure_fin')
        
#         if not all([etudiant_id, module_id, date, heure_debut, heure_fin]):
#             flash('Tous les champs sont obligatoires', 'danger')
#             return redirect(url_for('absence.ajouter'))
        
#         # Convert string dates to Python date/time objects
#         date = datetime.strptime(date, '%Y-%m-%d').date()
#         heure_debut = datetime.strptime(heure_debut, '%H:%M').time()
#         heure_fin = datetime.strptime(heure_fin, '%H:%M').time()
        
#         # Create new absence
#         nouvelle_absence = Absence(
#             etudiant_id=etudiant_id,
#             module_id=module_id,
#             date=date,
#             heure_debut=heure_debut,
#             heure_fin=heure_fin,
#             statut='non_justifiee'
#         )
        
#         db.session.add(nouvelle_absence)
#         db.session.commit()
        
#         # Create notification for the student
#         etudiant = Etudiant.query.get(etudiant_id)
#         module = Module.query.get(module_id)
        
#         notification = Notification(
#             user_id=etudiant.user_id,
#             message=f"Une absence a été enregistrée pour le module {module.nom} du {date.strftime('%d/%m/%Y')}",
#             type='nouvelle_absence'
#         )
        
#         db.session.add(notification)
#         db.session.commit()
        
#         # Send email notification
#         send_absence_notification(etudiant, nouvelle_absence)
        
#         flash('Absence ajoutée avec succès', 'success')
#         return redirect(url_for('absence.index'))
    
#     # Get data for the form
#     etudiants = Etudiant.query.all()
#     modules = Module.query.all()
    
#     return render_template('absence/ajouter.html', 
#                           title='Ajouter une Absence',
#                           etudiants=etudiants,
#                           modules=modules)

# @absence.route('/absences/<int:absence_id>/valider', methods=['POST'])
# @login_required
# def valider(absence_id):
#     if current_user.role != 'responsable':
#         flash('Accès non autorisé', 'danger')
#         return redirect(url_for('dashboard.index'))
    
#     absence = Absence.query.get_or_404(absence_id)
    
#     if absence.statut != 'en_attente':
#         flash('Cette absence ne peut pas être validée', 'warning')
#         return redirect(url_for('absence.index'))
    
#     absence.statut = 'justifiee'
#     absence.updated_at = datetime.utcnow()
#     db.session.commit()
    
#     # Create notification for the student
#     notification = Notification(
#         user_id=absence.etudiant.user_id,
#         message=f"Votre justificatif pour l'absence du {absence.date.strftime('%d/%m/%Y')} a été accepté",
#         type='justificatif_valide'
#     )
    
#     db.session.add(notification)
#     db.session.commit()
    
#     # Send email notification
#     # This would be implemented in an email service
    
#     flash('Justificatif validé avec succès', 'success')
#     return redirect(url_for('absence.index'))

# @absence.route('/absences/<int:absence_id>/refuser', methods=['POST'])
# @login_required
# def refuser(absence_id):
#     if current_user.role != 'responsable':
#         flash('Accès non autorisé', 'danger')
#         return redirect(url_for('dashboard.index'))
    
#     absence = Absence.query.get_or_404(absence_id)
    
#     if absence.statut != 'en_attente':
#         flash('Cette absence ne peut pas être refusée', 'warning')
#         return redirect(url_for('absence.index'))
    
#     raison = request.form.get('raison')
    
#     absence.statut = 'refusee'
#     absence.commentaire = raison
#     absence.updated_at = datetime.utcnow()
#     db.session.commit()
    
#     # Create notification for the student
#     notification = Notification(
#         user_id=absence.etudiant.user_id,
#         message=f"Votre justificatif pour l'absence du {absence.date.strftime('%d/%m/%Y')} a été refusé. Raison: {raison}",
#         type='justificatif_refuse'
#     )
    
#     db.session.add(notification)
#     db.session.commit()
    
#     # Send email notification
#     # This would be implemented in an email service
    
#     flash('Justificatif refusé', 'success')
#     return redirect(url_for('absence.index'))

# @absence.route('/absences/<int:absence_id>/voir-justificatif')
# @login_required
# def voir_justificatif(absence_id):
#     absence = Absence.query.get_or_404(absence_id)
    
#     if not absence.justificatif_path:
#         flash('Aucun justificatif disponible', 'warning')
#         return redirect(url_for('absence.index'))
    
#     # Check permissions
#     if current_user.role == 'etudiant' and absence.etudiant_id != current_user.etudiant.id:
#         flash('Accès non autorisé', 'danger')
#         return redirect(url_for('dashboard.index'))
    
#     file_path = os.path.join(Config.UPLOAD_FOLDER, absence.justificatif_path)
    
#     if not os.path.exists(file_path):
#         flash('Fichier non trouvé', 'danger')
#         return redirect(url_for('absence.index'))
    
#     # Determine file type to decide how to display it
#     file_ext = absence.justificatif_path.rsplit('.', 1)[1].lower()
    
#     if file_ext in ['jpg', 'jpeg', 'png']:
#         file_type = 'image'
#     elif file_ext == 'pdf':
#         file_type = 'pdf'
#     else:
#         file_type = 'unknown'
    
#     return render_template('absence/justificatif.html',
#                           title='Voir Justificatif',
#                           absence=absence,
#                           file_type=file_type)

# @absence.route('/absences/bulk-validate', methods=['POST'])
# @login_required
# def bulk_validate():
#     if current_user.role != 'responsable':
#         return {'success': False, 'message': 'Accès non autorisé'}, 403
    
#     absence_ids = request.form.get('absences', '').split(',')
    
#     try:
#         for absence_id in absence_ids:
#             if absence_id:
#                 absence = Absence.query.get(int(absence_id))
#                 if absence and absence.statut == 'en_attente':
#                     absence.statut = 'justifiee'
#                     absence.updated_at = datetime.utcnow()
                    
#                     # Create notification
#                     notification = Notification(
#                         user_id=absence.etudiant.user_id,
#                         message=f"Votre justificatif pour l'absence du {absence.date.strftime('%d/%m/%Y')} a été accepté",
#                         type='justificatif_valide'
#                     )
#                     db.session.add(notification)
        
#         db.session.commit()
#         return {'success': True, 'message': 'Absences validées avec succès'}
    
#     except Exception as e:
#         db.session.rollback()
#         return {'success': False, 'message': str(e)}, 500

# @absence.route('/absences/bulk-refuse', methods=['POST'])
# @login_required
# def bulk_refuse():
#     if current_user.role != 'responsable':
#         return {'success': False, 'message': 'Accès non autorisé'}, 403
    
#     absence_ids = request.form.get('selected_absences', '').split(',')
#     raison = request.form.get('raison')
    
#     try:
#         for absence_id in absence_ids:
#             if absence_id:
#                 absence = Absence.query.get(int(absence_id))
#                 if absence and absence.statut == 'en_attente':
#                     absence.statut = 'refusee'
#                     absence.commentaire = raison
#                     absence.updated_at = datetime.utcnow()
                    
#                     # Create notification
#                     notification = Notification(
#                         user_id=absence.etudiant.user_id,
#                         message=f"Votre justificatif pour l'absence du {absence.date.strftime('%d/%m/%Y')} a été refusé. Raison: {raison}",
#                         type='justificatif_refuse'
#                     )
#                     db.session.add(notification)
        
#         db.session.commit()
#         return {'success': True, 'message': 'Absences refusées avec succès'}
    
#     except Exception as e:
#         db.session.rollback()
#         return {'success': False, 'message': str(e)}, 500
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models.models import db, Absence, Etudiant, Module, Specialite, Annee, Notification, User
from datetime import datetime
from app.utils.email import send_absence_notification
from app.utils.notifications import (
    send_absence_notification_complete, 
    send_justification_notification_complete,
    notify_responsables_new_justification
)
import os
from app import Config

absence = Blueprint('absence', __name__)

@absence.route('/absences')
@login_required
def index():
    if current_user.role != 'responsable':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard.index'))
    
    # Get filter parameters
    specialite_id = request.args.get('specialite_id', type=int)
    annee_id = request.args.get('annee_id', type=int)
    module_id = request.args.get('module_id', type=int)
    statut = request.args.get('statut')
    date_debut = request.args.get('date_debut')
    date_fin = request.args.get('date_fin')
    
    # Base query
    query = Absence.query.join(Etudiant).join(Module)
    
    # Apply filters
    if specialite_id:
        query = query.filter(Etudiant.specialite_id == specialite_id)
    
    if annee_id:
        query = query.filter(Etudiant.annee_id == annee_id)
    
    if module_id:
        query = query.filter(Absence.module_id == module_id)
    
    if statut:
        query = query.filter(Absence.statut == statut)
    
    if date_debut:
        date_debut = datetime.strptime(date_debut, '%Y-%m-%d').date()
        query = query.filter(Absence.date >= date_debut)
    
    if date_fin:
        date_fin = datetime.strptime(date_fin, '%Y-%m-%d').date()
        query = query.filter(Absence.date <= date_fin)
    
    # Get data for filters
    specialites = Specialite.query.all()
    annees = Annee.query.all()
    modules = Module.query.all()
    
    # Get absences with pagination
    page = request.args.get('page', 1, type=int)
    absences = query.order_by(Absence.date.desc()).paginate(page=page, per_page=20, error_out=False)
    
    return render_template('absence/index.html', 
                          title='Gestion des Absences',
                          absences=absences,
                          specialites=specialites,
                          annees=annees,
                          modules=modules,
                          selected_specialite=specialite_id,
                          selected_annee=annee_id,
                          selected_module=module_id,
                          selected_statut=statut,
                          date_debut=date_debut,
                          date_fin=date_fin)

@absence.route('/absences/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter():
    if current_user.role != 'responsable':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        etudiant_id = request.form.get('etudiant_id', type=int)
        module_id = request.form.get('module_id', type=int)
        date = request.form.get('date')
        heure_debut = request.form.get('heure_debut')
        heure_fin = request.form.get('heure_fin')
        
        if not all([etudiant_id, module_id, date, heure_debut, heure_fin]):
            flash('Tous les champs sont obligatoires', 'danger')
            return redirect(url_for('absence.ajouter'))
        
        # Convert string dates to Python date/time objects
        date = datetime.strptime(date, '%Y-%m-%d').date()
        heure_debut = datetime.strptime(heure_debut, '%H:%M').time()
        heure_fin = datetime.strptime(heure_fin, '%H:%M').time()
        
        # Create new absence
        nouvelle_absence = Absence(
            etudiant_id=etudiant_id,
            module_id=module_id,
            date=date,
            heure_debut=heure_debut,
            heure_fin=heure_fin,
            statut='non_justifiee'
        )
        
        db.session.add(nouvelle_absence)
        db.session.commit()
        
        # Get related objects
        etudiant = Etudiant.query.get(etudiant_id)
        
        # Send complete notification (in-app + email)
        send_absence_notification_complete(etudiant, nouvelle_absence)
        
        flash('Absence ajoutée avec succès', 'success')
        return redirect(url_for('absence.index'))
    
    # Get data for the form
    etudiants = Etudiant.query.all()
    modules = Module.query.all()
    
    return render_template('absence/ajouter.html', 
                          title='Ajouter une Absence',
                          etudiants=etudiants,
                          modules=modules)

@absence.route('/absences/<int:absence_id>/valider', methods=['POST'])
@login_required
def valider(absence_id):
    if current_user.role != 'responsable':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard.index'))
    
    absence = Absence.query.get_or_404(absence_id)
    
    if absence.statut != 'en_attente':
        flash('Cette absence ne peut pas être validée', 'warning')
        return redirect(url_for('absence.index'))
    
    absence.statut = 'justifiee'
    absence.updated_at = datetime.utcnow()
    db.session.commit()
    
    # Send complete notification (in-app + email)
    send_justification_notification_complete(absence, accepted=True)
    
    flash('Justificatif validé avec succès', 'success')
    return redirect(url_for('absence.index'))

@absence.route('/absences/<int:absence_id>/refuser', methods=['POST'])
@login_required
def refuser(absence_id):
    if current_user.role != 'responsable':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard.index'))
    
    absence = Absence.query.get_or_404(absence_id)
    
    if absence.statut != 'en_attente':
        flash('Cette absence ne peut pas être refusée', 'warning')
        return redirect(url_for('absence.index'))
    
    raison = request.form.get('raison')
    
    absence.statut = 'refusee'
    absence.commentaire = raison
    absence.updated_at = datetime.utcnow()
    db.session.commit()
    
    # Send complete notification (in-app + email)
    send_justification_notification_complete(absence, accepted=False, raison=raison)
    
    flash('Justificatif refusé', 'success')
    return redirect(url_for('absence.index'))

@absence.route('/absences/<int:absence_id>/voir-justificatif')
@login_required
def voir_justificatif(absence_id):
    absence = Absence.query.get_or_404(absence_id)
    
    if not absence.justificatif_path:
        flash('Aucun justificatif disponible', 'warning')
        return redirect(url_for('absence.index'))
    
    # Check permissions
    if current_user.role == 'etudiant' and absence.etudiant_id != current_user.etudiant.id:
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard.index'))
    
    file_path = os.path.join(Config.UPLOAD_FOLDER, absence.justificatif_path)
    
    if not os.path.exists(file_path):
        flash('Fichier non trouvé', 'danger')
        return redirect(url_for('absence.index'))
    
    # Determine file type to decide how to display it
    file_ext = absence.justificatif_path.rsplit('.', 1)[1].lower()
    
    if file_ext in ['jpg', 'jpeg', 'png']:
        file_type = 'image'
    elif file_ext == 'pdf':
        file_type = 'pdf'
    else:
        file_type = 'unknown'
    
    return render_template('absence/justificatif.html',
                          title='Voir Justificatif',
                          absence=absence,
                          file_type=file_type)

@absence.route('/absences/bulk-validate', methods=['POST'])
@login_required
def bulk_validate():
    if current_user.role != 'responsable':
        return jsonify({'success': False, 'message': 'Accès non autorisé'}), 403
    
    absence_ids = request.form.get('absences', '').split(',')
    
    try:
        for absence_id in absence_ids:
            if absence_id:
                absence = Absence.query.get(int(absence_id))
                if absence and absence.statut == 'en_attente':
                    absence.statut = 'justifiee'
                    absence.updated_at = datetime.utcnow()
                    
                    # Send complete notification (in-app + email)
                    send_justification_notification_complete(absence, accepted=True)
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Absences validées avec succès'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@absence.route('/absences/bulk-refuse', methods=['POST'])
@login_required
def bulk_refuse():
    if current_user.role != 'responsable':
        return jsonify({'success': False, 'message': 'Accès non autorisé'}), 403
    
    absence_ids = request.form.get('selected_absences', '').split(',')
    raison = request.form.get('raison')
    
    try:
        for absence_id in absence_ids:
            if absence_id:
                absence = Absence.query.get(int(absence_id))
                if absence and absence.statut == 'en_attente':
                    absence.statut = 'refusee'
                    absence.commentaire = raison
                    absence.updated_at = datetime.utcnow()
                    
                    # Send complete notification (in-app + email)
                    send_justification_notification_complete(absence, accepted=False, raison=raison)
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Absences refusées avec succès'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
