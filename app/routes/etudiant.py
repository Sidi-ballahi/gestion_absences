# from flask import Blueprint, render_template, redirect, url_for, flash, request
# from flask_login import login_required, current_user
# from app.models.models import db, Absence, Module
# from werkzeug.utils import secure_filename
# import os
# from app import Config
# from datetime import datetime
# import json
# from sqlalchemy import func

# etudiant = Blueprint('etudiant', __name__)

# @etudiant.route('/dashboard')
# @login_required
# def dashboard():
#     if current_user.role != 'etudiant':
#         flash('Accès non autorisé', 'danger')
#         return redirect(url_for('dashboard.index'))
    
#     # Get student's absences statistics
#     total_absences = Absence.query.filter_by(etudiant_id=current_user.etudiant.id).count()
#     absences_justifiees = Absence.query.filter_by(etudiant_id=current_user.etudiant.id, statut='justifiee').count()
#     absences_refusees = Absence.query.filter_by(etudiant_id=current_user.etudiant.id, statut='refusee').count()
#     absences_en_attente = Absence.query.filter_by(etudiant_id=current_user.etudiant.id, statut='en_attente').count()
    
#     # Get absences by module for pie chart
#     absences_by_module = db.session.query(
#         Module.nom, func.count(Absence.id).label('total')
#     ).join(Absence).filter(Absence.etudiant_id == current_user.etudiant.id).group_by(Module.id).all()
    
#     module_names = [module for module, _ in absences_by_module]
#     module_counts = [count for _, count in absences_by_module]
    
#     # Recent absences
#     recent_absences = Absence.query.filter_by(etudiant_id=current_user.etudiant.id).order_by(Absence.date.desc()).limit(5).all()
    
#     return render_template('etudiant/dashboard.html',
#                           title='Mon Tableau de Bord',
#                           total_absences=total_absences,
#                           absences_justifiees=absences_justifiees,
#                           absences_refusees=absences_refusees,
#                           absences_en_attente=absences_en_attente,
#                           module_names=json.dumps(module_names),
#                           module_counts=json.dumps(module_counts),
#                           recent_absences=recent_absences)

# @etudiant.route('/absences')
# @login_required
# def absences():
#     if current_user.role != 'etudiant':
#         flash('Accès non autorisé', 'danger')
#         return redirect(url_for('dashboard.index'))
    
#     # Get filter parameters
#     module_id = request.args.get('module_id', type=int)
#     statut = request.args.get('statut')
#     date_debut = request.args.get('date_debut')
#     date_fin = request.args.get('date_fin')
    
#     # Base query
#     query = Absence.query.filter_by(etudiant_id=current_user.etudiant.id)
    
#     # Apply filters
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
    
#     absences = query.order_by(Absence.date.desc()).all()
    
#     # Get modules for filter
#     modules = db.session.query(Module).join(Absence).filter(
#         Absence.etudiant_id == current_user.etudiant.id
#     ).distinct().all()
    
#     # Calculate statistics
#     status_counts = {
#         'non_justifiee': query.filter_by(statut='non_justifiee').count(),
#         'en_attente': query.filter_by(statut='en_attente').count(),
#         'justifiee': query.filter_by(statut='justifiee').count(),
#         'refusee': query.filter_by(statut='refusee').count()
#     }
    
#     # Get absences by module for chart
#     module_stats = db.session.query(
#         Module.nom, func.count(Absence.id).label('total')
#     ).join(Absence).filter(
#         Absence.etudiant_id == current_user.etudiant.id
#     ).group_by(Module.id).all()
    
#     module_names = [module for module, _ in module_stats]
#     module_counts = [count for _, count in module_stats]
    
#     return render_template('etudiant/absences.html',
#                           title='Mes Absences',
#                           absences=absences,
#                           modules=modules,
#                           selected_module=module_id,
#                           selected_statut=statut,
#                           date_debut=date_debut,
#                           date_fin=date_fin,
#                           status_counts=status_counts,
#                           module_names=json.dumps(module_names),
#                           module_counts=json.dumps(module_counts))

# @etudiant.route('/absence/<int:absence_id>/justifier', methods=['GET', 'POST'])
# @login_required
# def justifier_absence(absence_id):
#     if current_user.role != 'etudiant':
#         flash('Accès non autorisé', 'danger')
#         return redirect(url_for('dashboard.index'))
    
#     absence = Absence.query.get_or_404(absence_id)
    
#     # Check if the absence belongs to the current student
#     if absence.etudiant_id != current_user.etudiant.id:
#         flash('Accès non autorisé', 'danger')
#         return redirect(url_for('etudiant.absences'))
    
#     # Check if the absence can be justified
#     if absence.statut not in ['non_justifiee', 'refusee']:
#         flash('Cette absence ne peut pas être justifiée', 'warning')
#         return redirect(url_for('etudiant.absences'))
    
#     if request.method == 'POST':
#         # Check if a file was uploaded
#         if 'justificatif' not in request.files:
#             flash('Aucun fichier sélectionné', 'danger')
#             return redirect(request.url)
        
#         file = request.files['justificatif']
        
#         if file.filename == '':
#             flash('Aucun fichier sélectionné', 'danger')
#             return redirect(request.url)
        
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             # Add timestamp to filename to make it unique
#             filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
#             file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
#             file.save(file_path)
            
#             # Update absence
#             absence.statut = 'en_attente'
#             absence.justificatif_path = filename
#             absence.commentaire = request.form.get('commentaire')
#             absence.updated_at = datetime.utcnow()
#             db.session.commit()
            
