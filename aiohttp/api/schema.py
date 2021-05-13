from datetime import datetime

from marshmallow import fields, Schema


class MyDateTimeField(fields.DateTime):
    """
    Кастомный класс для обработки поля datetime
    """

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, datetime):
            return value
        return super()._deserialize(value, attr, data)


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String()
    password = fields.String(required=True, load_only=True)
    email = fields.Email(required=True)
    created = MyDateTimeField(allow_none=None, default=datetime.now())
    is_admin = fields.Boolean(allow_none=None)

    class Meta:
        ordered = True


class AdvertisementSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    description = fields.String(required=True)
    created = MyDateTimeField(allow_none=None, default=datetime.now())
    user_id = fields.Integer()

    class Meta:
        ordered = True
