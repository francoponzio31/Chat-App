from marshmallow import Schema, fields, validates_schema, ValidationError
from schemas.user_schema import UserSchema


class ContactSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    contact_user_id = fields.Integer(required=True)
    contact_user = fields.Nested(UserSchema, dump_only=True)
    added_date = fields.DateTime(required=False, dump_only=True)

    @validates_schema
    def validate_user_and_contact(self, data, **kwargs):
        if data["user_id"] == data["contact_user_id"]:
            raise ValidationError("User and contact must be different.", "contact")


contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)