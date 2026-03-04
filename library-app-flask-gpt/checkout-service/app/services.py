from datetime import datetime, timedelta
from flask import current_app
from .extensions import db
from .models import Loan, LoanStatus
from .clients import CatalogClient
from .errors import APIError

class LoanService:
    def __init__(self):
        self.db = db
        self.catalog = CatalogClient()
        self.max_renewals = current_app.config.get("MAX_RENEWALS", 2)
        self.loan_period_days = current_app.config.get("LOAN_PERIOD_DAYS", 14)

    def checkout_book(self, user_id: str, book_id: str):
        # Step 1: Ask Catalog to reserve a copy (atomic in Catalog)
        self.catalog.reserve_book(book_id, user_id)

        # Step 2: Create local Loan record
        due_date = datetime.utcnow() + timedelta(days=self.loan_period_days)
        loan = Loan(
            user_id=user_id,
            book_id=book_id,
            checkout_date=datetime.utcnow(),
            due_date=due_date,
            renewal_count=0,
            status=LoanStatus.CHECKED_OUT
        )
        self.db.session.add(loan)
        try:
            self.db.session.commit()
            current_app.logger.info("Loan created: %s for user %s book %s", loan.id, user_id, book_id)
            return loan
        except Exception as e:
            self.db.session.rollback()
            # Attempt to release reservation in Catalog to avoid lost copies
            try:
                self.catalog.release_book(book_id, user_id)
            except APIError:
                current_app.logger.error("Failed to release book after DB error for loan creation")
            raise APIError("Failed to create loan", status_code=500)

    def renew_loan(self, user_id: str, loan_id: str):
        loan = Loan.query.get(loan_id)
        if not loan:
            raise APIError("Loan not found", status_code=404)
        if loan.user_id != user_id:
            raise APIError("Loan does not belong to user", status_code=403)
        if not loan.can_renew(self.max_renewals):
            raise APIError("Loan not eligible for renewal", status_code=403)

        # Extend due date
        loan.renewal_count += 1
        loan.due_date = datetime.utcnow() + timedelta(days=self.loan_period_days)
        try:
            self.db.session.commit()
            current_app.logger.info("Loan renewed: %s (renewal_count=%d)", loan.id, loan.renewal_count)
            return loan
        except Exception as e:
            self.db.session.rollback()
            raise APIError("Failed to renew loan", status_code=500)

    def return_loan(self, user_id: str, loan_id: str):
        loan = Loan.query.get(loan_id)
        if not loan:
            raise APIError("Loan not found", status_code=404)
        if loan.user_id != user_id:
            raise APIError("Loan does not belong to user", status_code=403)
        if loan.status == LoanStatus.RETURNED:
            raise APIError("Loan already returned", status_code=400)

        # Mark returned locally
        loan.return_date = datetime.utcnow()
        loan.status = LoanStatus.RETURNED
        try:
            self.db.session.commit()
            # Notify Catalog to increment availability
            try:
                self.catalog.release_book(loan.book_id, user_id)
            except APIError:
                current_app.logger.error("Failed to notify catalog of returned book")
                # still return success — inventory can be reconciled later
            current_app.logger.info("Loan returned: %s", loan.id)
            return loan
        except Exception as e:
            self.db.session.rollback()
            raise APIError("Failed to return loan", status_code=500)

    def get_user_loans(self, user_id: str):
        loans = Loan.query.filter_by(user_id=user_id).order_by(Loan.checkout_date.desc()).all()
        return loans

    def get_loan(self, loan_id: str):
        loan = Loan.query.get(loan_id)
        if not loan:
            raise APIError("Loan not found", status_code=404)
        return loan
