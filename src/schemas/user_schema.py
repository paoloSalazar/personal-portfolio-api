from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    second_last_name = fields.Str(required=False, allow_none=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    about_me = fields.Str(required=False, allow_none=True)
    profile_photo_url = fields.Str(required=False, allow_none=True)