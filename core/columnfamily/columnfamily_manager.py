class ColumnfamilyManager(object):
    def __init__(self):
        self.check_query = "SELECT * FROM System.schema_columnfamilies WHERE keyspace_name = '{0}' AND columnfamily_name = '{1}';"
        self.create_query = "CREATE TABLE {0}.{1} ({2}, PRIMARY KEY ({3}));"
        self.drop_query = "DROP TABLE {0}.{1};"

    def check_column_family_exists(self, session, keyspace_name, columnfamily_name):
        result = session.execute(self.check_query.format(keyspace_name, columnfamily_name))
        return len(result) > 0

    def create_columnfamily(self, session, columnfamily_descriptor):
        session.execute(self._create_columnfamily_str(columnfamily_descriptor))

    def _create_columnfamily_str(self, columnfamily_descriptor):
        return self.create_query.format(columnfamily_descriptor.keyspace,
                                        columnfamily_descriptor.name,
                                        ", ".join(map(lambda x: str(x), columnfamily_descriptor.columns)),
                                        ",".join(columnfamily_descriptor.primary_key))

    def drop_columnfamily(self, session, keyspace_name, columnfamily_name):
        session.execute(self.drop_query.format(keyspace_name, columnfamily_name))
