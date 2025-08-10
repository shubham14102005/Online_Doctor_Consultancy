# 🩺 Doctor Consultation Platform

A Django-based web application for online doctor consultations, prescription generation, and patient history management.

## 📌 Features

### **For Patients**
- User registration and login
- Book appointments with doctors
- View appointment history
- Access past prescriptions

### **For Doctors**
- View and manage patient appointments
- Create new prescriptions
- Access patient medical history
- Search prescriptions by name or price

### **General**
- Secure authentication system
- User-friendly UI with Bootstrap
- Search system for quick access to prescriptions and records

---

## 🛠 Tech Stack

- **Backend:** Django, Python
- **Database:** SQLite (default, can be switched to MySQL/PostgreSQL)
- **Frontend:** HTML, CSS, Bootstrap
- **Authentication:** Django's built-in auth doctor_consultation/


## 📂 Project Structure

├── core/ # Main application logic
├── doctor_consultation/ # Project settings
├── templates/ # HTML templates
├── db.sqlite3 # Database file (SQLite)
├── manage.py # Django management script
└── LICENSEsystem

## 🚀 Getting Started

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/shubham14102005/doctor_consultation.git
cd doctor_consultation
2️⃣ Create Virtual Environment
python -m venv env
source env/bin/activate   # On Windows: env\Scripts\activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Run Migrations
python manage.py makemigrations
python manage.py migrate
5️⃣ Create Superuser
python manage.py createsuperuser
6️⃣ Run the Server
python manage.py runserver
Access the application at: http://127.0.0.1:8000/

