from marshmallow import Schema, fields


class DocumentSchema(Schema):
    id = fields.Integer()
    filename = fields.String()
    content = fields.String()
