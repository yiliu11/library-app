from flask import request, jsonify
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.dtos.request_dto import (
    BookRequestDTO, BookRequestResponseDTO,
    RequestDecisionDTO, RequestSearchDTO
)
from app.services.request_service import RequestService

api = Namespace('requests', description='Book request operations')

@api.route('/')
class RequestList(Resource):
    @api.expect(BookRequestDTO.api_model)
    @jwt_required()
    def post(self):
        """Submit a new book request (staff only)"""
        current_user = get_jwt_identity()
        data = request.get_json()
        try:
            book_request = RequestService.submit_request(
                data['book_title'],
                data['book_author'],
                data.get('book_isbn'),
                current_user['user_id'],
                current_user['role']
            )
            return BookRequestResponseDTO.api_model(book_request), 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.marshal_list_with(BookRequestResponseDTO.api_model)
    @jwt_required()
    def get(self):
        """Get pending requests (librarian only) or user's requests"""
        current_user = get_jwt_identity()
        try:
            if current_user['role'] == 'LIBRARIAN':
                requests = RequestService.get_pending_requests(current_user['role'])
            else:
                requests = RequestService.get_requests_by_requester(
                    current_user['user_id'],
                    current_user['user_id'],
                    current_user['role']
                )
            return requests, 200
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/<int:request_id>')
@api.param('request_id', 'Request ID')
class RequestDetail(Resource):
    @api.marshal_with(BookRequestResponseDTO.api_model)
    @jwt_required()
    def get(self, request_id):
        """Get request details"""
        try:
            request = RequestService.get_request_by_id(request_id)
            return request.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 404

@api.route('/decide')
class RequestDecision(Resource):
    @api.expect(RequestDecisionDTO.api_model)
    @jwt_required()
    def put(self):
        """Approve or reject a book request (librarian only)"""
        current_user = get_jwt_identity()
        data = request.get_json()
        try:
            decided_request = RequestService.process_decision(
                data['request_id'],
                data['status'],
                current_user['user_id'],
                data.get('notes')
            )
            return BookRequestResponseDTO.api_model(decided_request), 200
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/status/<string:status>')
@api.param('status', 'Request status (PENDING, APPROVED, REJECTED, ARCHIVED)')
class RequestsByStatus(Resource):
    @api.marshal_list_with(BookRequestResponseDTO.api_model)
    @jwt_required()
    def get(self, status):
        """Get requests by status (librarian only)"""
        current_user = get_jwt_identity()
        try:
            requests = RequestService.get_requests_by_status(
                status,
                current_user['role']
            )
            return requests, 200
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/user/<int:user_id>')
@api.param('user_id', 'User ID')
class UserRequests(Resource):
    @api.marshal_list_with(BookRequestResponseDTO.api_model)
    @jwt_required()
    def get(self, user_id):
        """Get requests by user"""
        current_user = get_jwt_identity()
        try:
            requests = RequestService.get_requests_by_requester(
                user_id,
                current_user['user_id'],
                current_user['role']
            )
            return requests, 200
        except Exception as e:
            return {'error': str(e)}, 400
