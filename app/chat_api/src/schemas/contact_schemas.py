from marshmallow import Schema, fields, validates_schema, ValidationError
from schemas.user_schemas import UserOutputSchema


# ---- INPUTS ----
class ContactBodySchema(Schema):
    user_id = fields.Integer(required=True)
    contact_user_id = fields.Integer(required=True)

    @validates_schema
    def validate_user_and_contact(self, data, **kwargs):
        if data["user_id"] == data["contact_user_id"]:
            raise ValidationError("User and contact must be different.", "contact")


contact_body_schema = ContactBodySchema()

# ---- OUTPUTS ----
class ContactOutputSchema(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    contact_user = fields.Nested(UserOutputSchema)
    added_date = fields.DateTime()


contact_output_schema = ContactOutputSchema()
contacts_output_schema = ContactOutputSchema(many=True)