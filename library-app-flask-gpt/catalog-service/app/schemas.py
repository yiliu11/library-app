from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import datetime

class BookRequestSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=512))
    author = fields.Str(required=True, validate=validate.Length(min=1, max=256))
    isbn = fields.Str(required=False, allow_none=True, validate=validate.Length(max=64))
    published_date = fields.Date(required=False, allow_none=True)
    genre = fields.Str(required=False, allow_none=True, validate=validate.Length(max=128))
    copies_total = fields.Int(required=False, missing=1, validate=validate.Range(min=0))
    copies_available = fields.Int(required=False, missing=None, validate=validate.Range(min=0))

    @validates("copies_available")
    def validate_copies_available(self, val):
        # copies_available can't be greater than copies_total — this will be additionally enforced in service
        if val is not None and val < 0:
            raise ValidationError("copies_available must be >= 0")

class BookResponseSchema(Schema):
    id = fields.Str()
    title = fields.Str()
    author = fields.Str()
    isbn = fields.Str(allow_none=True)
    published_date = fields.Date(allow_none=True)
    genre = fields.Str(allow_none=True)
    copies_total = fields.Int()
    copies_available = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

class SearchQuerySchema(Schema):
    title = fields.Str(required=False, allow_none=True)
    author = fields.Str(required=False, allow_none=True)
    keyword = fields.Str(required=False, allow_none=True)
    genre = fields.Str(required=False, allow_none=True)
    page = fields.Int(missing=1, validate=validate.Range(min=1))
    size = fields.Int(missing=None, validate=validate.Range(min=1))
