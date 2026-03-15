import csv
import io
import logging
from flask import (
    Blueprint, render_template, request, redirect, url_for,
    flash, session, send_from_directory, current_app, Response,
)
from sqlalchemy import or_, func
from app.models import db, User, Cigar, CIGAR_STATUSES
from app.utils import login_required, handle_file_upload, delete_file
from app.config import Config

logger = logging.getLogger(__name__)

cigars = Blueprint("cigars", __name__)

PER_PAGE = 20


def _validate_cigar_form(form):
    """Valideer sigaarformulier-invoer.

    Geeft ((name, rating, origin_country, purchase_location, price, remarks), None)
    bij succes, of (None, foutmelding) bij fout.
    """
    name = form.get("name", "").strip()
    if not name:
        return None, "Naam is verplicht."
    if len(name) > 100:
        return None, "Naam mag maximaal 100 tekens zijn."

    try:
        rating = int(form.get("rating", 0))
        if not (1 <= rating <= 10):
            raise ValueError
    except (ValueError, TypeError):
        return None, "Beoordeling moet een geheel getal tussen 1 en 10 zijn."

    try:
        price = float(form.get("price") or 0)
        if price < 0 or price > 100_000:
            raise ValueError
    except (ValueError, TypeError):
        return None, "Prijs moet een geldig getal zijn (0 – 100.000)."

    origin_country = (form.get("origin_country") or "").strip()[:100]
    purchase_location = (form.get("purchase_location") or "").strip()[:100]
    remarks = (form.get("remarks") or "").strip()

    status = form.get("status", "in_stock")
    if status not in CIGAR_STATUSES:
        status = "in_stock"

    return (name, rating, origin_country, purchase_location, price, remarks, status), None


@cigars.route("/")
@login_required
def index():
    search_query = request.args.get("search", "").strip()
    sort_column = request.args.get("sort", "").strip()
    filter_status = request.args.get("status", "").strip()
    min_rating = request.args.get("min_rating", "", type=str).strip()
    page = request.args.get("page", 1, type=int)

    cigars_query = Cigar.query.filter_by(user_id=session["user_id"])

    if search_query:
        cigars_query = cigars_query.filter(
            or_(
                Cigar.name.ilike(f"%{search_query}%"),
                Cigar.purchase_location.ilike(f"%{search_query}%"),
                Cigar.origin_country.ilike(f"%{search_query}%"),
            )
        )

    if filter_status in CIGAR_STATUSES:
        cigars_query = cigars_query.filter(Cigar.status == filter_status)

    if min_rating.isdigit():
        min_r = int(min_rating)
        if 1 <= min_r <= 10:
            cigars_query = cigars_query.filter(Cigar.rating >= min_r)

    sort_options = {
        "name": Cigar.name,
        "price": Cigar.price,
        "purchase_location": Cigar.purchase_location,
        "origin_country": Cigar.origin_country,
        "rating": Cigar.rating.desc(),
        "created_at": Cigar.created_at.desc(),
    }
    if sort_column in sort_options:
        cigars_query = cigars_query.order_by(sort_options[sort_column])

    pagination = cigars_query.paginate(page=page, per_page=PER_PAGE, error_out=False)

    return render_template(
        "index.html",
        cigars=pagination.items,
        pagination=pagination,
        sort=sort_column,
        filter_status=filter_status,
        min_rating=min_rating,
        cigar_statuses=CIGAR_STATUSES,
        is_admin=(session.get("username") == Config.ADMIN_USERNAME),
    )


@cigars.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)


@cigars.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        fields, error = _validate_cigar_form(request.form)
        if error:
            flash(error, "warning")
            return redirect(url_for("cigars.add"))

        name, rating, origin_country, purchase_location, price, remarks, status = fields

        try:
            image_file = request.files.get("image")
            image_filename, upload_error = handle_file_upload(
                image_file, current_app.config["UPLOAD_FOLDER"]
            )
            if upload_error:
                flash(upload_error, "warning")
                return redirect(url_for("cigars.add"))

            new_cigar = Cigar(
                name=name,
                rating=rating,
                origin_country=origin_country,
                purchase_location=purchase_location,
                price=price,
                remarks=remarks,
                status=status,
                image_filename=image_filename,
                user_id=session["user_id"],
            )
            db.session.add(new_cigar)
            db.session.commit()
            logger.info("Sigaar '%s' toegevoegd door user_id=%s.", name, session["user_id"])
            flash("Sigaar toegevoegd!", "success")
            return redirect(url_for("cigars.index"))
        except Exception:
            logger.exception("Fout bij toevoegen sigaar door user_id=%s.", session.get("user_id"))
            flash("Er is een onverwachte fout opgetreden. Probeer het opnieuw.", "danger")
            return redirect(url_for("cigars.add"))

    return render_template("add.html")


