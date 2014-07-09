class KeyspaceManager(object):
    def __init__(self):
        self.create_query = "CREATE KEYSPACE {0} WITH REPLICATION = {{'class': '{1}', 'replication_factor': {2}}};"
        self.exists_query = "SELECT * FROM SYSTEM.schema_keyspaces WHERE keyspace_name = '{0}';"
        self.drop_query = "DROP KEYSPACE {0};"

    def create_keyspace(self, engine, name):
        engine.execute_query(self.create_query.format(name, 'SimpleStrategy', '3'))

    def check_keyspace_exists(self, engine, name):
        result = engine.execute_query(self.exists_query.format(name))
        return len(result) > 0

    def drop_keyspace(self, engine, name):
        engine.execute_query(self.drop_query.format(name))
