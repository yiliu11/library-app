from flask import Blueprint, request, jsonify, g, current_app
from .schemas import CheckoutRequestSchema, CheckoutResponseSchema, RenewRequestSchema, LoanResponseSchema
from .services import LoanService
from .errors import APIError
from .utils import jwt_required
from marshmallow import ValidationError

checkout_bp = Blueprint("checkout", __name__)
service = LoanService()

# POST /api/checkout/  (checkout a book)
@checkout_bp.route("/", methods=["POST"])
@jwt_required
def checkout():
    schema = CheckoutRequestSchema()
    try:
        data = schema.load(request.get_json() or {})
    except ValidationError as e:
        raise APIError(f"Invalid request: {e.messages}", status_code=400)

    user = g.current_user
    try:
        loan = service.checkout_book(user_id=user["id"], book_id=data["book_id"])
        return jsonify(CheckoutResponseSchema().dump(loan)), 201
    except APIError as e:
        raise e

# POST /api/checkout/renew  (renew a loan)
@checkout_bp.route("/renew", methods=["POST"])
@jwt_required
def renew():
    schema = RenewRequestSchema()
    try:
        data = schema.load(request.get_json() or {})
    except ValidationError as e:
        raise APIError(f"Invalid request: {e.messages}", status_code=400)

    user = g.current_user
    try:
        loan = service.renew_loan(user_id=user["id"], loan_id=data["loan_id"])
        return jsonify(LoanResponseSchema().dump(loan)), 200
    except APIError as e:
        raise e

# POST /api/checkout/return  (return a loan)
@checkout_bp.route("/return", methods=["POST"])
@jwt_required
def return_loan():
    schema = RenewRequestSchema()  # reuse: loan_id
    try:
        data = schema.load(request.get_json() or {})
    except ValidationError as e:
        raise APIError(f"Invalid request: {e.messages}", status_code=400)
    user = g.current_user
    try:
        loan = service.return_loan(user_id=user["id"], loan_id=data["loan_id"])
        return jsonify(LoanResponseSchema().dump(loan)), 200
    except APIError as e:
        raise e

# GET /api/checkout/loans  (list current user's loans)
@checkout_bp.route("/loans", methods=["GET"])
@jwt_required
def list_loans():
    user = g.current_user
    loans = service.get_user_loans(user_id=user["id"])
    return jsonify(LoanResponseSchema(many=True).dump(loans)), 200

# GET /api/checkout/loans/<id>
@checkout_bp.route("/loans/<loan_id>", methods=["GET"])
@jwt_required
def get_loan(loan_id):
    user = g.current_user
    try:
        loan = service.get_loan(loan_id)
        if loan.user_id != user["id"]:
            raise APIError("Loan does not belong to user", status_code=403)
        return jsonify(LoanResponseSchema().dump(loan)), 200
    except APIError as e:
        raise e
