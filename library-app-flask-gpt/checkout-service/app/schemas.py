from marshmallow import Schema, fields, validate, ValidationError

class CheckoutRequestSchema(Schema):
    book_id = fields.Str(required=True)

class CheckoutResponseSchema(Schema):
    id = fields.Str()
    user_id = fields.Str()
    book_id = fields.Str()
    checkout_date = fields.DateTime()
    due_date = fields.DateTime()
    renewal_count = fields.Int()
    status = fields.Str()

class RenewRequestSchema(Schema):
    loan_id = fields.Str(required=True)

class LoanResponseSchema(Schema):
    id = fields.Str()
    user_id = fields.Str()
    book_id = fields.Str()
    checkout_date = fields.DateTime()
    due_date = fields.DateTime()
    return_date = fields.DateTime(allow_none=True)
    renewal_count = fields.Int()
    status = fields.Str()
