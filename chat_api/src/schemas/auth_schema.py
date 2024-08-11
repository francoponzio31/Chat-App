from marshmallow import Schema, fields


class CredentialsSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)


class CurrentUserSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    email = fields.Email()
    role = fields.String()
    creation_date = fields.DateTime()


credentials_schema = CredentialsSchema()
current_user_schema = CurrentUserSchema()