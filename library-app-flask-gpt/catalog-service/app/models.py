import uuid
from datetime import datetime
from .extensions import db

def gen_uuid():
    return str(uuid.uuid4())

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.String, primary_key=True, default=gen_uuid)
    title = db.Column(db.String(512), nullable=False, index=True)
    author = db.Column(db.String(256), nullable=False, index=True)
    isbn = db.Column(db.String(64), unique=True, nullable=True, index=True)
    published_date = db.Column(db.Date, nullable=True)
    genre = db.Column(db.String(128), nullable=True, index=True)
    copies_total = db.Column(db.Integer, nullable=False, default=1)
    copies_available = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def is_available(self):
        return self.copies_available > 0

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "published_date": self.published_date.isoformat() if self.published_date else None,
            "genre": self.genre,
            "copies_total": self.copies_total,
            "copies_available": self.copies_available,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
