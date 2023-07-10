from marshmallow import Schema, fields


class PhoneSchema(Schema):
    id = fields.Integer(dump_only=True)
    number = fields.String(required=True)


class EmailSchema(Schema):
    id = fields.Integer(dump_only=True)
    email = fields.String(required=True)


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    lastName = fields.String(required=True)
    firstName = fields.String(required=True)
    emails = fields.List(fields.Nested(EmailSchema()), required=True)
    phoneNumbers = fields.List(fields.Nested(PhoneSchema()), required=True)