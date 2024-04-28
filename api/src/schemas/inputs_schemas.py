from marshmallow import Schema, fields
from schemas import custom_fields


class PictureSchema(Schema):
    filename = fields.String(required=True)
    content = custom_fields.Base64encodedField(required=True)

picture_schema = PictureSchema()