#             # Create notification for responsables
#             # This would be implemented in a notification service
            
#             flash('Justificatif soumis avec succès', 'success')
#             return redirect(url_for('etudiant.absences'))
#         else:
#             flash('Type de fichier non autorisé', 'danger')
#             return redirect(request.url)
    
#     return render_template('etudiant/justifier.html', title='Justifier une Absence', absence=absence)

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.models import db, Absence, Module
from werkzeug.utils import secure_filename
import os
from app import Config
from datetime import datetime
import json
from sqlalchemy import func
from app.utils.notifications import notify_responsables_new_justification

etudiant = Blueprint('etudiant', __name__)

@etudiant.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'etudiant':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard.index'))
    
    # Get student's absences statistics
    total_absences = Absence.query.filter_by(etudiant_id=current_user.etudiant.id).count()
    absences_justifiees = Absence.query.filter_by(etudiant_id=current_user.etudiant.id, statut='justifiee').count()
    absences_refusees = Absence.query.filter_by(etudiant_id=current_user.etudiant.id, statut='refusee').count()
    absences_en_attente = Absence.query.filter_by(etudiant_id=current_user.etudiant.id, statut='en_attente').count()
    
    # Get absences by module for pie chart
    absences_by_module = db.session.query(
        Module.nom, func.count(Absence.id).label('total')
    ).join(Absence).filter(Absence.etudiant_id == current_user.etudiant.id).group_by(Module.id).all()
    
    module_names = [module for module, _ in absences_by_module]
    module_counts = [count for _, count in absences_by_module]
    
    # Recent absences
    recent_absences = Absence.query.filter_by(etudiant_id=current_user.etudiant.id).order_by(Absence.date.desc()).limit(5).all()
    
    return render_template('etudiant/dashboard.html',
                          title='Mon Tableau de Bord',
                          total_absences=total_absences,
                          absences_justifiees=absences_justifiees,
                          absences_refusees=absences_refusees,
                          absences_en_attente=absences_en_attente,
                          module_names=json.dumps(module_names),
                          module_counts=json.dumps(module_counts),
                          recent_absences=recent_absences)

@etudiant.route('/absences')
@login_required
def absences():
    if current_user.role != 'etudiant':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard.index'))
    
    # Get filter parameters
    module_id = request.args.get('module_id', type=int)
    statut = request.args.get('statut')
    date_debut = request.args.get('date_debut')
    date_fin = request.args.get('date_fin')
    
    # Base query
    query = Absence.query.filter_by(etudiant_id=current_user.etudiant.id)
    
    # Apply filters
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
    
    absences = query.order_by(Absence.date.desc()).all()
    
    # Get modules for filter
    modules = db.session.query(Module).join(Absence).filter(
        Absence.etudiant_id == current_user.etudiant.id
    ).distinct().all()
    
    # Calculate statistics
    status_counts = {
        'non_justifiee': query.filter_by(statut='non_justifiee').count(),
        'en_attente': query.filter_by(statut='en_attente').count(),
        'justifiee': query.filter_by(statut='justifiee').count(),
        'refusee': query.filter_by(statut='refusee').count()
    }
    
    # Get absences by module for chart
    module_stats = db.session.query(
        Module.nom, func.count(Absence.id).label('total')
    ).join(Absence).filter(
        Absence.etudiant_id == current_user.etudiant.id
    ).group_by(Module.id).all()
    
    module_names = [module for module, _ in module_stats]
    module_counts = [count for _, count in module_stats]
    
    return render_template('etudiant/absences.html',
                          title='Mes Absences',
                          absences=absences,
                          modules=modules,
                          selected_module=module_id,
                          selected_statut=statut,
                          date_debut=date_debut,
                          date_fin=date_fin,
                          status_counts=status_counts,
                          module_names=json.dumps(module_names),
                          module_counts=json.dumps(module_counts))

@etudiant.route('/absence/<int:absence_id>/justifier', methods=['GET', 'POST'])
@login_required
def justifier_absence(absence_id):
    if current_user.role != 'etudiant':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard.index'))
    
    absence = Absence.query.get_or_404(absence_id)
    
    # Check if the absence belongs to the current student
    if absence.etudiant_id != current_user.etudiant.id:
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('etudiant.absences'))
    
    # Check if the absence can be justified
    if absence.statut not in ['non_justifiee', 'refusee']:
        flash('Cette absence ne peut pas être justifiée', 'warning')
        return redirect(url_for('etudiant.absences'))
    
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'justificatif' not in request.files:
            flash('Aucun fichier sélectionné', 'danger')
            return redirect(request.url)
        
        file = request.files['justificatif']
        
        if file.filename == '':
            flash('Aucun fichier sélectionné', 'danger')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Add timestamp to filename to make it unique
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
            
            # Create upload directory if it doesn't exist
            os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
            file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            file.save(file_path)
            
            # Update absence
            absence.statut = 'en_attente'
            absence.justificatif_path = filename
            absence.commentaire = request.form.get('commentaire')
            absence.updated_at = datetime.utcnow()
            db.session.commit()
            
            # Notify responsables about new justification
            notify_responsables_new_justification(absence)
            
            flash('Justificatif soumis avec succès', 'success')
            return redirect(url_for('etudiant.absences'))
        else:
            flash('Type de fichier non autorisé', 'danger')
            return redirect(request.url)
    
    return render_template('etudiant/justifier.html', title='Justifier une Absence', absence=absence)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
