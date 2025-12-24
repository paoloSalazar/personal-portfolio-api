from marshmallow import Schema, fields

class ResumeSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    title = fields.Str(required=True)
    summary = fields.Str(required=False, allow_none=True)
    education = fields.Str(required=False, allow_none=True)
    skills = fields.Str(required=False, allow_none=True)
    start_date = fields.Str(required=False, allow_none=True)
    end_date = fields.Str(required=False, allow_none=True)