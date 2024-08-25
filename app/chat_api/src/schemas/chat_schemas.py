from marshmallow import Schema, fields, validate, validates_schema, ValidationError


# ---- INPUTS ----
class ChatBodySchema(Schema):
    is_group = fields.Boolean(required=True)
    group_name = fields.String(validate=validate.Length(min=1), required=False, default=None)

    @validates_schema
    def validate_group_name_set(self, data, **kwargs):
        if data.get("is_group") is False and data.get("group_name"):
            raise ValidationError("The chat is not a group.", "group_name")
        
        if self.context.get("updating") and "is_group" in data:
            raise ValidationError("The field is_group is read-only and cannot be modified", "group_name")


create_chat_body_schema = ChatBodySchema()
update_chat_body_schema = ChatBodySchema(context={"updating": True})

# ---- OUTPUTS ----
class ChatOutputSchema(Schema):
    id = fields.Integer()
    is_group = fields.Boolean()
    group_name = fields.String()
    creation_date = fields.DateTime()


chat_output_schema = ChatOutputSchema()
chats_output_schema = ChatOutputSchema(many=True)