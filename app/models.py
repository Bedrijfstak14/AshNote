from datetime import datetime, timezone


def _utcnow():
    return datetime.now(timezone.utc)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

CIGAR_STATUSES = {
    "in_stock": "In voorraad",
    "smoked": "Gerookt",
    "gifted": "Weggegeven",
}

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
    status = db.Column(db.String(20), nullable=False, default="in_stock")
    created_at = db.Column(db.DateTime, nullable=False, default=_utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=_utcnow, onupdate=_utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
