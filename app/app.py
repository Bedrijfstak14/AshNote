from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cigars_data/cigars.db'
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
    cigars = Cigar.query.all()
    return render_template("index.html", cigars=cigars)

@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name")
    rating = int(request.form.get("rating"))
    origin_country = request.form.get("origin_country")
    purchase_location = request.form.get("purchase_location")
    price = float(request.form.get("price"))

    new_cigar = Cigar(
        name=name,
        rating=rating,
        origin_country=origin_country,
        purchase_location=purchase_location,
        price=price
    )
    db.session.add(new_cigar)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=8000)