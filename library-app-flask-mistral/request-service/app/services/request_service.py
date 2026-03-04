from flask import current_app
from werkzeug.exceptions import Unauthorized, BadRequest, NotFound, Conflict
from app.repositories.request_repository import RequestRepository
from app.utils.validators import RequestValidators
from app.models.request import RequestStatus
import requests
import json

class RequestService:
    @staticmethod
    def _call_user_service(endpoint, user_id=None, method='GET', data=None):
        url = f"{current_app.config['USER_SERVICE_URL']}/{endpoint}"
        headers = {
            'Authorization': f"Bearer {current_app.config['REQUEST_SERVICE_API_KEY']}",
            'Content-Type': 'application/json'
        }

        if user_id:
            url = f"{url}/{user_id}" if '{user_id}' in endpoint else f"{url}?user_id={user_id}"

        response = requests.request(method, url, headers=headers, json=data)

        if not response.ok:
            raise Exception(f"User service error: {response.text}")

        return response.json()

    @staticmethod
    def _call_notification_service(endpoint, data):
        url = f"{current_app.config['NOTIFICATION_SERVICE_URL']}/{endpoint}"
        headers = {
            'Authorization': f"Bearer {current_app.config['REQUEST_SERVICE_API_KEY']}",
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, json=data)

        if not response.ok:
            current_app.logger.error(f"Failed to send notification: {response.text}")
            # Continue even if notification fails (fire-and-forget pattern)
            # In production, you might want to implement a retry mechanism

    @staticmethod
    def submit_request(book_title, book_author, book_isbn, requester_id, requester_role):
        # Verify requester is staff
        try:
            user = RequestService._call_user_service('users', requester_id)
            if user.get('role') != 'STAFF':
                raise Unauthorized('Only staff members can submit book requests')
        except Exception as e:
            raise NotFound('User not found')

        # Create request
        request = RequestRepository.create_request(
            book_title, book_author, book_isbn, requester_id
        )

        # Send notification to librarians (in a real app, this would be more sophisticated)
        notification_data = {
            'recipient_role': 'LIBRARIAN',
            'subject': f'New Book Request: {book_title}',
            'message': f'Staff member {requester_id} has requested a new book: {book_title} by {book_author}',
            'notification_type': 'REQUEST_SUBMITTED',
            'metadata': {
                'request_id': str(request.id),
                'book_title': book_title
            }
        }

        try:
            RequestService._call_notification_service('notify/role', notification_data)
        except Exception as e:
            current_app.logger.error(f"Failed to send notification: {str(e)}")

        return request.to_dict()

    @staticmethod
    def process_decision(request_id, status, decided_by, notes=None):
        # Verify decided_by is a librarian
        try:
            user = RequestService._call_user_service('users', decided_by)
            if user.get('role') != 'LIBRARIAN':
                raise Unauthorized('Only librarians can process requests')
        except Exception as e:
            raise NotFound('User not found')

        # Update request status
        request = RequestRepository.update_request_status(
            request_id, status, decided_by, notes
        )

        # Send notification to requester
        requester = RequestService._call_user_service('users', request.requester_id)
        requester_email = requester.get('email')

        notification_data = {
            'recipient_id': request.requester_id,
            'recipient_email': requester_email,
            'subject': f'Book Request {status}: {request.book_title}',
            'message': f'Your request for "{request.book_title}" has been {status.lower()}.',
            'notification_type': f'REQUEST_{status}',
            'metadata': {
                'request_id': str(request.id),
                'book_title': request.book_title,
                'notes': notes
            }
        }

        try:
            RequestService._call_notification_service('notify', notification_data)
        except Exception as e:
            current_app.logger.error(f"Failed to send notification: {str(e)}")

        # If approved, add book to acquisition list (in a real app, this would be more complex)
        if status == 'APPROVED':
            try:
                book_data = {
                    'title': request.book_title,
                    'author': request.book_author,
                    'isbn': request.book_isbn,
                    'metadata': {
                        'request_id': str(request.id),
                        'requester_id': str(request.requester_id)
                    }
                }
                # In a real app, you would call an acquisition service or add to a database
                current_app.logger.info(f"Book approved for acquisition: {json.dumps(book_data)}")
            except Exception as e:
                current_app.logger.error(f"Failed to process approved book: {str(e)}")

        return request.to_dict()

    @staticmethod
    def get_pending_requests(user_role):
        if user_role != 'LIBRARIAN':
            raise Unauthorized('Only librarians can view pending requests')

        requests = RequestRepository.get_pending_requests()
        return [request.to_dict() for request in requests]

    @staticmethod
    def get_requests_by_requester(requester_id, user_id, user_role):
        # Verify user can only access their own requests (unless librarian)
        if requester_id != user_id and user_role != 'LIBRARIAN':
            raise Unauthorized('You can only view your own requests')

        requests = RequestRepository.get_requests_by_requester_id(requester_id)
        return [request.to_dict() for request in requests]

    @staticmethod
    def get_requests_by_status(status, user_role):
        if user_role != 'LIBRARIAN':
            raise Unauthorized('Only librarians can filter requests by status')

        RequestValidators.validate_request_status(status)
        requests = RequestRepository.get_requests_by_status(status)
        return [request.to_dict() for request in requests]
