# Student Absence Manager

A web application for managing student absences, justifications, and notifications (in-app and email) for educational institutions.

---

## Features

* Student absence recording and justification
* Role-based access (admin/responsable, student)
* Email notifications for absences and justifications
* In-app notifications
* Admin dashboard

---

## Prerequisites

* Python 3.8+
* MySQL server (or compatible)
* [pip](https://pip.pypa.io/en/stable/)
* (Optional) [virtualenv](https://virtualenv.pypa.io/en/latest/)

---

## Installation on a New Machine (Best Practices)

### 1. Clone the repository

```bash
git clone https://github.com/Sidi-ballahi/gestion_absences.git
cd student-absence-manager
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the database

* Make sure MySQL is running.
* Create a database named `gestion_absences` .

```sql
CREATE DATABASE gestion_absences CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```



### 5. Configure mail settings

By default, the app uses Gmail SMTP. You can set the values directly in `config.py` or use a `.env` file.

```python
MAIL_USERNAME = 'gdesabsences@gmail.com'
MAIL_PASSWORD = 'wxcr wmsy bjzi ncmb'  # Gmail app password
MAIL_DEFAULT_SENDER = 'gdesabsences@gmail.com'
```

Or use environment variables in a `.env` file:

```
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=your_email@gmail.com
```

### 6. Initialize the database with Flask-Migrate

#### ✅ Si vous êtes sur un nouveau PC et que le dossier `migrations/` existe déjà :

```bash
flask db upgrade
```

#### 🛠️ Si le dossier `migrations/` n'existe pas :

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 7. Create admin or test users

 run:

```bash
python create_admin.py
```

### 8. Run the application

```bash
flask run
```

Access the app at [http://localhost:5000](http://localhost:5000).

---

## Test Email (optional)



## Default Admin Credentials

* **Email:** `admin@esp.mr`
* **Password:** `admin123`

---

## Notes

* Never commit real passwords to public repositories.
* Use `.env` and load it with `python-dotenv` if needed.
* Always test mail and login features locally before going to production.

---

## License

MIT License
