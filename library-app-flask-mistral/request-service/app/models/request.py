from app import db
from datetime import datetime
from enum import Enum

class RequestStatus(Enum):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    ARCHIVED = 'ARCHIVED'

class BookRequest(db.Model):
    __tablename__ = 'book_requests'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    book_title = db.Column(db.String(255), nullable=False)
    book_author = db.Column(db.String(100), nullable=False)
    book_isbn = db.Column(db.String(20))
    requester_id = db.Column(db.BigInteger, nullable=False)
    request_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.Enum(RequestStatus), default=RequestStatus.PENDING, nullable=False)
    decision_date = db.Column(db.DateTime)
    decided_by = db.Column(db.BigInteger)
    notes = db.Column(db.String(500))

    def __repr__(self):
        return f'<BookRequest {self.id} for {self.book_title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'book_title': self.book_title,
            'book_author': self.book_author,
            'book_isbn': self.book_isbn,
            'requester_id': self.requester_id,
            'request_date': self.request_date.isoformat(),
            'status': self.status.value,
            'decision_date': self.decision_date.isoformat() if self.decision_date else None,
            'decided_by': self.decided_by,
            'notes': self.notes
        }

    def approve(self, decided_by, notes=None):
        self.status = RequestStatus.APPROVED
        self.decision_date = datetime.utcnow()
        self.decided_by = decided_by
        self.notes = notes
        self.updated_at = datetime.utcnow()

    def reject(self, decided_by, notes=None):
        self.status = RequestStatus.REJECTED
        self.decision_date = datetime.utcnow()
        self.decided_by = decided_by
        self.notes = notes
        self.updated_at = datetime.utcnow()

    def archive(self):
        self.status = RequestStatus.ARCHIVED
        self.updated_at = datetime.utcnow()
