import datetime
import enum
from . import db

class RequestStatus(enum.Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"

class BookRequest(db.Model):
    __tablename__ = "book_requests"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.String(20), nullable=True)
    requested_by = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Enum(RequestStatus), default=RequestStatus.PENDING, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(50), nullable=False)
    performed_by = db.Column(db.String(100), nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey("book_requests.id"), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
