import humps
from marshmallow import Schema, pre_load, post_dump


class BaseSchema(Schema):

    @pre_load
    def decamelize_input(self, data, **kwargs):
        return humps.decamelize(data)
    
    @post_dump
    def camelize_output(self, data, **kwargs):
        return humps.camelize(data)