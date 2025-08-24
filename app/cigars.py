from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_from_directory, current_app
from sqlalchemy import or_, func
from app.models import db, User, Cigar
from app.utils import login_required, handle_file_upload, delete_file
from app.config import Config

cigars = Blueprint('cigars', __name__)

@cigars.route("/")
@login_required
def index():
    search_query = request.args.get("search", "").strip()
    sort_column = request.args.get("sort", "").strip()
    cigars_query = Cigar.query.filter_by(user_id=session["user_id"])

    if search_query:
        cigars_query = cigars_query.filter(
            or_(
                Cigar.name.ilike(f"%{search_query}%"),
                Cigar.purchase_location.ilike(f"%{search_query}%"),
                Cigar.origin_country.ilike(f"%{search_query}%")
            )
        )

    sort_options = {
        "name": Cigar.name,
        "price": Cigar.price,
        "purchase_location": Cigar.purchase_location,
        "origin_country": Cigar.origin_country,
        "rating": Cigar.rating.desc()  # Hoogste beoordeling eerst
    }
    if sort_column in sort_options:
        cigars_query = cigars_query.order_by(sort_options[sort_column])

    cigars_list = cigars_query.all()
    return render_template("index.html", cigars=cigars_list, sort=sort_column, 
                         is_admin=(session.get("username") == Config.ADMIN_USERNAME))

@cigars.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)

@cigars.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        try:
            name = request.form.get("name")
            rating = int(request.form.get("rating"))
            origin_country = request.form.get("origin_country")
            purchase_location = request.form.get("purchase_location")
            price = float(request.form.get("price") or 0.0)
            remarks = request.form.get("remarks") 

            image_file = request.files.get("image")
            image_filename = handle_file_upload(image_file, current_app.config["UPLOAD_FOLDER"])

            new_cigar = Cigar(
                name=name,
                rating=rating,
                origin_country=origin_country,
                purchase_location=purchase_location,
                price=price,
                remarks=remarks, 
                image_filename=image_filename,
                user_id=session["user_id"]
            )
            db.session.add(new_cigar)
            db.session.commit()
            flash("Sigaar toegevoegd!", "success")
            return redirect(url_for("cigars.index"))
        except Exception as e:
            flash(f"Fout bij toevoegen: {e}", "danger")
            return redirect(url_for("cigars.add"))

    return render_template("add.html")

@cigars.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    cigar = Cigar.query.filter_by(id=id, user_id=session["user_id"]).first_or_404()

    if request.method == "POST":
        cigar.name = request.form["name"]
        cigar.rating = int(request.form["rating"])
        cigar.origin_country = request.form.get("origin_country")
        cigar.purchase_location = request.form.get("purchase_location")
        cigar.price = float(request.form.get("price") or 0.0)
        cigar.remarks = request.form.get("remarks")

        image_file = request.files.get("image")
        if image_file and image_file.filename:
            # Verwijder oude foto
            if cigar.image_filename:
                delete_file(cigar.image_filename, current_app.config["UPLOAD_FOLDER"])
            
            # Upload nieuwe foto
            cigar.image_filename = handle_file_upload(image_file, current_app.config["UPLOAD_FOLDER"])

        db.session.commit()
        flash("Sigaar bijgewerkt!", "success")
        return redirect(url_for("cigars.index"))

    return render_template("edit.html", cigar=cigar)

@cigars.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):
    cigar = Cigar.query.filter_by(id=id, user_id=session["user_id"]).first_or_404()

    if cigar.image_filename:
        delete_file(cigar.image_filename, current_app.config["UPLOAD_FOLDER"])

    db.session.delete(cigar)
    db.session.commit()
    flash("Sigaar verwijderd.", "success")
    return redirect(url_for("cigars.index"))

@cigars.route("/account")
@login_required
def account():
    user = User.query.get(session["user_id"])

    cigar_count = Cigar.query.filter_by(user_id=user.id).count()

    total_value = db.session.query(func.sum(Cigar.price))\
        .filter_by(user_id=user.id).scalar() or 0

    most_common_location = db.session.query(
        Cigar.purchase_location,
        func.count(Cigar.purchase_location).label("loc_count")
    ).filter_by(user_id=user.id)\
     .group_by(Cigar.purchase_location)\
     .order_by(func.count(Cigar.purchase_location).desc())\
     .first()

    return render_template("account.html",
                           user=user,
                           cigar_count=cigar_count,
                           total_value=total_value,
                           most_common_location=most_common_location[0] if most_common_location else None)
