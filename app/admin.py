from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import db, User, Cigar
from app.utils import admin_required

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route("/")
@admin_required
def admin_panel():
    users = User.query.all()
    return render_template("admin.html", users=users)

@admin.route("/delete_user/<int:user_id>", methods=["POST"])
@admin_required
def delete_user(user_id):
    current_user = User.query.get(session["user_id"])
    
    if user_id == current_user.id:
        flash("Je kunt jezelf niet verwijderen.", "warning")
        return redirect(url_for("admin.admin_panel"))

    user = User.query.get_or_404(user_id)
    Cigar.query.filter_by(user_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    flash("Gebruiker verwijderd.", "success")
    return redirect(url_for("admin.admin_panel"))

@admin.route("/reset_password/<int:user_id>", methods=["GET", "POST"])
@admin_required
def admin_reset_password(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if new_password != confirm_password:
            flash("Wachtwoorden komen niet overeen.", "warning")
            return redirect(url_for("admin.admin_reset_password", user_id=user.id))

        user.set_password(new_password)
        db.session.commit()
        flash(f"Wachtwoord voor gebruiker '{user.username}' is gewijzigd.", "success")
        return redirect(url_for("admin.admin_panel"))

    return render_template("admin_reset_password.html", user=user)
