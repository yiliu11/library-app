from marshmallow import Schema, fields, validate, validates_schema, ValidationError

# Used by librarian to create a user (delegates credentials to Auth Service)
class CreateUserRequestSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=128))
    email = fields.Email(required=True, validate=validate.Length(max=256))
    password = fields.Str(required=True, validate=validate.Length(min=8))
    role = fields.Str(required=True, validate=validate.OneOf(["patron", "staff", "librarian"]))
    full_name = fields.Str(required=False, allow_none=True, validate=validate.Length(max=256))
    phone = fields.Str(required=False, allow_none=True, validate=validate.Length(max=32))
    address = fields.Str(required=False, allow_none=True, validate=validate.Length(max=512))

class UpdateProfileSchema(Schema):
    full_name = fields.Str(required=False, allow_none=True, validate=validate.Length(max=256))
    phone = fields.Str(required=False, allow_none=True, validate=validate.Length(max=32))
    address = fields.Str(required=False, allow_none=True, validate=validate.Length(max=512))

class StatusPatchSchema(Schema):
    status = fields.Str(required=True, validate=validate.OneOf(["active", "suspended", "archived"]))

class QueryUsersSchema(Schema):
    q = fields.Str(required=False, allow_none=True)      # keyword in username/email/name
    role = fields.Str(required=False, allow_none=True, validate=validate.OneOf(["patron","staff","librarian"]))
    status = fields.Str(required=False, allow_none=True, validate=validate.OneOf(["active","suspended","archived"]))
    page = fields.Int(required=False, missing=1, validate=validate.Range(min=1))
    size = fields.Int(required=False, allow_none=True, validate=validate.Range(min=1))
