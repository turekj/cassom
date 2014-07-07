class KeyspaceManager(object):
    def __init__(self):
        pass

    def create_keyspace(self, session, keyspace_settings):
        session.execute(self._create_keyspace_str(keyspace_settings))

    def check_keyspace_exists(self, session, name):
        session.execute("USE SYSTEM;")
        result = session.execute("SELECT * FROM schema_keyspaces WHERE keyspace_name = '{0}';".format(name))
        return len(result) > 0

    def drop_keyspace(self, session, name):
        session.execute("DROP KEYSPACE {0};".format(name))

    def _create_keyspace_str(self, keyspace_settings):
        return "CREATE KEYSPACE {0} WITH replication = {{'class': '{1}', 'replication_factor': {2}}};".format(
            keyspace_settings.name,
            keyspace_settings.replication_class,
            keyspace_settings.replication_factor)
