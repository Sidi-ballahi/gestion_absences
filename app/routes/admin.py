# from flask import Blueprint, render_template, redirect, url_for, flash, request
# from flask_login import login_required, current_user
# from app.models.models import db, Specialite, Annee, Module, Etudiant, User, Responsable, Absence, Notification
# from werkzeug.security import generate_password_hash

# admin = Blueprint('admin', __name__)

# @admin.route('/admin')
# @login_required
# def index():
#     if current_user.role != 'responsable':
#         flash('Accès non autorisé', 'danger')
#         return redirect(url_for('dashboard.index'))
    
#     # Get statistics
#     total_specialites = Specialite.query.count()
#     total_modules = Module.query.count()
#     total_etudiants = Etudiant.query.count()
#     total_responsables = Responsable.query.count()
    
#     return render_template('admin/index.html', 
#                           title='Administration',
#                           total_specialites=total_specialites,
#                           total_modules=total_modules,
#                           total_etudiants=total_etudiants,
#                           total_responsables=total_responsables)

# # Specialités CRUD
# @admin.route('/admin/specialites')
# @login_required
# def specialites():
#     if current_user.role != 'responsable':
#         flash('Accès non autorisé', 'danger')
#         return redirect(url_for('dashboard.index'))
    
#     specialites = Specialite.query.all()
#     return render_template('admin/specialites.html', title='Gestion des Spécialités', specialites=specialites)

# @admin.route('/admin/specialites/ajouter', methods=['GET', 'POST'])
# @login_required
# def ajouter_specialite():
#     if current_user.role != 'responsable':
#         flash('Accès non autorisé', 'danger')
#         return redirect(url_for('dashboard.index'))
    
#     if request.method == 'POST':
#         nom = request.form.get('nom')
#         description = request.form.get('description')
        
#         if not nom:
#             flash('Le nom est obligatoire', 'danger')
#             return redirect(url_for('admin.ajouter_specialite'))
        
#         specialite = Specialite(nom=nom, description=description)
#         db.session.add(specialite)
#         db.session.commit()
        
#         flash('Spécialité ajoutée avec succès', 'success')
#         return redirect(url_for('admin.specialites'))
    
#     return render_template('admin/ajouter_specialite.html', title='Ajouter une Spécialité')

# @admin.route('/admin/specialites/<int:specialite_id>/modifier', methods=['GET', 'POST'])
# @login_required
# def modifier_specialite(specialite_id):
#     if current_user.role != 'responsable':
#         flash('Accès non autorisé', 'danger')
#         return redirect(url_for('dashboard.index'))
    
#     specialite = Specialite.query.get_or_404(specialite_id)
    
#     if request.method == 'POST':
#         nom = request.form.get('nom')
#         description = request.form.get('description')
        
#         if not nom:
#             flash('Le nom est obligatoire', 'danger')
#             return redirect(url_for('admin.modifier_specialite', specialite_id=specialite_id))
        
#         specialite.nom = nom
#         specialite.description = description
#         db.session.commit()
        
#         flash('Spécialité modifiée avec succès', 'success')
#         return redirect(url_for('admin.specialites'))
    
#     return render_template('admin/modifier_specialite.html', title='Modifier une Spécialité', specialite=specialite)

# @admin.route('/admin/specialites/<int:specialite_id>/supprimer', methods=['POST'])
# @login_required
# def supprimer_specialite(specialite_id):
#     if current_user.role != 'responsable':
#         flash('Accès non autorisé', 'danger')
#         return redirect(url_for('dashboard.index'))
    
#     specialite = Specialite.query.get_or_404(specialite_id)
    
#     # Check if the specialite is used by students or modules
#     if specialite.etudiants.count() > 0 or specialite.modules.count() > 0:
#         flash('Impossible de supprimer cette spécialité car elle est utilisée par des étudiants ou des modules', 'danger')
#         return redirect(url_for('admin.specialites'))
    
#     db.session.delete(specialite)
#     db.session.commit()
    
#     flash('Spécialité supprimée avec succès', 'success')
#     return redirect(url_for('admin.specialites'))

# # Similar CRUD operations for Annees and Modules would be implemented here
# # Add missing routes for years and modules
# @admin.route('/admin/annees')
# @login_required
# def annees():
#     if current_user.role != 'responsable':
#         flash('Accès non autorisé', 'danger')
#         return redirect(url_for('dashboard.index'))
    
