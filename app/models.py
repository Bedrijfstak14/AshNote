from datetime import datetime, date, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


def _utcnow():
    return datetime.now(timezone.utc)

db = SQLAlchemy()

CIGAR_STATUSES = {
    "in_stock": "In voorraad",
    "smoking": "Aan het roken",
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
    rating = db.Column(db.Integer, nullable=True)
    origin_country = db.Column(db.String(100))
    purchase_location = db.Column(db.String(100))
    cigar_type = db.Column(db.String(100))
    price = db.Column(db.Float)
    image_filename = db.Column(db.String(255))
    remarks = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False, default="in_stock")
    created_at = db.Column(db.DateTime, nullable=False, default=_utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=_utcnow, onupdate=_utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    smoke_events = db.relationship("SmokeEvent", backref="cigar", lazy=True,
                                   cascade="all, delete-orphan", order_by="SmokeEvent.smoked_at.desc()")


class SmokeEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cigar_id = db.Column(db.Integer, db.ForeignKey("cigar.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    smoked_at = db.Column(db.Date, nullable=False, default=date.today)
    location = db.Column(db.String(100))
    notes = db.Column(db.Text)
