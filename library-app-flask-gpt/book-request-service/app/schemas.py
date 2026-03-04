from marshmallow import Schema, fields, validate

class BookRequestSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1, max=255))
    author = fields.String(required=True, validate=validate.Length(min=1, max=255))
    isbn = fields.String(required=False, validate=validate.Length(max=20))

class BookRequestUpdateSchema(Schema):
    status = fields.String(required=True, validate=validate.OneOf(["Approved", "Rejected"]))
