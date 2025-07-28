import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# .env laden
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Upload- en databasepaden
UPLOAD_FOLDER = os.path.join("data", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////app/data/cigars.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Cigar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    origin_country = db.Column(db.String(100))
    purchase_location = db.Column(db.String(100))
    price = db.Column(db.Float)
    image_filename = db.Column(db.String(255))

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)



@app.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("login"))

    search_query = request.args.get("search", "").strip()
    sort_column = request.args.get("sort", "").strip()

    cigars_query = Cigar.query

    # Zoeken op naam
    if search_query:
        cigars_query = cigars_query.filter(
            or_(
                Cigar.name.ilike(f"%{search_query}%"),
                Cigar.purchase_location.ilike(f"%{search_query}%"),
                Cigar.origin_country.ilike(f"%{search_query}%")
            )
        )

    # Sorteerbare kolommen
    sort_options = {
        "name": Cigar.name,
        "price": Cigar.price,
        "purchase_location": Cigar.purchase_location,
        "origin_country": Cigar.origin_country
    }
    if sort_column in sort_options:
        cigars_query = cigars_query.order_by(sort_options[sort_column])

    cigars = cigars_query.all()
    show_images = any(c.image_filename for c in cigars)

    return render_template("index.html", cigars=cigars, show_images=show_images, sort=sort_column)

@app.route("/add", methods=["GET", "POST"])
def add():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        try:
            name = request.form.get("name")
            rating = int(request.form.get("rating"))
            origin_country = request.form.get("origin_country")
            purchase_location = request.form.get("purchase_location")
            price = float(request.form.get("price") or 0.0)

            image_file = request.files.get("image")
            image_filename = None
            if image_file and image_file.filename != "":
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                image_file.save(image_path)
                image_filename = filename

            new_cigar = Cigar(
                name=name,
                rating=rating,
                origin_country=origin_country,
                purchase_location=purchase_location,
                price=price,
                image_filename=image_filename
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
    if "user" not in session:
        return redirect(url_for("login"))

    cigar = Cigar.query.get_or_404(id)

    if request.method == "POST":
        try:
            cigar.name = request.form.get("name")
            cigar.rating = int(request.form.get("rating"))
            cigar.origin_country = request.form.get("origin_country")
            cigar.purchase_location = request.form.get("purchase_location")
            cigar.price = float(request.form.get("price") or 0.0)

            image_file = request.files.get("image")
            if image_file and image_file.filename != "":
                if cigar.image_filename:
                    old_path = os.path.join(app.config["UPLOAD_FOLDER"], cigar.image_filename)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                image_file.save(image_path)
                cigar.image_filename = filename

            db.session.commit()
            flash("Sigaar bijgewerkt!", "success")
            return redirect(url_for("index"))
        except Exception as e:
            flash(f"Fout bij bijwerken: {e}", "danger")
            return redirect(url_for("edit", id=id))

    return render_template("edit.html", cigar=cigar)

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    if "user" not in session:
        return redirect(url_for("login"))

    cigar = Cigar.query.get_or_404(id)
    if cigar.image_filename:
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], cigar.image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(cigar)
    db.session.commit()
    flash("Sigaar verwijderd.", "success")
    return redirect(url_for("index"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == os.getenv("LOGIN_USER") and password == os.getenv("LOGIN_PASS"):
            session["user"] = username
            flash("Succesvol ingelogd!", "success")
            return redirect(url_for("index"))
        else:
            flash("Ongeldige inloggegevens", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Je bent uitgelogd.", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=8000)
