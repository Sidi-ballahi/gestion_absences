from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.models import db, Absence, Etudiant, Module, Specialite, Annee
from sqlalchemy import func
from datetime import datetime, timedelta
import json

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
@login_required
def index():
    if current_user.role == 'etudiant':
        return redirect(url_for('etudiant.dashboard'))
    
    # Get statistics for the dashboard
    total_etudiants = Etudiant.query.count()
    total_absences = Absence.query.count()
    absences_justifiees = Absence.query.filter_by(statut='justifiee').count()
    absences_en_attente = Absence.query.filter_by(statut='en_attente').count()
    
    # Top 5 students with most absences
    top_absents = db.session.query(
        Etudiant.id, Etudiant.nom, Etudiant.prenom, func.count(Absence.id).label('total')
    ).join(Absence).group_by(Etudiant.id).order_by(func.count(Absence.id).desc()).limit(5).all()
    
    # Modules with most absences
    top_modules = db.session.query(
        Module.id, Module.nom, func.count(Absence.id).label('total')
    ).join(Absence).group_by(Module.id).order_by(func.count(Absence.id).desc()).limit(5).all()
    
    # Monthly evolution of absences
    now = datetime.now()
    six_months_ago = now - timedelta(days=180)
    
    monthly_absences = db.session.query(
        func.year(Absence.date).label('year'),
        func.month(Absence.date).label('month'),
        func.count(Absence.id).label('total')
    ).filter(Absence.date >= six_months_ago).group_by(
        func.year(Absence.date), func.month(Absence.date)
    ).order_by(func.year(Absence.date), func.month(Absence.date)).all()
    
    # Format data for Chart.js
    months = []
    counts = []
    
    for year, month, total in monthly_absences:
        months.append(f"{month}/{year}")
        counts.append(total)
    
    # Recent absences for the table
    recent_absences = Absence.query.order_by(Absence.created_at.desc()).limit(10).all()
    
    return render_template('dashboard/index.html', 
                          title='Tableau de Bord',
                          total_etudiants=total_etudiants,
                          total_absences=total_absences,
                          absences_justifiees=absences_justifiees,
                          absences_en_attente=absences_en_attente,
                          top_absents=top_absents,
                          top_modules=top_modules,
                          months=json.dumps(months),
                          counts=json.dumps(counts),
                          recent_absences=recent_absences)
