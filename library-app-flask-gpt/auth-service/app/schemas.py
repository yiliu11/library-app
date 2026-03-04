from marshmallow import Schema, fields, validate, ValidationError, validates

class RegisterSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=128))
    email = fields.Email(required=True, validate=validate.Length(max=256))
    password = fields.Str(required=True, validate=validate.Length(min=8))
    role = fields.Str(required=False, validate=validate.OneOf(["patron","staff","librarian"]))

class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class TokenResponseSchema(Schema):
    token = fields.Str()
    expires_in = fields.Int()
    role = fields.Str()
