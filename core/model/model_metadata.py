from core.field.field import Field
from core.model.model import Model
from utilities.string.string_utilities import StringUtilities


class ModelMetadata(object):
    def __init__(self):
        self.name = ''
        self.columns = {}
        self.primary_key = ''


class ModelMetadataFactory(object):
    def create_model_metadata(self, model):
        if isinstance(model, Model):
            descriptor = ModelMetadata()
            descriptor.name = StringUtilities.convert_to_underscore(type(model).__name__)

            fields = dir(model)

            for field in fields:
                value = getattr(model, field)

                if isinstance(value, Field):
                    descriptor.columns[field] = value.field_type()

            return descriptor
