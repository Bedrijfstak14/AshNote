import os
import logging
from functools import wraps
from flask import session, redirect, url_for, flash
from app.models import User
from app.config import Config

logger = logging.getLogger(__name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        from app.models import db
        current_user = db.session.get(User, session["user_id"])
        if current_user.username != Config.ADMIN_USERNAME:
            flash("Je hebt geen toegang tot deze pagina.", "danger")
            return redirect(url_for("cigars.index"))
        return f(*args, **kwargs)
    return decorated_function


def get_current_user():
    if "user_id" in session:
        from app.models import db
        return db.session.get(User, session["user_id"])
    return None


def is_admin():
    current_user = get_current_user()
    if current_user:
        return current_user.username == Config.ADMIN_USERNAME
    return False


def _allowed_file(filename):
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in Config.ALLOWED_EXTENSIONS


def handle_file_upload(file, upload_folder):
    """Upload bestand na validatie van type en grootte.

    Geeft (filename, error_message) terug. Bij succes is error_message None.
    Bij geen bestand: (None, None).
    """
    from werkzeug.utils import secure_filename

    if not file or file.filename == "":
        return None, None

    if not _allowed_file(file.filename):
        allowed = ", ".join(sorted(Config.ALLOWED_EXTENSIONS))
        return None, f"Bestandstype niet toegestaan. Gebruik: {allowed}."

    # Controleer bestandsgrootte
    file.seek(0, 2)
    size = file.tell()
    file.seek(0)
    if size > Config.MAX_CONTENT_LENGTH:
        max_mb = Config.MAX_CONTENT_LENGTH // (1024 * 1024)
        return None, f"Bestand is te groot. Maximum is {max_mb} MB."

    filename = secure_filename(file.filename)
    file.save(os.path.join(upload_folder, filename))
    logger.info("Bestand '%s' geüpload.", filename)
    return filename, None


def delete_file(filename, upload_folder):
    if filename:
        path = os.path.join(upload_folder, filename)
        if os.path.exists(path):
            os.remove(path)
            logger.info("Bestand '%s' verwijderd.", filename)
