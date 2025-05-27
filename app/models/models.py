from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'etudiant' or 'responsable'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    etudiant = db.relationship('Etudiant', backref='user', uselist=False)
    responsable = db.relationship('Responsable', backref='user', uselist=False)
    notifications = db.relationship('Notification', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Etudiant(db.Model):
    __tablename__ = 'etudiants'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    numero_etudiant = db.Column(db.String(20), unique=True, nullable=False)
    specialite_id = db.Column(db.Integer, db.ForeignKey('specialites.id'))
    annee_id = db.Column(db.Integer, db.ForeignKey('annees.id'))
    
    # Relationships
    absences = db.relationship('Absence', backref='etudiant', lazy='dynamic')

class Responsable(db.Model):
    __tablename__ = 'responsables'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    titre = db.Column(db.String(100))

class Specialite(db.Model):
    __tablename__ = 'specialites'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    
    # Relationships
    etudiants = db.relationship('Etudiant', backref='specialite', lazy='dynamic')
    modules = db.relationship('Module', backref='specialite', lazy='dynamic')

class Annee(db.Model):
    __tablename__ = 'annees'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False, unique=True)  # e.g., "2023-2024"
    
    # Relationships
    etudiants = db.relationship('Etudiant', backref='annee', lazy='dynamic')

class Module(db.Model):
    __tablename__ = 'modules'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), nullable=False, unique=True)
    nom = db.Column(db.String(100), nullable=False)
    specialite_id = db.Column(db.Integer, db.ForeignKey('specialites.id'))
    
    # Relationships
    absences = db.relationship('Absence', backref='module', lazy='dynamic')

class Absence(db.Model):
    __tablename__ = 'absences'
    
    id = db.Column(db.Integer, primary_key=True)
    etudiant_id = db.Column(db.Integer, db.ForeignKey('etudiants.id'))
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'))
    date = db.Column(db.Date, nullable=False)
    heure_debut = db.Column(db.Time, nullable=False)
    heure_fin = db.Column(db.Time, nullable=False)
    justifiee = db.Column(db.Boolean, default=False)
    justificatif_path = db.Column(db.String(255))
    statut = db.Column(db.String(20), default='non_justifiee')  # non_justifiee, en_attente, justifiee, refusee
    commentaire = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50))  # nouvelle_absence, justificatif_valide, justificatif_refuse, rappel
    lue = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
