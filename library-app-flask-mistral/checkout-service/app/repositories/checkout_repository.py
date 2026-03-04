from app import db
from app.models.checkout import Checkout, CheckoutStatus
from werkzeug.exceptions import NotFound, Conflict
from datetime import datetime
from app.utils.validators import CheckoutValidators

class CheckoutRepository:
    @staticmethod
    def get_checkout_by_id(checkout_id):
        CheckoutValidators.validate_checkout_id(checkout_id)
        checkout = Checkout.query.get(checkout_id)
        if not checkout:
            raise NotFound('Checkout not found')
        return checkout

    @staticmethod
    def get_checkouts_by_user_id(user_id):
        CheckoutValidators.validate_user_id(user_id)
        return Checkout.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_active_checkouts_by_user_id(user_id):
        CheckoutValidators.validate_user_id(user_id)
        return Checkout.query.filter_by(
            user_id=user_id,
            status=CheckoutStatus.ACTIVE
        ).all()

    @staticmethod
    def get_overdue_checkouts_by_user_id(user_id):
        CheckoutValidators.validate_user_id(user_id)
        return Checkout.query.filter_by(
            user_id=user_id,
            status=CheckoutStatus.OVERDUE
        ).all()

    @staticmethod
    def create_checkout(user_id, book_id, due_date):
        CheckoutValidators.validate_user_id(user_id)
        CheckoutValidators.validate_book_id(book_id)

        # Check for existing active checkout of the same book by the user
        existing_checkout = Checkout.query.filter_by(
            user_id=user_id,
            book_id=book_id,
            status=CheckoutStatus.ACTIVE
        ).first()
        if existing_checkout:
            raise Conflict('You already have this book checked out')

        checkout = Checkout(
            user_id=user_id,
            book_id=book_id,
            due_date=due_date
        )
        db.session.add(checkout)
        db.session.commit()
        return checkout

    @staticmethod
    def renew_checkout(checkout_id, new_due_date):
        checkout = CheckoutRepository.get_checkout_by_id(checkout_id)
        checkout.renew(new_due_date)
        db.session.commit()
        return checkout

    @staticmethod
    def return_book(checkout_id):
        checkout = CheckoutRepository.get_checkout_by_id(checkout_id)
        checkout.mark_as_returned()
        db.session.commit()
        return checkout

    @staticmethod
    def update_checkout_status(checkout_id, new_status):
        checkout = CheckoutRepository.get_checkout_by_id(checkout_id)
        checkout.status = CheckoutStatus[new_status]
        db.session.commit()
        return checkout
