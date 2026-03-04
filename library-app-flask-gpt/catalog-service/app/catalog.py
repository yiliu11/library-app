from flask import Blueprint, request, jsonify, current_app
from .schemas import BookRequestSchema, BookResponseSchema, SearchQuerySchema
from .services import BookCatalogService
from .errors import APIError
from .utils import jwt_required, role_required, jwt_optional
from marshmallow import ValidationError
from .extensions import db

catalog_bp = Blueprint("catalog", __name__)
service = BookCatalogService()

# GET /api/catalog/books/<id>
@catalog_bp.route("/books/<book_id>", methods=["GET"])
@jwt_optional
def get_book(book_id):
    try:
        book = service.get_book(book_id)
    except APIError as e:
        raise e
    return jsonify(BookResponseSchema().dump(book)), 200

# GET /api/catalog/books  (search)
@catalog_bp.route("/books", methods=["GET"])
@jwt_optional
def search_books():
    # Validate query params
    schema = SearchQuerySchema()
    try:
        params = schema.load({
            "title": request.args.get("title"),
            "author": request.args.get("author"),
            "keyword": request.args.get("keyword"),
            "genre": request.args.get("genre"),
            "page": request.args.get("page", None),
            "size": request.args.get("size", None)
        })
    except ValidationError as e:
        raise APIError("Invalid query parameters: %s" % e.messages, status_code=400)

    page = params.get("page", 1)
    size = params.get("size") or current_app.config["DEFAULT_PAGE_SIZE"]

    result = service.search_books(params, page=page, size=size)
    # serialize items
    response = {
        "total": result["total"],
        "page": result["page"],
        "size": result["size"],
        "items": BookResponseSchema(many=True).dump(result["items"])
    }
    return jsonify(response), 200

# POST /api/catalog/books  (add book) - librarian only
@catalog_bp.route("/books", methods=["POST"])
@jwt_required
@role_required(["librarian"])
def add_book():
    json_data = request.get_json() or {}
    schema = BookRequestSchema()
    try:
        data = schema.load(json_data)
    except ValidationError as e:
        raise APIError("Invalid book data: %s" % e.messages, status_code=400)

    try:
        book = service.add_book(data)
        return jsonify(BookResponseSchema().dump(book)), 201
    except APIError as e:
        raise e

# PUT /api/catalog/books/<id>  (update book) - librarian only
@catalog_bp.route("/books/<book_id>", methods=["PUT"])
@jwt_required
@role_required(["librarian"])
def update_book(book_id):
    json_data = request.get_json() or {}
    schema = BookRequestSchema(partial=True)
    try:
        data = schema.load(json_data)
    except ValidationError as e:
        raise APIError("Invalid book data: %s" % e.messages, status_code=400)

    try:
        book = service.update_book(book_id, data)
        return jsonify(BookResponseSchema().dump(book)), 200
    except APIError as e:
        raise e
