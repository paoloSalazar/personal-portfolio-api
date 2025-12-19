from marshmallow import Schema, fields

class UserContactSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    contacttype_id = fields.Int(required=True)
    link_or_number = fields.Str(required=True)