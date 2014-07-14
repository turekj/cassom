from core.field.field import Field
from core.model.model_manager import ModelManager
from core.model.model_metadata import ModelMetadata, TableMetadata
from utilities.string.string_utilities import StringUtilities


class ModelTransformator(object):
    def __init__(self):
        pass

    def transform_model(self, cls):
        if not (hasattr(cls, 'metadata') and hasattr(cls, 'managers')):
            cls.metadata = ModelMetadata()
            cls.managers = {}
            return

        table_name = StringUtilities.convert_to_underscore(cls.__name__)
        field_names = filter(lambda x: isinstance(getattr(cls, x), Field), dir(cls))
        table_columns = dict()
        primary_keys = dict()

        for field_name in field_names:
            field = getattr(cls, field_name)
            table_columns = dict(table_columns.items() + field.table_columns(field_name).items())
            primary_keys = dict(primary_keys.items() + field.primary_keys(field_name).items())
            field.model_transformation(cls, field_name)

            if table_name not in cls.managers:
                cls.managers[table_name] = ModelManager(cls)

            cls.managers[table_name].add_field(field_name, field)

        table_metadata = TableMetadata()
        table_metadata.name = table_name
        table_metadata.columns = table_columns
        gravity_sorted_primary_keys = sorted(primary_keys.items(), key=lambda pk: pk[1], reverse=True)
        table_metadata.primary_key = map(lambda (x, y): x, gravity_sorted_primary_keys)

        cls.metadata[table_name] = table_metadata

