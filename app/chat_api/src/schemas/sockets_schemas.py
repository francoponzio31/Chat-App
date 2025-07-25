from schemas.base_schema import BaseSchema
from marshmallow import fields


class JoinChatEventSchema(BaseSchema):
    chat_id = fields.Integer(required=True)

class CreateChatEventSchema(BaseSchema):
    chat_id = fields.Integer(required=True)
    chat_members = fields.List(fields.Integer(), required=True)

class ChatCreatedEventSchema(BaseSchema):
    chat_id = fields.Integer(required=True)
    chat_members = fields.List(fields.Integer(), required=True)

join_chat_event_schema = JoinChatEventSchema()
create_chat_event_schema = CreateChatEventSchema()
chat_created_event_schema = ChatCreatedEventSchema()
