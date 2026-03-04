from app import db
from app.models.request import BookRequest, RequestStatus
from werkzeug.exceptions import NotFound, Conflict
from app.utils.validators import RequestValidators

class RequestRepository:
    @staticmethod
    def get_request_by_id(request_id):
        request = BookRequest.query.get(request_id)
        if not request:
            raise NotFound('Request not found')
        return request

    @staticmethod
    def get_requests_by_requester_id(requester_id):
        return BookRequest.query.filter_by(requester_id=requester_id).all()

    @staticmethod
    def get_pending_requests():
        return BookRequest.query.filter_by(status=RequestStatus.PENDING).all()

    @staticmethod
    def create_request(book_title, book_author, book_isbn, requester_id):
        RequestValidators.validate_book_title(book_title)
        RequestValidators.validate_book_author(book_author)
        if book_isbn:
            RequestValidators.validate_isbn(book_isbn)

        request = BookRequest(
            book_title=book_title,
            book_author=book_author,
            book_isbn=book_isbn,
            requester_id=requester_id
        )
        db.session.add(request)
        db.session.commit()
        return request

    @staticmethod
    def update_request_status(request_id, new_status, decided_by=None, notes=None):
        request = RequestRepository.get_request_by_id(request_id)
        RequestValidators.validate_request_status(new_status)

        if new_status == 'APPROVED':
            request.approve(decided_by, notes)
        elif new_status == 'REJECTED':
            request.reject(decided_by, notes)
        elif new_status == 'ARCHIVED':
            request.archive()

        db.session.commit()
        return request

    @staticmethod
    def get_requests_by_status(status):
        RequestValidators.validate_request_status(status)
        return BookRequest.query.filter_by(status=RequestStatus[status]).all()
