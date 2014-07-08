from inspect import getmembers
from core.columnfamily.columnfamily_descriptor import ColumnfamilyDescriptor, ColumnDescriptor
from core.field.field import Field
from core.model.model import Model
from utilities.string.string_utilities import StringUtilities


class DescriptorFactory(object):
    def __init__(self):
        pass

    def create_descriptor(self, model):
        if isinstance(model, Model):
            descriptor = ColumnfamilyDescriptor()
            descriptor.name = StringUtilities.convert_to_underscore(type(model).__name__)

            fields = dir(model)

            for field in fields:
                value = getattr(model, field)

                if isinstance(value, Field):
                    field_descriptor = ColumnDescriptor()
                    field_descriptor.name = field
                    field_descriptor.data_type = value.field_type()

                    descriptor.columns.append(field_descriptor)

            return descriptor
