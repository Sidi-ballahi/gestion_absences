from app import create_app
from app.models.models import db, Etudiant, User
from flask import Flask

# Crée l'application avec le contexte Flask
app = create_app()

with app.app_context():
    # Remplace par l'email de ton utilisateur étudiant
    email = "etudiant@test.com"

    # Recherche de l'utilisateur
    user = User.query.filter_by(email=email).first()

    if user:
        if user.etudiant:
            print("⚠️ Cet utilisateur a déjà une fiche Étudiant.")
        else:
            etudiant = Etudiant(
                nom="Ali",
                prenom="Ahmed",
                numero_etudiant="ETU001",
                specialite_id=None,  # Mets l'ID d'une spécialité si elle existe
                annee_id=None,       # Mets l'ID d'une année si elle existe
                user_id=user.id
            )
            db.session.add(etudiant)
            db.session.commit()
            print("✅ Fiche Étudiant créée et liée à l'utilisateur.")
    else:
        print("❌ Utilisateur non trouvé.")
