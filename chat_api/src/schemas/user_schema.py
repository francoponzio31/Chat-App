from marshmallow import Schema, fields, validate
from schemas import custom_fields


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(validate=validate.Length(min=1), required=True)
    email = fields.Email(required=True)
    password = custom_fields.HashedPassword(required=True, load_only=True)
    role = fields.String(validate=validate.OneOf(["user", "admin"]), dump_only=True)
    picture_id = fields.UUID(required=False)
    creation_date = fields.DateTime(required=False, dump_only=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)