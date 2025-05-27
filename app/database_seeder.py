from app import create_app
from app.models.models import db, User, Etudiant, Responsable, Specialite, Annee, Module, Absence
from datetime import datetime, date, time
import random

def seed_database():
    app = create_app()
    
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Create specialties
        specialites = [
            Specialite(nom="Informatique", description="Spécialité en informatique et programmation"),
            Specialite(nom="Mathématiques", description="Spécialité en mathématiques appliquées"),
            Specialite(nom="Physique", description="Spécialité en physique et sciences"),
            Specialite(nom="Chimie", description="Spécialité en chimie et biochimie")
        ]
        
        for specialite in specialites:
            db.session.add(specialite)
        
        # Create years
        annees = [
            Annee(nom="2023-2024"),
            Annee(nom="2024-2025"),
            Annee(nom="2025-2026")
        ]
        
        for annee in annees:
            db.session.add(annee)
        
        db.session.commit()
        
        # Create modules
        modules_data = [
            ("INF101", "Programmation I", 1),
            ("INF102", "Base de données", 1),
            ("INF201", "Programmation II", 1),
            ("MAT101", "Algèbre linéaire", 2),
            ("MAT102", "Analyse", 2),
            ("PHY101", "Mécanique", 3),
            ("PHY102", "Électricité", 3),
            ("CHI101", "Chimie générale", 4),
            ("CHI102", "Chimie organique", 4)
        ]
        
        modules = []
        for code, nom, specialite_id in modules_data:
            module = Module(code=code, nom=nom, specialite_id=specialite_id)
            modules.append(module)
            db.session.add(module)
        
        # Create admin user
        admin_user = User(email="admin@example.com", role="responsable")
        admin_user.set_password("admin123")
        db.session.add(admin_user)
        db.session.flush()
        
        admin_responsable = Responsable(
            user_id=admin_user.id,
            nom="Admin",
            prenom="Système",
            titre="Administrateur"
        )
        db.session.add(admin_responsable)
        
        # Create sample students
        students_data = [
            ("Dupont", "Jean", "jean.dupont@example.com", "E001", 1, 1),
            ("Martin", "Marie", "marie.martin@example.com", "E002", 1, 1),
            ("Bernard", "Pierre", "pierre.bernard@example.com", "E003", 2, 1),
            ("Dubois", "Sophie", "sophie.dubois@example.com", "E004", 2, 1),
            ("Moreau", "Luc", "luc.moreau@example.com", "E005", 3, 1),
            ("Laurent", "Emma", "emma.laurent@example.com", "E006", 3, 1),
            ("Simon", "Paul", "paul.simon@example.com", "E007", 4, 1),
            ("Michel", "Julie", "julie.michel@example.com", "E008", 4, 1)
        ]
        
        etudiants = []
        for nom, prenom, email, numero, specialite_id, annee_id in students_data:
            user = User(email=email, role="etudiant")
            user.set_password("password123")
            db.session.add(user)
            db.session.flush()
            
            etudiant = Etudiant(
                user_id=user.id,
                nom=nom,
                prenom=prenom,
                numero_etudiant=numero,
                specialite_id=specialite_id,
                annee_id=annee_id
            )
            etudiants.append(etudiant)
            db.session.add(etudiant)
        
        # Create sample responsables
        responsables_data = [
            ("Professeur", "Alice", "alice.prof@example.com", "Professeure"),
            ("Directeur", "Bob", "bob.directeur@example.com", "Directeur des études")
        ]
        
        for nom, prenom, email, titre in responsables_data:
            user = User(email=email, role="responsable")
            user.set_password("password123")
            db.session.add(user)
            db.session.flush()
            
            responsable = Responsable(
                user_id=user.id,
                nom=nom,
                prenom=prenom,
                titre=titre
            )
            db.session.add(responsable)
        
        db.session.commit()
        
        # Create sample absences
        for etudiant in etudiants:
            for _ in range(random.randint(2, 8)):
                module = random.choice(modules)
                absence_date = date(2024, random.randint(1, 12), random.randint(1, 28))
                heure_debut = time(random.randint(8, 16), 0)
                heure_fin = time(heure_debut.hour + random.randint(1, 3), 0)
                
                statut = random.choice(['non_justifiee', 'en_attente', 'justifiee', 'refusee'])
                
                absence = Absence(
                    etudiant_id=etudiant.id,
                    module_id=module.id,
                    date=absence_date,
                    heure_debut=heure_debut,
                    heure_fin=heure_fin,
                    statut=statut
                )
                
                if statut == 'refusee':
                    absence.commentaire = "Justificatif insuffisant"
                
                db.session.add(absence)
        
        db.session.commit()
        print("Base de données initialisée avec succès!")

if __name__ == "__main__":
    seed_database()
