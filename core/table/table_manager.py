class TableManager(object):
    def __init__(self):
        self.check_query = "SELECT * FROM System.schema_columnfamilies WHERE keyspace_name = '{0}' AND columnfamily_name = '{1}';"
        self.create_query = "CREATE TABLE {0}.{1} ({2}, PRIMARY KEY ({3}));"
        self.drop_query = "DROP TABLE {0}.{1};"

    def check_table_exists(self, engine, table_name):
        result = engine.execute_query(self.check_query.format(engine.get_keyspace(), table_name))
        return len(result) > 0

    def create_table(self, engine, metadata):
        engine.execute_query(self._create_table_str(engine.get_keyspace(), metadata))

    def _create_table_str(self, keyspace, metadata):
        return self.create_query.format(keyspace,
                                        metadata.name,
                                        ", ".join(map(lambda (x, y): x + ' ' + y, metadata.columns.iteritems())),
                                        ",".join(metadata.primary_key))

    def drop_table(self, engine, table_name):
        engine.execute_query(self.drop_query.format(engine.get_keyspace(), table_name))
