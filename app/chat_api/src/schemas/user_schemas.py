from schemas.base_schema import BaseSchema
from marshmallow import fields, validate
from schemas import custom_fields


# ---- INPUTS ----
class UserSearchParamsSchema(BaseSchema):
    limit = fields.Integer(required=False)
    offset = fields.Integer(required=False)
    username = fields.String(required=False)
    is_verified = fields.Boolean(required=False)
    exclude_users = custom_fields.DelimitedListField(fields.Integer(), required=False)


class UserBodySchema(BaseSchema):
    username = fields.String(validate=validate.Length(min=1), required=True)
    email = fields.Email(required=True)
    password = custom_fields.HashedPasswordField(required=True)


class PictureBodySchema(BaseSchema):
    filename = fields.String(required=True)
    content = custom_fields.Base64encodedField(required=True)


user_body_schema = UserBodySchema()
picture_body_schema = PictureBodySchema()
user_search_params_schema = UserSearchParamsSchema()

# ---- OUTPUTS ----
class UserOutputSchema(BaseSchema):
    id = fields.Integer()
    username = fields.String()
    email = fields.Email()
    role = fields.String()
    picture_id = fields.UUID()
    is_verified = fields.Boolean()
    creation_date = fields.DateTime()


user_output_schema = UserOutputSchema()
users_output_schema = UserOutputSchema(many=True)