class TableManager(object):
    def __init__(self):
        self.check_query = "SELECT * FROM System.schema_columnfamilies WHERE keyspace_name = '{0}' AND columnfamily_name = '{1}';"
        self.create_query = "CREATE TABLE {0}.{1} ({2}, PRIMARY KEY ({3}));"
        self.drop_query = "DROP TABLE {0}.{1};"
        self.insert_query = "INSERT INTO {0}.{1} ({2}) VALUES({3});"

    def check_table_exists(self, engine, table_name):
        result = engine.execute_query(self.check_query.format(engine.get_keyspace(), table_name))
        return len(result) > 0

    def create_table(self, engine, metadata):
        if len(metadata.primary_key) > 0:
            engine.execute_query(self._create_table_str(engine.get_keyspace(), metadata))
        else:
            raise AttributeError('No primary key defined for model ' + metadata.name)

    def _create_table_str(self, keyspace, metadata):
        return self.create_query.format(keyspace,
                                        metadata.name,
                                        ", ".join(map(lambda (x, y): x + ' ' + y, metadata.columns.iteritems())),
                                        ",".join(metadata.primary_key))

    def drop_table(self, engine, table_name):
        engine.execute_query(self.drop_query.format(engine.get_keyspace(), table_name))

    def insert_into_table(self, engine, table_name, column_values):
        col_val_items = column_values.items()
        cols = map(lambda (c, v): c, col_val_items)
        vals = map(lambda (c, v): v, col_val_items)
        engine.execute_query(self.insert_query.format(engine.get_keyspace(),
                                                      table_name,
                                                      ",".join(cols),
                                                      ",".join(vals)))

    def select_from_table(self, engine, table_name, where_clause):
        pass

