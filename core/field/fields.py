from core.field.field import Field


class IdField(Field):
    def table_columns(self, field_name):
        return {field_name: 'uuid'}


class TextField(Field):
    def table_columns(self, field_name):
        return {field_name: 'text'}


class PasswordField(Field):
    def table_columns(self, field_name):
        return {field_name: 'text'}


class TimestampField(Field):
    def table_columns(self, field_name):
        return {field_name: 'timestamp'}
