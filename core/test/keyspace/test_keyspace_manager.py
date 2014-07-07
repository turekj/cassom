from unittest import TestCase
from core.config.cassandra_config import CassandraConfig
from core.config.keyspace_config import KeyspaceConfig
from core.keyspace.keyspace_manager import KeyspaceManager
from core.session.session_factory import SessionFactory


class TestKeyspaceManager(TestCase):
    def test_create_keyspace_str(self):
        settings = KeyspaceConfig()
        settings.name = 'test_keyspace'
        settings.replication_class = 'SimpleStrategy'
        settings.replication_factor = 3
        manager = KeyspaceManager()

        create_keyspace_str = manager._create_keyspace_str(settings)

        self.assertEqual(
            "CREATE KEYSPACE test_keyspace WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 3};",
            create_keyspace_str)

    def test_keyspace_operations(self):
        config = CassandraConfig()
        config.contact_points = ['127.0.0.1']
        config.keyspace.name = 'test_keyspace'
        config.keyspace.replication_class = 'SimpleStrategy'
        config.keyspace.replication_factor = 3
        session = SessionFactory(config).create_session()
        manager = KeyspaceManager()

        initial_has_keyspace = manager.check_keyspace_exists(session, config.keyspace.name)
        manager.create_keyspace(session, config.keyspace)
        after_created_has_keyspace = manager.check_keyspace_exists(session, config.keyspace.name)
        manager.drop_keyspace(session, config.keyspace.name)
        after_drop_has_keyspace = manager.check_keyspace_exists(session, config.keyspace.name)

        self.assertFalse(initial_has_keyspace)
        self.assertTrue(after_created_has_keyspace)
        self.assertFalse(after_drop_has_keyspace)
