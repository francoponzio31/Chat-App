from marshmallow import Schema, fields, validate
from schemas import custom_fields


# ---- INPUTS ----
class UserBodySchema(Schema):
    username = fields.String(validate=validate.Length(min=1), required=True)
    email = fields.Email(required=True)
    password = custom_fields.HashedPassword(required=True)


class PictureBodySchema(Schema):
    filename = fields.String(required=True)
    content = custom_fields.Base64encodedField(required=True)


class UserSearchParamsSchema(Schema):
    limit = fields.Integer(required=False)
    offset = fields.Integer(required=False)
    username = fields.String(required=False)


user_body_schema = UserBodySchema()
picture_body_schema = PictureBodySchema()
user_search_params_schema = UserSearchParamsSchema()

# ---- OUTPUTS ----
class UserOutputSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    email = fields.Email()
    role = fields.String()
    picture_id = fields.UUID()
    creation_date = fields.DateTime()


user_output_schema = UserOutputSchema()
users_output_schema = UserOutputSchema(many=True)