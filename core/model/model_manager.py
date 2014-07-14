from utilities.string.string_utilities import StringUtilities


class ModelManager(object):
    def __init__(self, cls):
        self.cls = cls
        self.fields = []
        self.engine = None
        self.table_manager = None

    def add_field(self, name, field):
        self.fields.append((name, field))

    def _table_name(self):
        return StringUtilities.convert_to_underscore(self.cls.__name__)

    def save(self, model_instance):
        column_values = {}

        for field_name, field in self.fields:
            column_values.update(field.values_to_persist(model_instance, field_name))

        self.table_manager.insert_into_table(self.engine, self._table_name(), column_values)

    def create(self):
        return self.cls()

    def find(self, **kwargs):
        results = self.table_manager.select_from_table(self.engine, self._table_name(), kwargs)
        instances = []

        for result in results:
            instance = self.create()

            for field_name, field in self.fields:
                field.update_from_persisted_values(instance, result.__dict__, field_name)

            instances.append(instance)

        if len(instances) > 1:
            return instances

        return instances[0]
