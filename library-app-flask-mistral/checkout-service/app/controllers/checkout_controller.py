from flask import request, jsonify
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.dtos.checkout_dto import (
    CheckoutRequestDTO, CheckoutResponseDTO,
    RenewalRequestDTO, ReturnRequestDTO, UserRecordDTO
)
from app.services.checkout_service import CheckoutService
from app.utils.logger import setup_logging

api = Namespace('checkout', description='Checkout operations')

@api.route('/')
class CheckoutList(Resource):
    @api.expect(CheckoutRequestDTO.api_model)
    @jwt_required()
    def post(self):
        """Checkout a book"""
        current_user = get_jwt_identity()
        data = request.get_json()
        try:
            checkout = CheckoutService.checkout_book(
                data['user_id'],
                data['book_id'],
                current_user['role']
            )
            return CheckoutResponseDTO.api_model(checkout), 201
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/renew')
class CheckoutRenew(Resource):
    @api.expect(RenewalRequestDTO.api_model)
    @jwt_required()
    def put(self):
        """Renew a checked-out book"""
        current_user = get_jwt_identity()
        data = request.get_json()
        try:
            renewed_checkout = CheckoutService.renew_checkout(
                data['checkout_id'],
                current_user['user_id']
            )
            return CheckoutResponseDTO.api_model(renewed_checkout), 200
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/return')
class CheckoutReturn(Resource):
    @api.expect(ReturnRequestDTO.api_model)
    @jwt_required()
    def put(self):
        """Return a checked-out book"""
        current_user = get_jwt_identity()
        data = request.get_json()
        try:
            returned_checkout = CheckoutService.return_book(
                data['checkout_id'],
                current_user['user_id'],
                current_user['role']
            )
            return CheckoutResponseDTO.api_model(returned_checkout), 200
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/records/<int:user_id>')
@api.param('user_id', 'User ID')
class UserRecords(Resource):
    @api.marshal_with(UserRecordDTO.api_model)
    @jwt_required()
    def get(self, user_id):
        """Get user's checkout records"""
        current_user = get_jwt_identity()
        try:
            records = CheckoutService.get_user_records(
                user_id,
                current_user['user_id'],
                current_user['role']
            )
            return records, 200
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/admin/check-overdue')
class CheckOverdue(Resource):
    @jwt_required()
    def post(self):
        """Check for overdue checkouts (admin task)"""
        current_user = get_jwt_identity()
        if current_user['role'] != 'LIBRARIAN':
            return {'error': 'Only librarians can perform this action'}, 403

        try:
            result = CheckoutService.check_overdue_checkouts()
            return result, 200
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/<int:checkout_id>/status')
@api.param('checkout_id', 'Checkout ID')
class CheckoutStatus(Resource):
    @jwt_required()
    def put(self, checkout_id):
        """Update checkout status"""
        current_user = get_jwt_identity()
        data = request.get_json()
        try:
            if current_user['role'] not in ['LIBRARIAN', 'CHECKOUT_SERVICE']:
                return {'error': 'Not authorized to update checkout status'}, 403

            updated_checkout = CheckoutService.update_checkout_status(
                checkout_id,
                data['status']
            )
            return CheckoutResponseDTO.api_model(updated_checkout), 200
        except Exception as e:
            return {'error': str(e)}, 400