#     annees = Annee.query.all()
#     return render_template('admin/annees.html', title='Gestion des Années', annees=annees)

# @admin.route('/admin/modules')
# @login_required
# def modules():
#     if current_user.role != 'responsable':
#         flash('Accès non autorisé', 'danger')
#         return redirect(url_for('dashboard.index'))
    
#     modules = Module.query.all()
#     specialites = Specialite.query.all()
#     return render_template('admin/modules.html', title='Gestion des Modules', modules=modules, specialites=specialites)

# # User management
# @admin.route('/admin/utilisateurs')
# @login_required
# def utilisateurs():
#     if current_user.role != 'responsable':
#         flash('Accès non autorisé', 'danger')
#         return redirect(url_for('dashboard.index'))
    
#     etudiants = Etudiant.query.join(User).all()
#     responsables = Responsable.query.join(User).all()
    
#     return render_template('admin/utilisateurs.html', 
#                           title='Gestion des Utilisateurs',
#                           etudiants=etudiants,
#                           responsables=responsables)

# @admin.route('/admin/utilisateurs/ajouter', methods=['GET', 'POST'])
# @login_required
# def ajouter_utilisateur():
#     if current_user.role != 'responsable':
#         flash('Accès non autorisé', 'danger')
#         return redirect(url_for('dashboard.index'))
    
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')
#         role = request.form.get('role')
#         nom = request.form.get('nom')
#         prenom = request.form.get('prenom')
        
#         # Check if email already exists
#         if User.query.filter_by(email=email).first():
#             flash('Cet email est déjà utilisé', 'danger')
#             return redirect(url_for('admin.ajouter_utilisateur'))
        
#         # Create user
#         user = User(email=email, role=role)
#         user.set_password(password)
#         db.session.add(user)
#         db.session.flush()  # To get the user ID
        
#         if role == 'etudiant':
#             numero_etudiant = request.form.get('numero_etudiant')
#             specialite_id = request.form.get('specialite_id')
#             annee_id = request.form.get('annee_id')
            
#             etudiant = Etudiant(
#                 user_id=user.id,
#                 nom=nom,
#                 prenom=prenom,
#                 numero_etudiant=numero_etudiant,
#                 specialite_id=specialite_id,
#                 annee_id=annee_id
#             )
#             db.session.add(etudiant)
#         else:
#             titre = request.form.get('titre')
            
#             responsable = Responsable(
#                 user_id=user.id,
#                 nom=nom,
#                 prenom=prenom,
#                 titre=titre
#             )
#             db.session.add(responsable)
        
#         db.session.commit()
        
#         flash('Utilisateur ajouté avec succès', 'success')
#         return redirect(url_for('admin.utilisateurs'))
    
#     specialites = Specialite.query.all()
#     annees = Annee.query.all()
    
#     return render_template('admin/ajouter_utilisateur.html',
#                           title='Ajouter un Utilisateur',
#                           specialites=specialites,
#                           annees=annees)

# # Similar edit and delete operations for users would be implemented here
# # Add user deletion route
# @admin.route('/admin/utilisateurs/<int:user_id>/supprimer', methods=['POST'])
# @login_required
# def supprimer_utilisateur(user_id):
#     if current_user.role != 'responsable':
#         flash('Accès non autorisé', 'danger')
#         return redirect(url_for('dashboard.index'))
    
#     user = User.query.get_or_404(user_id)
    
#     # Don't allow deletion of current user
#     if user.id == current_user.id:
#         flash('Vous ne pouvez pas supprimer votre propre compte', 'danger')
#         return redirect(url_for('admin.utilisateurs'))
    
#     try:
#         # Delete associated records first
#         if user.role == 'etudiant' and user.etudiant:
#             # Delete absences first
#             Absence.query.filter_by(etudiant_id=user.etudiant.id).delete()
#             db.session.delete(user.etudiant)
#         elif user.role == 'responsable' and user.responsable:
#             db.session.delete(user.responsable)
        
#         # Delete notifications
#         Notification.query.filter_by(user_id=user.id).delete()
        
#         # Delete user
#         db.session.delete(user)
#         db.session.commit()
        
#         flash('Utilisateur supprimé avec succès', 'success')
#     except Exception as e:
#         db.session.rollback()
#         flash('Erreur lors de la suppression de l\'utilisateur', 'danger')
    
#     return redirect(url_for('admin.utilisateurs'))

