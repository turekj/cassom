from core.config.keyspace_config import KeyspaceConfig


class CassandraConfig(object):
    def __init__(self):
        self.contact_points = []
        self.keyspace = KeyspaceConfig()
