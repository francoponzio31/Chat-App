from marshmallow import Schema, fields
from schemas.user_schema import UserSchema


class MessageSchema(Schema):
    id = fields.Integer(dump_only=True)
    chat_id = fields.Integer(required=True)
    sender_user_id = fields.Integer(required=True)
    sender_user = fields.Nested(UserSchema, dump_only=True)
    content = fields.String(required=True)
    sent_date = fields.DateTime(required=False, dump_only=True)


message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)