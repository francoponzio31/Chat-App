from marshmallow import fields, ValidationError
from utilities.utils import hash_password
import base64


class HashedPassword(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        if value:
            return hash_password(value)
        return value


class Base64encodedField(fields.Field):

    def _deserialize(self, value, attr, data, **kwargs):
        """
        Decode the b64 content to bytes
        """
        if value is None:
            raise ValidationError("Field may not be null")
        try:
            return base64.b64decode(value)
        except Exception:
            raise ValidationError("Invalid base64 string")

    def _serialize(self, value, attr, obj, **kwargs):
        return value
