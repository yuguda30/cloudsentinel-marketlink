from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    user_type = db.Column(db.String(30), nullable=False, default="buyer")
    is_active_account = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    listings = db.relationship(
        "Listing",
        backref="seller",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"


class Listing(db.Model):
    __tablename__ = "listings"

    id = db.Column(db.Integer, primary_key=True)

    seller_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    title = db.Column(db.String(180), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    condition = db.Column(db.String(80), nullable=False)

    price = db.Column(db.Float, nullable=False)

    state = db.Column(db.String(80), nullable=False)
    lga = db.Column(db.String(120), nullable=False)

    description = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(255), nullable=False)

    contact_phone = db.Column(db.String(20), nullable=False)
    whatsapp_number = db.Column(db.String(20), nullable=True)

    status = db.Column(db.String(20), default="active", nullable=False)
    views = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def mark_as_sold(self):
        self.status = "sold"

    def is_active_listing(self):
        return self.status == "active"

    def __repr__(self):
        return f"<Listing {self.title}>"

class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)

    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey("listings.id"), nullable=False)

    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship("User", foreign_keys=[sender_id], backref="sent_messages")
    receiver = db.relationship("User", foreign_keys=[receiver_id], backref="received_messages")
    listing = db.relationship("Listing", backref="messages")

    def __repr__(self):
        return f"<Message {self.id}>"
