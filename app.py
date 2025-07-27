import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# .env laden
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  # ✔️ geladen uit .env

# SQLite locatie
DB_DIR = "/tmp/cigars_data"
os.makedirs(DB_DIR, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/cigars_data/cigars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Cigar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    origin_country = db.Column(db.String(100))
    purchase_location = db.Column(db.String(100))
    price = db.Column(db.Float)

@app.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("login"))

    cigars = Cigar.query.all()
    return render_template("index.html", cigars=cigars)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        try:
            name = request.form.get("name")
            rating = int(request.form.get("rating"))
            origin_country = request.form.get("origin_country")
            purchase_location = request.form.get("purchase_location")
            price = float(request.form.get("price") or 0.0)

            new_cigar = Cigar(
                name=name,
                rating=rating,
                origin_country=origin_country,
                purchase_location=purchase_location,
                price=price
            )
            db.session.add(new_cigar)
            db.session.commit()
            flash("Sigaar toegevoegd!", "success")
            return redirect(url_for("index"))
        except Exception as e:
            flash(f"Fout bij toevoegen: {e}", "danger")
            return redirect(url_for("add"))

    return render_template("add.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if (username == os.getenv("LOGIN_USER") and
                password == os.getenv("LOGIN_PASS")):
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

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    if "user" not in session:
        return redirect(url_for("login"))

    cigar = Cigar.query.get_or_404(id)
    db.session.delete(cigar)
    db.session.commit()
    flash("Sigaar verwijderd.", "success")
    return redirect(url_for("index"))

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

            db.session.commit()
            flash("Sigaar bijgewerkt!", "success")
            return redirect(url_for("index"))
        except Exception as e:
            flash(f"Fout bij bijwerken: {e}", "danger")
            return redirect(url_for("edit", id=id))

    return render_template("edit.html", cigar=cigar)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=8000)
