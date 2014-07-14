import re
from core.field.field import Field


class IdField(Field):
    def __init__(self, primary_key_gravity=-1):
        self.primary_key = True
        self.primary_key_gravity = primary_key_gravity
        self.id_regex = re.compile('^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}$')

    def table_columns(self, field_name):
        return {field_name: 'uuid'}

    def values_to_persist(self, model, field_name):
        value = getattr(model, field_name)

        if isinstance(value, str):
            if self.id_regex.match(value):
                return {field_name: value}

        raise AttributeError('ID not parseable')

    def update_from_persisted_values(self, model, table_values, field_name):
        setattr(model, field_name, str(table_values[field_name]))


class TextField(Field):
    def table_columns(self, field_name):
        return {field_name: 'text'}

    def values_to_persist(self, model, field_name):
        value = getattr(model, field_name)

        if isinstance(value, str):
            return {field_name: "'" + value + "'"}

        raise AttributeError('Could not map non-string value to TextField')


class PasswordField(Field):
    def table_columns(self, field_name):
        return {field_name: 'text'}


class TimestampField(Field):
    def table_columns(self, field_name):
        return {field_name: 'timestamp'}
