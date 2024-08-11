from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class ChatSchema(Schema):
    id = fields.Integer(dump_only=True)
    is_group = fields.Boolean(required=True)
    group_name = fields.String(validate=validate.Length(min=1), required=False)
    creation_date = fields.DateTime(required=False, dump_only=True)

    @validates_schema
    def validate_group_name_set(self, data, **kwargs):
        if data.get("is_group") is False and data.get("group_name"):
            raise ValidationError("The chat is not a group.", "group_name")


chat_schema = ChatSchema()
chats_schema = ChatSchema(many=True)