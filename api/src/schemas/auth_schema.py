from marshmallow import Schema, fields


class CredentialsSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)


credentials_schema = CredentialsSchema()