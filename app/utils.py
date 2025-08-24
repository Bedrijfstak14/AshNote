import os
from functools import wraps
from flask import session, redirect, url_for, flash
from app.models import User
from app.config import Config

def login_required(f):
    """Decorator om in te loggen vereist te maken"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator om admin rechten vereist te maken"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        
        current_user = User.query.get(session["user_id"])
        if current_user.username != Config.ADMIN_USERNAME:
            flash("Je hebt geen toegang tot deze pagina.", "danger")
            return redirect(url_for("cigars.index"))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Haal de huidige gebruiker op"""
    if "user_id" in session:
        return User.query.get(session["user_id"])
    return None

def is_admin():
    """Check of de huidige gebruiker admin is"""
    current_user = get_current_user()
    if current_user:
        return current_user.username == Config.ADMIN_USERNAME
    return False

def handle_file_upload(file, upload_folder):
    """Helper functie voor bestand uploads"""
    from werkzeug.utils import secure_filename
    
    if file and file.filename != "":
        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_folder, filename))
        return filename
    return None

def delete_file(filename, upload_folder):
    """Helper functie voor bestand verwijdering"""
    if filename:
        path = os.path.join(upload_folder, filename)
        if os.path.exists(path):
            os.remove(path)