@cigars.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    cigar = Cigar.query.filter_by(id=id, user_id=session["user_id"]).first_or_404()

    if request.method == "POST":
        fields, error = _validate_cigar_form(request.form)
        if error:
            flash(error, "warning")
            return redirect(url_for("cigars.edit", id=id))

        name, rating, origin_country, purchase_location, price, remarks, status = fields

        cigar.name = name
        cigar.rating = rating
        cigar.origin_country = origin_country
        cigar.purchase_location = purchase_location
        cigar.price = price
        cigar.remarks = remarks
        cigar.status = status

        image_file = request.files.get("image")
        if image_file and image_file.filename:
            if cigar.image_filename:
                delete_file(cigar.image_filename, current_app.config["UPLOAD_FOLDER"])
            new_filename, upload_error = handle_file_upload(
                image_file, current_app.config["UPLOAD_FOLDER"]
            )
            if upload_error:
                flash(upload_error, "warning")
                return redirect(url_for("cigars.edit", id=id))
            cigar.image_filename = new_filename

        db.session.commit()
        logger.info("Sigaar id=%s bijgewerkt door user_id=%s.", id, session["user_id"])
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
    logger.info("Sigaar id=%s verwijderd door user_id=%s.", id, session["user_id"])
    flash("Sigaar verwijderd.", "success")
    return redirect(url_for("cigars.index"))


@cigars.route("/account")
@login_required
def account():
    user = db.session.get(User, session["user_id"])
    uid = user.id

    cigar_count = Cigar.query.filter_by(user_id=uid).count()

    total_value = (
        db.session.query(func.sum(Cigar.price)).filter_by(user_id=uid).scalar() or 0
    )

    avg_rating = (
        db.session.query(func.avg(Cigar.rating)).filter_by(user_id=uid).scalar()
    )
    avg_rating = round(avg_rating, 1) if avg_rating else None

    most_common_location = (
        db.session.query(
            Cigar.purchase_location,
            func.count(Cigar.purchase_location).label("loc_count"),
        )
        .filter(Cigar.user_id == uid, Cigar.purchase_location.isnot(None), Cigar.purchase_location != "")
        .group_by(Cigar.purchase_location)
        .order_by(func.count(Cigar.purchase_location).desc())
        .first()
    )

    # Verdeling per status
    status_rows = (
        db.session.query(Cigar.status, func.count(Cigar.id))
        .filter_by(user_id=uid)
        .group_by(Cigar.status)
        .all()
    )
    status_counts = {row[0]: row[1] for row in status_rows}

    # Rating verdeling (1-10)
    rating_rows = (
        db.session.query(Cigar.rating, func.count(Cigar.id))
        .filter_by(user_id=uid)
        .group_by(Cigar.rating)
        .order_by(Cigar.rating)
        .all()
    )
    rating_distribution = {str(r): c for r, c in rating_rows}

    # Top 5 landen
    country_rows = (
        db.session.query(Cigar.origin_country, func.count(Cigar.id).label("cnt"))
        .filter(Cigar.user_id == uid, Cigar.origin_country.isnot(None), Cigar.origin_country != "")
        .group_by(Cigar.origin_country)
        .order_by(func.count(Cigar.id).desc())
        .limit(5)
        .all()
    )

    return render_template(
        "account.html",
        user=user,
        cigar_count=cigar_count,
        total_value=total_value,
        avg_rating=avg_rating,
        most_common_location=most_common_location[0] if most_common_location else None,
        status_counts=status_counts,
        rating_distribution=rating_distribution,
        country_rows=country_rows,
        cigar_statuses=CIGAR_STATUSES,
    )


@cigars.route("/export/csv")
@login_required
def export_csv():
    user_cigars = (
        Cigar.query.filter_by(user_id=session["user_id"])
        .order_by(Cigar.name)
        .all()
    )
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Naam", "Beoordeling", "Status", "Land van herkomst",
        "Aankooplocatie", "Prijs (€)", "Opmerkingen", "Toegevoegd op",
    ])
    for c in user_cigars:
        writer.writerow([
            c.name,
            c.rating,
            CIGAR_STATUSES.get(c.status, c.status),
            c.origin_country or "",
            c.purchase_location or "",
            f"{c.price:.2f}" if c.price else "",
            c.remarks or "",
            c.created_at.strftime("%Y-%m-%d"),
        ])
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment; filename=sigaren.csv"},
    )
