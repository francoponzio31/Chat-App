from marshmallow import fields
from utilities.utils import hash_password


class HashedPassword(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        if value:
            return hash_password(value)
        return value
