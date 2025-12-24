from marshmallow import Schema, fields

class ResumeSkillSchema(Schema):
    id = fields.Int(dump_only=True)
    resume_id = fields.Int(required=True)
    skill_id = fields.Int(required=True)