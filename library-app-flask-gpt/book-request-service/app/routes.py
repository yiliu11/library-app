from flask import Blueprint, request, jsonify
from . import db
from .models import BookRequest, RequestStatus, AuditLog
from .schemas import BookRequestSchema, BookRequestUpdateSchema
from .utils import token_required, role_required

request_bp = Blueprint("requests", __name__)

book_request_schema = BookRequestSchema()
book_request_update_schema = BookRequestUpdateSchema()

# Staff: Submit a book request
@request_bp.route("/", methods=["POST"])
@token_required
@role_required(["staff"])
def submit_request(current_user):
    data = request.get_json()
    errors = book_request_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    new_request = BookRequest(
        title=data["title"],
        author=data["author"],
        isbn=data.get("isbn"),
        requested_by=current_user["username"]
    )
    db.session.add(new_request)
    db.session.commit()

    return jsonify({"message": "Book request submitted", "request_id": new_request.id}), 201


# Librarian: Approve or Reject a request
@request_bp.route("/<int:request_id>", methods=["PUT"])
@token_required
@role_required(["librarian"])
def update_request(current_user, request_id):
    data = request.get_json()
    errors = book_request_update_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    book_request = BookRequest.query.get(request_id)
    if not book_request:
        return jsonify({"error": "Book request not found"}), 404

    new_status = RequestStatus[data["status"].upper()]
    book_request.status = new_status
    db.session.commit()

    # Log action
    log = AuditLog(
        action=f"Request {new_status.value}",
        performed_by=current_user["username"],
        request_id=book_request.id
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({"message": f"Book request {new_status.value.lower()}"}), 200


# Staff & Librarian: View requests
@request_bp.route("/", methods=["GET"])
@token_required
@role_required(["staff", "librarian"])
def view_requests(current_user):
    requests = BookRequest.query.all()
    result = [
        {
            "id": r.id,
            "title": r.title,
            "author": r.author,
            "isbn": r.isbn,
            "status": r.status.value,
            "requested_by": r.requested_by,
            "created_at": r.created_at
        }
        for r in requests
    ]
    return jsonify(result), 200
