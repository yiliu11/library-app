import uuid
from datetime import datetime, timedelta
from enum import Enum
from .extensions import db

def gen_uuid():
    return str(uuid.uuid4())

class LoanStatus(Enum):
    CHECKED_OUT = "checked_out"
    RETURNED = "returned"
    OVERDUE = "overdue"

class Loan(db.Model):
    __tablename__ = "loans"
    id = db.Column(db.String, primary_key=True, default=gen_uuid)
    user_id = db.Column(db.String, nullable=False, index=True)
    book_id = db.Column(db.String, nullable=False, index=True)
    checkout_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)
    renewal_count = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.Enum(LoanStatus), nullable=False, default=LoanStatus.CHECKED_OUT)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def is_overdue(self):
        if self.status == LoanStatus.RETURNED:
            return False
        return datetime.utcnow() > self.due_date

    def can_renew(self, max_renewals):
        if self.status != LoanStatus.CHECKED_OUT:
            return False
        if self.renewal_count >= max_renewals:
            return False
        if self.is_overdue():
            return False
        return True

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "checkout_date": self.checkout_date.isoformat() if self.checkout_date else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "return_date": self.return_date.isoformat() if self.return_date else None,
            "renewal_count": self.renewal_count,
            "status": self.status.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
