import humps
from marshmallow import Schema, pre_load


class BaseSchema(Schema):

    @pre_load
    def decamelize_input(self, data, **kwargs):
        return humps.decamelize(data)