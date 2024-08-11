from marshmallow import Schema, fields


# Inputs schema
class CredentialsSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)

class EmailVerificationSchema(Schema):
    user_id = fields.Integer(required=True)
    token = fields.String(required=True)

# Output schemas
class CurrentUserSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    email = fields.Email()
    role = fields.String()
    creation_date = fields.DateTime()


credentials_schema = CredentialsSchema()
email_validation_schema = EmailVerificationSchema()
current_user_schema = CurrentUserSchema()