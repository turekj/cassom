from core.field.field import Field
from utilities.string.string_utilities import StringUtilities


class ModelMetadata(object):
    def __init__(self):
        self.table_metadata = {}

    def __getitem__(self, item):
        return self.table_metadata[item]

    def __setitem__(self, key, value):
        self.table_metadata[key] = value

    def populate(self):
        for table in self.table_metadata:
            print 'populating metadata for table %s' % table


class TableMetadata(object):
    def __init__(self):
        self.name = ''
        self.columns = {}
        self.primary_key = ''


class ModelMetadataFactory(object):
    def create_table_metadata(self, model):
        descriptor = TableMetadata()
        descriptor.name = StringUtilities.convert_to_underscore(type(model).__name__)

        fields = dir(model)

        for field in fields:
            value = getattr(model, field)

            if isinstance(value, Field):
                descriptor.columns[field] = value.field_type()

        return descriptor
