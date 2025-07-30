import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from sqlalchemy import or_
import requests


load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "geheim")

UPLOAD_FOLDER = os.path.join("data", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////app/data/cigars.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Cigar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    origin_country = db.Column(db.String(100))
    purchase_location = db.Column(db.String(100))
    price = db.Column(db.Float)
    image_filename = db.Column(db.String(255))
    remarks = db.Column(db.Text) 
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))

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
        "origin_country": Cigar.origin_country
    }
    if sort_column in sort_options:
        cigars_query = cigars_query.order_by(sort_options[sort_column])

    cigars = cigars_query.all()
    return render_template("index.html", cigars=cigars, sort=sort_column, is_admin=(session.get("username") == ADMIN_USERNAME))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session["user"] = user.username
            session["username"] = user.username
            session["user_id"] = user.id
            flash("Succesvol ingelogd!", "success")
            return redirect(url_for("index"))
        else:
            flash("Ongeldige inloggegevens", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if User.query.filter_by(username=username).first():
            flash("Gebruikersnaam bestaat al.", "warning")
            return redirect(url_for("register"))
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Registratie gelukt. Je kunt nu inloggen.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/admin")
def admin():
    if "user_id" not in session:
        return redirect(url_for("login"))

    current_user = User.query.get(session["user_id"])
    if current_user.username != ADMIN_USERNAME:
        flash("Je hebt geen toegang tot de beheerderspagina.", "danger")
        return redirect(url_for("index"))

    users = User.query.all()
    return render_template("admin.html", users=users)


@app.route("/admin/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    current_user = User.query.get(session["user_id"])
    if current_user.username != ADMIN_USERNAME:
        flash("Geen toestemming", "danger")
        return redirect(url_for("index"))

    if user_id == current_user.id:
        flash("Je kunt jezelf niet verwijderen.", "warning")
        return redirect(url_for("admin"))

    user = User.query.get_or_404(user_id)
    Cigar.query.filter_by(user_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    flash("Gebruiker verwijderd.", "success")
    return redirect(url_for("admin"))

@app.route("/admin/reset_password/<int:user_id>", methods=["GET", "POST"])
def admin_reset_password(user_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    current_user = User.query.get(session["user_id"])
    if current_user.username != ADMIN_USERNAME:
        flash("Geen toegang tot deze pagina.", "danger")
        return redirect(url_for("index"))

    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if new_password != confirm_password:
            flash("Wachtwoorden komen niet overeen.", "warning")
            return redirect(url_for("admin_reset_password", user_id=user.id))

        user.set_password(new_password)
        db.session.commit()
        flash(f"Wachtwoord voor gebruiker '{user.username}' is gewijzigd.", "success")
        return redirect(url_for("admin"))

    return render_template("admin_reset_password.html", user=user)

@app.context_processor
def inject_is_admin():
    return {
        "is_admin": session.get("username") == ADMIN_USERNAME
    }

@app.route("/add", methods=["GET", "POST"])
def add():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        try:
            name = request.form.get("name")
            rating = int(request.form.get("rating"))
            origin_country = request.form.get("origin_country")
            purchase_location = request.form.get("purchase_location")
            price = float(request.form.get("price") or 0.0)
            remarks = request.form.get("remarks") 

            image_file = request.files.get("image")
            image_filename = None
            if image_file and image_file.filename != "":
                filename = secure_filename(image_file.filename)
                image_file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                image_filename = filename

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
            return redirect(url_for("index"))
        except Exception as e:
            flash(f"Fout bij toevoegen: {e}", "danger")
            return redirect(url_for("add"))

    return render_template("add.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if "user_id" not in session:
        return redirect(url_for("login"))

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
            if cigar.image_filename:
                old_path = os.path.join(app.config["UPLOAD_FOLDER"], cigar.image_filename)
                if os.path.exists(old_path):
                    os.remove(old_path)
            filename = secure_filename(image_file.filename)
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image_file.save(path)
            cigar.image_filename = filename

        db.session.commit()
        flash("Sigaar bijgewerkt!", "success")
        return redirect(url_for("index"))

    return render_template("edit.html", cigar=cigar)

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    cigar = Cigar.query.filter_by(id=id, user_id=session["user_id"]).first_or_404()

    if cigar.image_filename:
        path = os.path.join(app.config["UPLOAD_FOLDER"], cigar.image_filename)
        if os.path.exists(path):
            os.remove(path)

    db.session.delete(cigar)
    db.session.commit()
    flash("Sigaar verwijderd.", "success")
    return redirect(url_for("index"))

from sqlalchemy import func

@app.route("/account")
def account():
    if "user_id" not in session:
        return redirect(url_for("login"))

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

@app.route("/change-password", methods=["GET", "POST"])
def change_password():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    if request.method == "POST":
        current = request.form.get("current_password")
        new = request.form.get("new_password")
        confirm = request.form.get("confirm_password")

        if not check_password_hash(user.password_hash, current):
            flash("Huidig wachtwoord klopt niet.", "danger")
            return redirect(url_for("change_password"))

        if new != confirm:
            flash("Nieuwe wachtwoorden komen niet overeen.", "danger")
            return redirect(url_for("change_password"))

        user.password_hash = generate_password_hash(new)
        db.session.commit()
        flash("Wachtwoord succesvol gewijzigd.", "success")
        return redirect(url_for("account"))

    return render_template("change_password.html")

@app.route("/api/search_cigar")
def api_search_cigar():
    name = request.args.get("name", "").strip()
    if not name:
        return jsonify([])

    url = "https://cigars.p.rapidapi.com/cigars"
    headers = {
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
        "x-rapidapi-host": os.getenv("RAPIDAPI_HOST", "cigars.p.rapidapi.com")
    }
    params = {"page": "1", "name": name}

    try:
        response = requests.get(url, headers=headers, params=params)
        print("RESPONSETEXT =", response.text)  # optioneel weer verwijderen
        response.raise_for_status()
        return jsonify(response.json().get("cigars", []))
    except requests.RequestException as e:
        logging.error("API FOUT: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/logout")
def logout():
    session.clear()
    flash("Je bent uitgelogd.", "info")
    return redirect(url_for("login"))
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=8000)

