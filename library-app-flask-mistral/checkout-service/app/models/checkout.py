from app import db
from datetime import datetime, timedelta
from enum import Enum

class CheckoutStatus(Enum):
    ACTIVE = 'ACTIVE'
    OVERDUE = 'OVERDUE'
    RETURNED = 'RETURNED'
    RENEWED = 'RENEWED'

class Checkout(db.Model):
    __tablename__ = 'checkouts'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    book_id = db.Column(db.BigInteger, nullable=False)
    checkout_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime)
    status = db.Column(db.Enum(CheckoutStatus), default=CheckoutStatus.ACTIVE, nullable=False)
    fine_amount = db.Column(db.Numeric(10, 2), default=0.00, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Checkout {self.id} for user {self.user_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'checkout_date': self.checkout_date.isoformat(),
            'due_date': self.due_date.isoformat(),
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'status': self.status.value,
            'fine_amount': float(self.fine_amount),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def calculate_due_date(self, max_checkout_days):
        return datetime.utcnow() + timedelta(days=max_checkout_days)

    def calculate_fine(self, daily_fine_amount):
        if self.status != CheckoutStatus.OVERDUE:
            return 0.00

        days_overdue = (datetime.utcnow() - self.due_date).days
        return days_overdue * daily_fine_amount

    def mark_as_returned(self):
        self.status = CheckoutStatus.RETURNED
        self.return_date = datetime.utcnow()
        self.fine_amount = self.calculate_fine(current_app.config['DAILY_FINE_AMOUNT'])

    def renew(self, renewal_days):
        if self.status != CheckoutStatus.ACTIVE:
            raise ValueError('Only active checkouts can be renewed')

        self.status = CheckoutStatus.RENEWED
        self.due_date = datetime.utcnow() + timedelta(days=renewal_days)
        self.updated_at = datetime.utcnow()
