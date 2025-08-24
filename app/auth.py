from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import db, User
from app.utils import login_required

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session["user"] = user.username
            session["username"] = user.username
            session["user_id"] = user.id
            flash("Succesvol ingelogd!", "success")
            return redirect(url_for("cigars.index"))
        else:
            flash("Ongeldige inloggegevens", "danger")
            return redirect(url_for("auth.login"))

    return render_template("login.html")

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if User.query.filter_by(username=username).first():
            flash("Gebruikersnaam bestaat al.", "warning")
            return redirect(url_for("auth.register"))
            
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Registratie gelukt. Je kunt nu inloggen.", "success")
        return redirect(url_for("auth.login"))
        
    return render_template("register.html")

@auth.route("/logout")
def logout():
    session.clear()
    flash("Je bent uitgelogd.", "info")
    return redirect(url_for("auth.login"))

@auth.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    user = User.query.get(session["user_id"])

    if request.method == "POST":
        current = request.form.get("current_password")
        new = request.form.get("new_password")
        confirm = request.form.get("confirm_password")

        if not user.check_password(current):
            flash("Huidig wachtwoord klopt niet.", "danger")
            return redirect(url_for("auth.change_password"))

        if new != confirm:
            flash("Nieuwe wachtwoorden komen niet overeen.", "danger")
            return redirect(url_for("auth.change_password"))

        user.set_password(new)
        db.session.commit()
        flash("Wachtwoord succesvol gewijzigd.", "success")
        return redirect(url_for("cigars.account"))

    return render_template("change_password.html")
