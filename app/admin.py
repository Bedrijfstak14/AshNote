import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from sqlalchemy import func
from app.models import db, User, Cigar
from app.utils import admin_required

logger = logging.getLogger(__name__)

admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route("/")
@admin_required
def admin_panel():
    users_with_counts = (
        db.session.query(User, func.count(Cigar.id).label("cigar_count"))
        .outerjoin(Cigar, User.id == Cigar.user_id)
        .group_by(User.id)
        .order_by(User.username)
        .all()
    )
    return render_template("admin.html", users_with_counts=users_with_counts)


@admin.route("/delete_user/<int:user_id>", methods=["POST"])
@admin_required
def delete_user(user_id):
    current_user = db.session.get(User, session["user_id"])

    if user_id == current_user.id:
        flash("Je kunt jezelf niet verwijderen.", "warning")
        return redirect(url_for("admin.admin_panel"))

    user = User.query.get_or_404(user_id)
    username = user.username
    Cigar.query.filter_by(user_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    logger.info("Admin verwijderde gebruiker '%s' (id=%s).", username, user_id)
    flash("Gebruiker verwijderd.", "success")
    return redirect(url_for("admin.admin_panel"))


@admin.route("/reset_password/<int:user_id>", methods=["GET", "POST"])
@admin_required
def admin_reset_password(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_password", "")

        if len(new_password) < 8:
            flash("Wachtwoord moet minimaal 8 tekens lang zijn.", "warning")
            return redirect(url_for("admin.admin_reset_password", user_id=user.id))

        if new_password != confirm_password:
            flash("Wachtwoorden komen niet overeen.", "warning")
            return redirect(url_for("admin.admin_reset_password", user_id=user.id))

        user.set_password(new_password)
        db.session.commit()
        logger.info("Admin resette wachtwoord voor '%s' (id=%s).", user.username, user_id)
        flash(f"Wachtwoord voor gebruiker '{user.username}' is gewijzigd.", "success")
        return redirect(url_for("admin.admin_panel"))

    return render_template("admin_reset_password.html", user=user)
