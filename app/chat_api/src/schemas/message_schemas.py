from marshmallow import Schema, fields
from schemas.user_schemas import UserOutputSchema


# ---- INPUTS ----
class MessageBodySchema(Schema):
    chat_id = fields.Integer(required=True)
    sender_user_id = fields.Integer(required=True)
    content = fields.String(required=True)


message_body_schema = MessageBodySchema()

# ---- OUTPUTS ----
class MessageOutputSchema(Schema):
    id = fields.Integer()
    chat_id = fields.Integer()
    sender_user = fields.Nested(UserOutputSchema)
    content = fields.String()
    sent_date = fields.DateTime()


message_output_schema = MessageOutputSchema()
messages_output_schema = MessageOutputSchema(many=True)
