from core.field.field import Field


class TextField(Field):
    def field_type(self):
        return 'text'


class PasswordField(Field):
    def field_type(self):
        return 'text'


class TimestampField(Field):
    def field_type(self):
        return 'timestamp'
