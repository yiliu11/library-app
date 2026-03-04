from app import db
from datetime import datetime
from enum import Enum

class AvailabilityStatus(Enum):
    AVAILABLE = 'AVAILABLE'
    CHECKED_OUT = 'CHECKED_OUT'
    RESERVED = 'RESERVED'
    LOST = 'LOST'

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    publication_date = db.Column(db.Date)
    availability_status = db.Column(db.Enum(AvailabilityStatus), default=AvailabilityStatus.AVAILABLE, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'publication_date': self.publication_date.isoformat() if self.publication_date else None,
            'availability_status': self.availability_status.value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def update_availability(self, new_status):
        if isinstance(new_status, str):
            new_status = AvailabilityStatus[new_status]
        self.availability_status = new_status
        self.updated_at = datetime.utcnow()
