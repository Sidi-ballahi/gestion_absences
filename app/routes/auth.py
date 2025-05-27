from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app.models.models import db, User, Etudiant, Responsable
from werkzeug.urls import url_parse
from app.utils.email import send_email

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = 'remember' in request.form
        
        user = User.query.filter_by(email=email).first()
        
        if user is None or not user.check_password(password):
            flash('Email ou mot de passe incorrect', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=remember)
        
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            if user.role == 'etudiant':
                next_page = url_for('etudiant.dashboard')
            else:
                next_page = url_for('dashboard.index')
        
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Connexion')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Handle profile update
        if current_user.role == 'etudiant':
            etudiant = current_user.etudiant
            etudiant.nom = request.form.get('nom')
            etudiant.prenom = request.form.get('prenom')
            db.session.commit()
        elif current_user.role == 'responsable':
            responsable = current_user.responsable
            responsable.nom = request.form.get('nom')
            responsable.prenom = request.form.get('prenom')
            responsable.titre = request.form.get('titre')
            db.session.commit()
        
        # Handle password change if provided
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if current_password and new_password and confirm_password:
            if not current_user.check_password(current_password):
                flash('Mot de passe actuel incorrect', 'danger')
            elif new_password != confirm_password:
                flash('Les nouveaux mots de passe ne correspondent pas', 'danger')
            else:
                current_user.set_password(new_password)
                db.session.commit()
                flash('Mot de passe mis à jour avec succès', 'success')
        
        flash('Profil mis à jour avec succès', 'success')
        return redirect(url_for('auth.profile'))
    
    if current_user.role == 'etudiant':
        return render_template('auth/profile.html', title='Mon Profil', user=current_user, etudiant=current_user.etudiant)
    else:
        return render_template('auth/profile.html', title='Mon Profil', user=current_user, responsable=current_user.responsable)