# # Add user modification route
# @admin.route('/admin/utilisateurs/<int:user_id>/modifier', methods=['GET', 'POST'])
# @login_required
# def modifier_utilisateur(user_id):
#     if current_user.role != 'responsable':
#         flash('Accès non autorisé', 'danger')
#         return redirect(url_for('dashboard.index'))
    
#     user = User.query.get_or_404(user_id)
    
#     if request.method == 'POST':
#         # Update user information
#         nom = request.form.get('nom')
#         prenom = request.form.get('prenom')
        
#         if user.role == 'etudiant':
#             etudiant = user.etudiant
#             etudiant.nom = nom
#             etudiant.prenom = prenom
#             etudiant.numero_etudiant = request.form.get('numero_etudiant')
#             etudiant.specialite_id = request.form.get('specialite_id') or None
#             etudiant.annee_id = request.form.get('annee_id') or None
#         else:
#             responsable = user.responsable
#             responsable.nom = nom
#             responsable.prenom = prenom
#             responsable.titre = request.form.get('titre')
        
#         db.session.commit()
#         flash('Utilisateur modifié avec succès', 'success')
#         return redirect(url_for('admin.utilisateurs'))
    
#     specialites = Specialite.query.all()
#     annees = Annee.query.all()
    
#     return render_template('admin/modifier_utilisateur.html',
#                           title='Modifier un Utilisateur',
#                           user=user,
#                           specialites=specialites,
#                           annees=annees)

# # Routes for Années
# @admin.route('/admin/annees/ajouter', methods=['POST'])
# @login_required
# def ajouter_annee():
#     if current_user.role != 'responsable':
#         flash('Accès non autorisé', 'danger')
#         return redirect(url_for('dashboard.index'))
    
#     nom = request.form.get('nom')
    
#     if not nom:
#         flash('Le nom est obligatoire', 'danger')
#         return redirect(url_for('admin.annees'))
    
#     # Check if year already exists
#     if Annee.query.filter_by(nom=nom).first():
#         flash('Cette année existe déjà', 'danger')
#         return redirect(url_for('admin.annees'))
    
#     annee = Annee(nom=nom)
#     db.session.add(annee)
#     db.session.commit()
    
#     flash('Année ajoutée avec succès', 'success')
#     return redirect(url_for('admin.annees'))

# # Routes for Modules
# @admin.route('/admin/modules/ajouter', methods=['POST'])
# @login_required
# def ajouter_module():
#     if current_user.role != 'responsable':
#         flash('Accès non autorisé', 'danger')
#         return redirect(url_for('dashboard.index'))
    
#     code = request.form.get('code')
#     nom = request.form.get('nom')
#     specialite_id = request.form.get('specialite_id') or None
    
#     if not code or not nom:
#         flash('Le code et le nom sont obligatoires', 'danger')
#         return redirect(url_for('admin.modules'))
    
#     # Check if module code already exists
#     if Module.query.filter_by(code=code).first():
#         flash('Ce code de module existe déjà', 'danger')
#         return redirect(url_for('admin.modules'))
    
#     module = Module(code=code, nom=nom, specialite_id=specialite_id)
#     db.session.add(module)
#     db.session.commit()
    
#     flash('Module ajouté avec succès', 'success')
#     return redirect(url_for('admin.modules'))
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models.models import db, Specialite, Annee, Module, Etudiant, User, Responsable, Absence, Notification
from werkzeug.security import generate_password_hash

admin = Blueprint('admin', __name__)

@admin.route('/admin')
@login_required
def index():
    if current_user.role != 'responsable':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard.index'))
    
    # Get statistics
    total_specialites = Specialite.query.count()
    total_modules = Module.query.count()
    total_etudiants = Etudiant.query.count()
    total_responsables = Responsable.query.count()
    
    return render_template('admin/index.html', 
                          title='Administration',
                          total_specialites=total_specialites,
                          total_modules=total_modules,
                          total_etudiants=total_etudiants,
                          total_responsables=total_responsables)

# Specialités CRUD
@admin.route('/admin/specialites')
@login_required
def specialites():
    if current_user.role != 'responsable':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard.index'))
    
    specialites = Specialite.query.all()
    return render_template('admin/specialites.html', title='Gestion des Spécialités', specialites=specialites)

