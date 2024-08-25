from marshmallow import Schema, fields
from schemas.user_schemas import UserOutputSchema


# ---- INPUTS ----
class ChatMemberBodySchema(Schema):
    chat_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)


chat_member_body_schema = ChatMemberBodySchema()

# ---- OUTPUTS ----
class ChatMemberOutputSchema(Schema):
    id = fields.Integer()
    chat_id = fields.Integer()
    user = fields.Nested(UserOutputSchema)
    joined_date = fields.DateTime()


chat_member_output_schema = ChatMemberOutputSchema()
chat_members_output_schema = ChatMemberOutputSchema(many=True)