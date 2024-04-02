from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(validate=validate.Length(min=1), required=True)
    email = fields.Email(required=True)
    password = fields.String(required=False, load_only=True)
    role = fields.String(validate=validate.OneOf(["user", "admin"]), required=True)
    picture_id = fields.UUID(required=False)
    creation_date = fields.DateTime(required=False, dump_only=True)
    last_connection = fields.DateTime(required=False)


user_schema = UserSchema()
users_schema = UserSchema(many=True)