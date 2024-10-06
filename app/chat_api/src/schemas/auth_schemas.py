from schemas.base_schema import BaseSchema
from marshmallow import fields, validate
from schemas import custom_fields


# ---- INPUTS ----
class LoginBodySchema(BaseSchema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class SignupBodySchema(BaseSchema):
    username = fields.String(validate=validate.Length(min=1), required=True)
    email = fields.Email(required=True)
    password = custom_fields.HashedPasswordField(required=True)


class EmailVerificationBodySchema(BaseSchema):
    token = fields.String(required=True)


login_body_schema = LoginBodySchema()
signup_body_schema = SignupBodySchema()
email_validation_body_schema = EmailVerificationBodySchema()

# ---- OUTPUTS ----

class CurrentUserOutputSchema(BaseSchema):
    id = fields.Integer()
    username = fields.String()
    email = fields.Email()
    role = fields.String()
    picture_id = fields.String()
    creation_date = fields.DateTime()

class LoginOutputSchema(BaseSchema):
    token = fields.String()
    user = fields.Nested(CurrentUserOutputSchema)


current_user_output_schema = CurrentUserOutputSchema()
login_output_schema = LoginOutputSchema()