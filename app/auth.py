import logging
import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import db, User
from app.utils import login_required
from app.extensions import limiter

logger = logging.getLogger(__name__)

auth = Blueprint("auth", __name__)

MIN_PASSWORD_LENGTH = 8
USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_]{3,50}$")


def _validate_username(username):
    if not username or not USERNAME_PATTERN.match(username):
        return "Gebruikersnaam moet 3–50 tekens zijn (letters, cijfers, underscore)."
    return None


def _validate_password(password):
    if not password or len(password) < MIN_PASSWORD_LENGTH:
        return f"Wachtwoord moet minimaal {MIN_PASSWORD_LENGTH} tekens lang zijn."
    return None


@auth.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per minute")
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session.clear()  # Voorkom session fixation
            session["user"] = user.username
            session["username"] = user.username
            session["user_id"] = user.id
            logger.info("Gebruiker '%s' ingelogd.", username)
            flash("Succesvol ingelogd!", "success")
            return redirect(url_for("cigars.index"))

        logger.warning("Mislukte loginpoging voor gebruikersnaam '%s'.", username)
        flash("Ongeldige inloggegevens.", "danger")
        return redirect(url_for("auth.login"))

    return render_template("login.html")


@auth.route("/register", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        error = _validate_username(username)
        if error:
            flash(error, "warning")
            return redirect(url_for("auth.register"))

        error = _validate_password(password)
        if error:
            flash(error, "warning")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(username=username).first():
            flash("Gebruikersnaam bestaat al.", "warning")
            return redirect(url_for("auth.register"))

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        logger.info("Nieuw account aangemaakt: '%s'.", username)
        flash("Registratie gelukt. Je kunt nu inloggen.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth.route("/logout")
def logout():
    username = session.get("username", "onbekend")
    session.clear()
    logger.info("Gebruiker '%s' uitgelogd.", username)
    flash("Je bent uitgelogd.", "info")
    return redirect(url_for("auth.login"))


@auth.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    user = db.session.get(User, session["user_id"])

    if request.method == "POST":
        current = request.form.get("current_password", "")
        new = request.form.get("new_password", "")
        confirm = request.form.get("confirm_password", "")

        if not user.check_password(current):
            flash("Huidig wachtwoord klopt niet.", "danger")
            return redirect(url_for("auth.change_password"))

        error = _validate_password(new)
        if error:
            flash(error, "warning")
            return redirect(url_for("auth.change_password"))

        if new != confirm:
            flash("Nieuwe wachtwoorden komen niet overeen.", "danger")
            return redirect(url_for("auth.change_password"))

        user.set_password(new)
        db.session.commit()
        logger.info("Wachtwoord gewijzigd voor '%s'.", user.username)
        flash("Wachtwoord succesvol gewijzigd.", "success")
        return redirect(url_for("cigars.account"))

    return render_template("change_password.html")
