from app import create_app
from app.models.models import db, User
from werkzeug.security import generate_password_hash

# Crée l'application Flask
app = create_app()

# Crée les utilisateurs à l'intérieur du contexte de l'application
with app.app_context():
    # Vérifie s'ils existent déjà
    existing_admin = User.query.filter_by(email="admin@example.com").first()
   

    if not existing_admin:
        admin = User(
            email="admin@esp.mr",
            password_hash=generate_password_hash("admin123"),
            role="responsable"
        )
        db.session.add(admin)

    

    db.session.commit()
    print("✅ Utilisateurs créés avec succès (ou déjà existants).")
