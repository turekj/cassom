from core.field.field import Field
from utilities.string.string_utilities import StringUtilities


class ModelMetadata(object):
    def __init__(self):
        self.table_metadata = {}

    def __getitem__(self, item):
        return self.table_metadata[item]

    def __setitem__(self, key, value):
        self.table_metadata[key] = value

    def __iter__(self):
        return self.table_metadata.iterkeys()


class TableMetadata(object):
    def __init__(self):
        self.name = ''
        self.columns = {}
        self.primary_key = []


class ModelMetadataFactory(object):
    def create_table_metadata(self, model):
        descriptor = TableMetadata()
        descriptor.name = StringUtilities.convert_to_underscore(model.__name__)

        fields = dir(model)

        for field in fields:
            value = getattr(model, field)

            if isinstance(value, Field):
                descriptor.columns[field] = value.field_type()

                if value.is_primary_key():
                    descriptor.primary_key.append(field)

        if len(descriptor.primary_key) == 0:
            descriptor.columns['id'] = 'uuid'
            descriptor.primary_key.append('id')

        return descriptor
