from marshmallow import Schema, fields, validate
from schemas import custom_fields


# ---- INPUTS ----
class LoginBodySchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class SignupBodySchema(Schema):
    username = fields.String(validate=validate.Length(min=1), required=True)
    email = fields.Email(required=True)
    password = custom_fields.HashedPassword(required=True)


class EmailVerificationBodySchema(Schema):
    user_id = fields.Integer(required=True)
    token = fields.String(required=True)


login_body_schema = LoginBodySchema()
signup_body_schema = SignupBodySchema()
email_validation_body_schema = EmailVerificationBodySchema()

# ---- OUTPUTS ----
class CurrentUserOutputSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    email = fields.Email()
    role = fields.String()
    picture_id = fields.String()
    creation_date = fields.DateTime()


current_user_output_schema = CurrentUserOutputSchema()