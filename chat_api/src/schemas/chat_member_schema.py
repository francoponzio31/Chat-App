from marshmallow import Schema, fields
from schemas.user_schema import UserSchema


class ChatMemberSchema(Schema):
    id = fields.Integer(dump_only=True)
    chat_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    user = fields.Nested(UserSchema, dump_only=True, skip_if=None)
    joined_date = fields.DateTime(required=False, dump_only=True)


chat_member_schema = ChatMemberSchema()
chat_members_schema = ChatMemberSchema(many=True)