@admin.route('/admin/specialites/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter_specialite():
    if current_user.role != 'responsable':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        nom = request.form.get('nom')
        description = request.form.get('description')
        
        if not nom:
            flash('Le nom est obligatoire', 'danger')
            return redirect(url_for('admin.ajouter_specialite'))
        
        # Check if specialty already exists
        if Specialite.query.filter_by(nom=nom).first():
            flash('Cette spécialité existe déjà', 'danger')
            return redirect(url_for('admin.ajouter_specialite'))
        
        specialite = Specialite(nom=nom, description=description)
        db.session.add(specialite)
        db.session.commit()
        
        flash('Spécialité ajoutée avec succès', 'success')
        return redirect(url_for('admin.specialites'))
    
    return render_template('admin/ajouter_specialite.html', title='Ajouter une Spécialité')

@admin.route('/admin/specialites/<int:specialite_id>/modifier', methods=['GET', 'POST'])
@login_required
def modifier_specialite(specialite_id):
    if current_user.role != 'responsable':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard.index'))
    
    specialite = Specialite.query.get_or_404(specialite_id)
    
    if request.method == 'POST':
        nom = request.form.get('nom')
        description = request.form.get('description')
        
        if not nom:
            flash('Le nom est obligatoire', 'danger')
            return redirect(url_for('admin.modifier_specialite', specialite_id=specialite_id))
        
        # Check if another specialty with same name exists
        existing = Specialite.query.filter_by(nom=nom).first()
        if existing and existing.id != specialite.id:
            flash('Cette spécialité existe déjà', 'danger')
            return redirect(url_for('admin.modifier_specialite', specialite_id=specialite_id))
        
        specialite.nom = nom
        specialite.description = description
        db.session.commit()
        
        flash('Spécialité modifiée avec succès', 'success')
        return redirect(url_for('admin.specialites'))
    
    return render_template('admin/modifier_specialite.html', title='Modifier une Spécialité', specialite=specialite)

@admin.route('/admin/specialites/<int:specialite_id>/supprimer', methods=['POST'])
@login_required
def supprimer_specialite(specialite_id):
    if current_user.role != 'responsable':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard.index'))
    
    specialite = Specialite.query.get_or_404(specialite_id)
    
    # Check if the specialite is used by students or modules
    if specialite.etudiants.count() > 0 or specialite.modules.count() > 0:
        flash('Impossible de supprimer cette spécialité car elle est utilisée par des étudiants ou des modules', 'danger')
        return redirect(url_for('admin.specialites'))
    
    db.session.delete(specialite)
    db.session.commit()
    
    flash('Spécialité supprimée avec succès', 'success')
    return redirect(url_for('admin.specialites'))

# Années CRUD
@admin.route('/admin/annees')
@login_required
def annees():
    if current_user.role != 'responsable':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard.index'))
    
    annees = Annee.query.all()
    return render_template('admin/annees.html', title='Gestion des Années', annees=annees)

@admin.route('/admin/annees/ajouter', methods=['POST'])
@login_required
def ajouter_annee():
    if current_user.role != 'responsable':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard.index'))
    
    nom = request.form.get('nom')
    
    if not nom:
        flash('Le nom est obligatoire', 'danger')
        return redirect(url_for('admin.annees'))
    
    # Check if year already exists
    if Annee.query.filter_by(nom=nom).first():
        flash('Cette année existe déjà', 'danger')
        return redirect(url_for('admin.annees'))
    
    annee = Annee(nom=nom)
    db.session.add(annee)
    db.session.commit()
    
    flash('Année ajoutée avec succès', 'success')
    return redirect(url_for('admin.annees'))

@admin.route('/admin/annees/<int:annee_id>/modifier', methods=['POST'])
@login_required
def modifier_annee(annee_id):
    if current_user.role != 'responsable':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard.index'))
    
    annee = Annee.query.get_or_404(annee_id)
    nom = request.form.get('nom')
    
    if not nom:
        flash('Le nom est obligatoire', 'danger')
        return redirect(url_for('admin.annees'))
    
    # Check if another year with same name exists
    existing = Annee.query.filter_by(nom=nom).first()
    if existing and existing.id != annee.id:
        flash('Cette année existe déjà', 'danger')
        return redirect(url_for('admin.annees'))
    
    annee.nom = nom
    db.session.commit()
    
    flash('Année modifiée avec succès', 'success')
    return redirect(url_for('admin.annees'))

@admin.route('/admin/annees/<int:annee_id>/supprimer', methods=['POST'])
@login_required
def supprimer_annee(annee_id):
    if current_user.role != 'responsable':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard.index'))
    
    annee = Annee.query.get_or_404(annee_id)
    
    # Check if the year is used by students
    if annee.etudiants.count() > 0:
        flash('Impossible de supprimer cette année car elle est utilisée par des étudiants', 'danger')
        return redirect(url_for('admin.annees'))
    
    db.session.delete(annee)
    db.session.commit()
    
    flash('Année supprimée avec succès', 'success')
    return redirect(url_for('admin.annees'))

# Modules CRUD
@admin.route('/admin/modules')
@login_required
def modules():
    if current_user.role != 'responsable':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard.index'))
    
    modules = Module.query.all()
    specialites = Specialite.query.all()
    return render_template('admin/modules.html', title='Gestion des Modules', modules=modules, specialites=specialites)

@admin.route('/admin/modules/ajouter', methods=['POST'])
@login_required
def ajouter_module():
    if current_user.role != 'responsable':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard.index'))
    
    code = request.form.get('code')
    nom = request.form.get('nom')
    specialite_id = request.form.get('specialite_id') or None
    
    if not code or not nom:
        flash('Le code et le nom sont obligatoires', 'danger')
        return redirect(url_for('admin.modules'))
    
    # Check if module code already exists
    if Module.query.filter_by(code=code).first():
        flash('Ce code de module existe déjà', 'danger')
        return redirect(url_for('admin.modules'))
    
    module = Module(code=code, nom=nom, specialite_id=specialite_id)
    db.session.add(module)
    db.session.commit()
    
    flash('Module ajouté avec succès', 'success')
    return redirect(url_for('admin.modules'))

@admin.route('/admin/modules/<int:module_id>/modifier', methods=['POST'])
@login_required
def modifier_module(module_id):
    if current_user.role != 'responsable':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard.index'))
    
    module = Module.query.get_or_404(module_id)
    code = request.form.get('code')
    nom = request.form.get('nom')
    specialite_id = request.form.get('specialite_id') or None
    
    if not code or not nom:
        flash('Le code et le nom sont obligatoires', 'danger')
        return redirect(url_for('admin.modules'))
    
    # Check if another module with same code exists
    existing = Module.query.filter_by(code=code).first()
    if existing and existing.id != module.id:
        flash('Ce code de module existe déjà', 'danger')
        return redirect(url_for('admin.modules'))
    
    module.code = code
    module.nom = nom
    module.specialite_id = specialite_id
    db.session.commit()
    
    flash('Module modifié avec succès', 'success')
    return redirect(url_for('admin.modules'))

@admin.route('/admin/modules/<int:module_id>/supprimer', methods=['POST'])
@login_required
def supprimer_module(module_id):
    if current_user.role != 'responsable':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard.index'))
    
    module = Module.query.get_or_404(module_id)
    
    # Check if the module is used by absences
    if module.absences.count() > 0:
        flash('Impossible de supprimer ce module car il est utilisé par des absences', 'danger')
        return redirect(url_for('admin.modules'))
    
    db.session.delete(module)
    db.session.commit()
    
    flash('Module supprimé avec succès', 'success')
    return redirect(url_for('admin.modules'))

# User management
@admin.route('/admin/utilisateurs')
@login_required
def utilisateurs():
    if current_user.role != 'responsable':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard.index'))
    
    etudiants = Etudiant.query.join(User).all()
    responsables = Responsable.query.join(User).all()
    
    return render_template('admin/utilisateurs.html', 
                          title='Gestion des Utilisateurs',
                          etudiants=etudiants,
                          responsables=responsables)

@admin.route('/admin/utilisateurs/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter_utilisateur():
    if current_user.role != 'responsable':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash('Cet email est déjà utilisé', 'danger')
            return redirect(url_for('admin.ajouter_utilisateur'))
        
        # Create user
        user = User(email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()  # To get the user ID
        
        if role == 'etudiant':
            numero_etudiant = request.form.get('numero_etudiant')
            specialite_id = request.form.get('specialite_id')
            annee_id = request.form.get('annee_id')
            
            # Check if student number already exists
            if Etudiant.query.filter_by(numero_etudiant=numero_etudiant).first():
                flash('Ce numéro étudiant est déjà utilisé', 'danger')
                db.session.rollback()
                return redirect(url_for('admin.ajouter_utilisateur'))
            
            etudiant = Etudiant(
                user_id=user.id,
                nom=nom,
                prenom=prenom,
                numero_etudiant=numero_etudiant,
                specialite_id=specialite_id,
                annee_id=annee_id
            )
            db.session.add(etudiant)
        else:
            titre = request.form.get('titre')
            
            responsable = Responsable(
                user_id=user.id,
                nom=nom,
                prenom=prenom,
                titre=titre
            )
            db.session.add(responsable)
        
        db.session.commit()
        
        flash('Utilisateur ajouté avec succès', 'success')
        return redirect(url_for('admin.utilisateurs'))
    
    specialites = Specialite.query.all()
    annees = Annee.query.all()
    
    return render_template('admin/ajouter_utilisateur.html',
                          title='Ajouter un Utilisateur',
                          specialites=specialites,
                          annees=annees)

@admin.route('/admin/utilisateurs/<int:user_id>/supprimer', methods=['POST'])
@login_required
def supprimer_utilisateur(user_id):
    if current_user.role != 'responsable':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard.index'))
    
    user = User.query.get_or_404(user_id)
    
    # Don't allow deletion of current user
    if user.id == current_user.id:
        flash('Vous ne pouvez pas supprimer votre propre compte', 'danger')
        return redirect(url_for('admin.utilisateurs'))
    
    try:
        # Delete associated records first
        if user.role == 'etudiant' and user.etudiant:
            # Delete absences first
            Absence.query.filter_by(etudiant_id=user.etudiant.id).delete()
            db.session.delete(user.etudiant)
        elif user.role == 'responsable' and user.responsable:
            db.session.delete(user.responsable)
        
        # Delete notifications
        Notification.query.filter_by(user_id=user.id).delete()
        
        # Delete user
        db.session.delete(user)
        db.session.commit()
        
        flash('Utilisateur supprimé avec succès', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erreur lors de la suppression de l\'utilisateur', 'danger')
    
    return redirect(url_for('admin.utilisateurs'))

@admin.route('/admin/utilisateurs/<int:user_id>/modifier', methods=['GET', 'POST'])
@login_required
def modifier_utilisateur(user_id):
    if current_user.role != 'responsable':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard.index'))
    
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        # Update user information
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        
        if user.role == 'etudiant':
            etudiant = user.etudiant
            numero_etudiant = request.form.get('numero_etudiant')
            
            # Check if student number already exists for another student
            existing = Etudiant.query.filter_by(numero_etudiant=numero_etudiant).first()
            if existing and existing.id != etudiant.id:
                flash('Ce numéro étudiant est déjà utilisé', 'danger')
                return redirect(url_for('admin.modifier_utilisateur', user_id=user_id))
            
            etudiant.nom = nom
            etudiant.prenom = prenom
            etudiant.numero_etudiant = numero_etudiant
            etudiant.specialite_id = request.form.get('specialite_id') or None
            etudiant.annee_id = request.form.get('annee_id') or None
        else:
            responsable = user.responsable
            responsable.nom = nom
            responsable.prenom = prenom
            responsable.titre = request.form.get('titre')
        
        db.session.commit()
        flash('Utilisateur modifié avec succès', 'success')
        return redirect(url_for('admin.utilisateurs'))
    
    specialites = Specialite.query.all()
    annees = Annee.query.all()
    
    return render_template('admin/modifier_utilisateur.html',
                          title='Modifier un Utilisateur',
                          user=user,
                          specialites=specialites,
                          annees=annees)

# API Routes for notifications
@admin.route('/api/notifications')
@login_required
def get_notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id, lue=False).order_by(Notification.created_at.desc()).limit(10).all()
    
    notifications_data = []
    for notif in notifications:
        notifications_data.append({
            'id': notif.id,
            'message': notif.message,
            'type': notif.type,
            'created_at': notif.created_at.strftime('%d/%m/%Y %H:%M'),
            'lue': notif.lue
        })
    
    return jsonify({
        'notifications': notifications_data,
        'count': len(notifications_data)
    })

@admin.route('/api/notifications/<int:notification_id>/mark-read', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    notification = Notification.query.filter_by(id=notification_id, user_id=current_user.id).first_or_404()
    notification.lue = True
    db.session.commit()
    
    return jsonify({'success': True})

@admin.route('/api/notifications/mark-all-read', methods=['POST'])
@login_required
def mark_all_notifications_read():
    Notification.query.filter_by(user_id=current_user.id, lue=False).update({'lue': True})
    db.session.commit()
    
    return jsonify({'success': True})
