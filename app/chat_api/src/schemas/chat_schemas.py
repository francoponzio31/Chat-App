from schemas.base_schema import BaseSchema
from marshmallow import fields, validate, validates_schema, ValidationError


# ---- INPUTS ----
class ChatSearchParamsSchema(BaseSchema):
    limit = fields.Integer(required=False)
    offset = fields.Integer(required=False)
    type = fields.String(
        required=False,
        validate=validate.OneOf(["direct", "group"])
    )


class MessagesSearchParamsSchema(BaseSchema):
    limit = fields.Integer(required=False)
    offset = fields.Integer(required=False)


class ChatBodySchema(BaseSchema):
    is_group = fields.Boolean(required=True)
    group_name = fields.String(validate=validate.Length(min=1), required=False, default=None)
    chat_members_ids = fields.List(fields.Integer(), required=False)

    @validates_schema
    def validate_group_name_set(self, data, **kwargs):
        if data.get("is_group") is False and data.get("group_name"):
            raise ValidationError("The chat is not a group.", "group_name")
        
        if self.context.get("updating") and "is_group" in data:
            raise ValidationError("The field is_group is read-only and cannot be modified", "group_name")
        
    @validates_schema
    def validate_chat_members(self, data, **kwargs):
        if data.get("is_group") is False:
            members = data.get("chat_members_ids", [])
            if len(members) != 2:
                raise ValidationError("A direct chat must have exactly 2 members.", "chat_members_ids")
            

class MessageBodySchema(BaseSchema):
    content = fields.String(required=True)


class MessageReadBodySchema(BaseSchema):
    messages_id = fields.List(fields.Integer())


chats_search_params_schema = ChatSearchParamsSchema()
messages_search_params_schema = MessagesSearchParamsSchema()
create_chat_body_schema = ChatBodySchema()
update_chat_body_schema = ChatBodySchema(context={"updating": True})
message_body_schema = MessageBodySchema()
messages_read_body_schema = MessageReadBodySchema()


# ---- OUTPUTS ----
class UserOutputSchema(BaseSchema):
    id = fields.Integer()
    username = fields.String()
    picture_id = fields.UUID()

class ChatMemberOutputSchema(BaseSchema):
    joined_date = fields.DateTime()
    user = fields.Nested(UserOutputSchema)


class MessageOutputSchema(BaseSchema):
    id = fields.Integer()
    content = fields.String()
    sender_user = fields.Nested(UserOutputSchema)
    read_by_user = fields.Boolean(required=False)
    sent_date = fields.DateTime()


class ChatOutputSchema(BaseSchema):
    id = fields.Integer()
    is_group = fields.Boolean()
    group_name = fields.String()
    chat_members = fields.Nested(ChatMemberOutputSchema, many=True)
    unread_messages = fields.Integer(required=False)
    creation_date = fields.DateTime()


chat_output_schema = ChatOutputSchema()
chats_output_schema = ChatOutputSchema(many=True)
message_output_schema = MessageOutputSchema()
messages_output_schema = MessageOutputSchema(many=True)