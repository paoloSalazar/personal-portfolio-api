from marshmallow import Schema, fields

class ContactTypeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=False, allow_none=True)