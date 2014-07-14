class ModelManager(object):
    def __init__(self, table_name):
        self.table_name = table_name
        self.fields = []

    def add_field(self, name, field):
        self.fields.append((name, field))

    def save(self, engine, table_manager, model_instance):
        column_values = {}

        for field_name, field in self.fields:
            column_values.update(field.values_to_persist(model_instance, field_name))

        table_manager.insert_into_table(engine, self.table_name, column_values)
