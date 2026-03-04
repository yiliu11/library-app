from flask import current_app
from werkzeug.exceptions import Unauthorized, BadRequest, NotFound, Conflict
from app.repositories.checkout_repository import CheckoutRepository
from app.utils.validators import CheckoutValidators
from app.models.checkout import CheckoutStatus
from datetime import datetime, timedelta
import requests

class CheckoutService:
    @staticmethod
    def _call_user_service(endpoint, user_id=None, method='GET', data=None):
        url = f"{current_app.config['USER_SERVICE_URL']}/{endpoint}"
        headers = {'Authorization': f"Bearer {current_app.config['CHECKOUT_SERVICE_API_KEY']}"}

        if user_id:
            url = f"{url}/{user_id}" if '{user_id}' in endpoint else f"{url}?user_id={user_id}"

        response = requests.request(method, url, headers=headers, json=data)

        if not response.ok:
            raise Exception(f"User service error: {response.text}")

        return response.json()

    @staticmethod
    def _call_book_service(endpoint, book_id=None, method='GET', data=None):
        url = f"{current_app.config['BOOK_SERVICE_URL']}/{endpoint}"
        headers = {'Authorization': f"Bearer {current_app.config['CHECKOUT_SERVICE_API_KEY']}"}

        if book_id:
            url = f"{url}/{book_id}" if '{book_id}' in endpoint else f"{url}?book_id={book_id}"

        response = requests.request(method, url, headers=headers, json=data)

        if not response.ok:
            raise Exception(f"Book service error: {response.text}")

        return response.json()

    @staticmethod
    def checkout_book(user_id, book_id, requesting_user_role):
        # Verify user exists and is active
        try:
            user = CheckoutService._call_user_service('users', user_id)
            if not user.get('is_active', False):
                raise Unauthorized('User account is not active')
        except Exception as e:
            raise NotFound('User not found')

        # Verify book exists and is available
        try:
            book = CheckoutService._call_book_service('books', book_id)
            if book.get('availability_status') != 'AVAILABLE':
                raise Conflict('Book is not available for checkout')
        except Exception as e:
            raise NotFound('Book not found')

        # Check if user has reached checkout limit
        active_checkouts = CheckoutRepository.get_active_checkouts_by_user_id(user_id)
        if len(active_checkouts) >= current_app.config['MAX_CHECKOUTS_PER_USER']:
            raise Conflict(f'Maximum checkout limit ({current_app.config["MAX_CHECKOUTS_PER_USER"]}) reached')

        # Create checkout
        due_date = datetime.utcnow() + timedelta(days=current_app.config['MAX_CHECKOUT_DAYS'])
        checkout = CheckoutRepository.create_checkout(user_id, book_id, due_date)

        # Update book availability
        try:
            CheckoutService._call_book_service(
                f'books/{book_id}/availability',
                method='PUT',
                data={'status': 'CHECKED_OUT'}
            )
        except Exception as e:
            current_app.logger.error(f"Failed to update book availability: {str(e)}")
            # Rollback checkout if book update fails
            db.session.delete(checkout)
            db.session.commit()
            raise Exception('Failed to update book availability')

        return checkout.to_dict()

    @staticmethod
    def renew_checkout(checkout_id, user_id):
        checkout = CheckoutRepository.get_checkout_by_id(checkout_id)

        # Verify user owns the checkout
        if checkout.user_id != user_id:
            raise Unauthorized('You can only renew your own checkouts')

        # Check if checkout is eligible for renewal
        if checkout.status != CheckoutStatus.ACTIVE:
            raise Conflict('Only active checkouts can be renewed')

        # Calculate new due date
        new_due_date = datetime.utcnow() + timedelta(days=current_app.config['RENEWAL_DAYS'])

        # Renew checkout
        renewed_checkout = CheckoutRepository.renew_checkout(checkout_id, new_due_date)

        return renewed_checkout.to_dict()

    @staticmethod
    def return_book(checkout_id, user_id, user_role):
        checkout = CheckoutRepository.get_checkout_by_id(checkout_id)

        # Verify user owns the checkout or is a librarian
        if checkout.user_id != user_id and user_role != 'LIBRARIAN':
            raise Unauthorized('You can only return your own checkouts')

        # Return book
        returned_checkout = CheckoutRepository.return_book(checkout_id)

        # Update book availability
        try:
            CheckoutService._call_book_service(
                f'books/{checkout.book_id}/availability',
                method='PUT',
                data={'status': 'AVAILABLE'}
            )
        except Exception as e:
            current_app.logger.error(f"Failed to update book availability: {str(e)}")
            # The checkout is still marked as returned, but book status might be inconsistent
            # In a production system, you might want to implement a retry mechanism

        return returned_checkout.to_dict()

    @staticmethod
    def get_user_records(user_id, requesting_user_id, requesting_user_role):
        # Verify requesting user has permission
        if user_id != requesting_user_id and requesting_user_role != 'LIBRARIAN':
            raise Unauthorized('You can only view your own records')

        checkouts = CheckoutRepository.get_checkouts_by_user_id(user_id)

        # Get book details for each checkout
        user_records = []
        total_fines = 0.0

        for checkout in checkouts:
            try:
                book = CheckoutService._call_book_service('books', checkout.book_id)
                book_title = book.get('title', 'Unknown')

                # Calculate fine if overdue
                if checkout.status == CheckoutStatus.OVERDUE:
                    fine = checkout.calculate_fine(current_app.config['DAILY_FINE_AMOUNT'])
                    total_fines += fine
                else:
                    fine = float(checkout.fine_amount)

                user_records.append({
                    'checkout_id': checkout.id,
                    'book_id': checkout.book_id,
                    'book_title': book_title,
                    'due_date': checkout.due_date.isoformat(),
                    'status': checkout.status.value,
                    'fine_amount': fine
                })
            except Exception as e:
                current_app.logger.error(f"Failed to get book details for checkout {checkout.id}: {str(e)}")
                continue

        return {
            'user_id': user_id,
            'checked_out_items': user_records,
            'total_fines': total_fines
        }

    @staticmethod
    def check_overdue_checkouts():
        # Get all active checkouts
        active_checkouts = Checkout.query.filter_by(status=CheckoutStatus.ACTIVE).all()

        overdue_count = 0
        for checkout in active_checkouts:
            if datetime.utcnow() > checkout.due_date:
                # Mark as overdue
                checkout.status = CheckoutStatus.OVERDUE
                db.session.commit()
                overdue_count += 1

                # In a real application, you would also send a notification
                # This would be handled by the Notification Service

        return {'message': f'Checked {len(active_checkouts)} active checkouts, found {overdue_count} overdue'}

    @staticmethod
    def update_checkout_status(checkout_id, new_status):
        CheckoutValidators.validate_checkout_status(new_status)
        checkout = CheckoutRepository.update_checkout_status(checkout_id, new_status)
        return checkout.to_dict()
