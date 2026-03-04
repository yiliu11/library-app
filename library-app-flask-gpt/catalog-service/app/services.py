from sqlalchemy import or_, func
from sqlalchemy.exc import IntegrityError
from flask import current_app
from .extensions import db
from .models import Book
from .errors import APIError
from datetime import datetime

class BookCatalogService:
    def __init__(self):
        self.db = db

    def add_book(self, data: dict):
        # Ensure copies_available default
        copies_total = data.get("copies_total", 1)
        copies_available = data.get("copies_available", copies_total if data.get("copies_available") is None else data.get("copies_available"))

        if copies_available > copies_total:
            raise APIError("copies_available cannot exceed copies_total", status_code=400)

        book = Book(
            title=data["title"].strip(),
            author=data["author"].strip(),
            isbn=data.get("isbn"),
            published_date=data.get("published_date"),
            genre=data.get("genre"),
            copies_total=copies_total,
            copies_available=copies_available
        )
        self.db.session.add(book)
        try:
            self.db.session.commit()
            current_app.logger.info("Book added: %s by %s", book.title, book.author)
            return book
        except IntegrityError as e:
            self.db.session.rollback()
            # If ISBN uniqueness fails, propagate a friendly message
            if "unique" in str(e).lower():
                raise APIError("Book with same ISBN already exists", status_code=409)
            raise APIError("Database error when adding book", status_code=500)

    def update_book(self, book_id: str, data: dict):
        book = Book.query.get(book_id)
        if not book:
            raise APIError("Book not found", status_code=404)

        # apply updates with validation
        if "title" in data:
            book.title = data["title"].strip()
        if "author" in data:
            book.author = data["author"].strip()
        if "isbn" in data:
            book.isbn = data["isbn"]
        if "published_date" in data:
            book.published_date = data["published_date"]
        if "genre" in data:
            book.genre = data["genre"]
        if "copies_total" in data:
            new_total = data["copies_total"]
            if new_total < 0:
                raise APIError("copies_total must be >= 0", status_code=400)
            # adjust copies_available proportionally if needed
            if new_total < book.copies_total:
                # ensure not to make copies_available > copies_total
                book.copies_available = min(book.copies_available, new_total)
            book.copies_total = new_total
        if "copies_available" in data:
            new_avail = data["copies_available"]
            if new_avail < 0 or new_avail > book.copies_total:
                raise APIError("Invalid copies_available value", status_code=400)
            book.copies_available = new_avail

        try:
            self.db.session.commit()
            current_app.logger.info("Book updated: %s (%s)", book.title, book.id)
            return book
        except IntegrityError as e:
            self.db.session.rollback()
            if "unique" in str(e).lower():
                raise APIError("Book with same ISBN already exists", status_code=409)
            raise APIError("Database error when updating book", status_code=500)

    def search_books(self, criteria: dict, page: int = 1, size: int = None):
        size = size or current_app.config["DEFAULT_PAGE_SIZE"]
        if size > current_app.config["MAX_PAGE_SIZE"]:
            size = current_app.config["MAX_PAGE_SIZE"]

        query = Book.query

        # apply filters safely using SQLAlchemy
        title = criteria.get("title")
        author = criteria.get("author")
        keyword = criteria.get("keyword")
        genre = criteria.get("genre")

        if title:
            query = query.filter(Book.title.ilike(f"%{title.strip()}%"))
        if author:
            query = query.filter(Book.author.ilike(f"%{author.strip()}%"))
        if genre:
            query = query.filter(Book.genre.ilike(f"%{genre.strip()}%"))
        if keyword:
            like_term = f"%{keyword.strip()}%"
            query = query.filter(
                or_(
                    Book.title.ilike(like_term),
                    Book.author.ilike(like_term),
                    Book.genre.ilike(like_term),
                    Book.isbn.ilike(like_term)
                )
            )

        total = query.with_entities(func.count()).scalar()
        # pagination
        items = query.order_by(Book.title.asc()).offset((page - 1) * size).limit(size).all()

        return {
            "total": int(total or 0),
            "page": page,
            "size": size,
            "items": items
        }

    def get_book(self, book_id: str):
        book = Book.query.get(book_id)
        if not book:
            raise APIError("Book not found", status_code=404)
        return book
