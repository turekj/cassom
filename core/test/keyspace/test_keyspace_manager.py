from unittest import TestCase
from core.config.cassandra_config import CassandraConfig
from core.config.keyspace_config import KeyspaceConfig
from core.engine.engine import Engine
from core.keyspace.keyspace_manager import KeyspaceManager
from core.session.session_factory import SessionFactory


class TestKeyspaceManager(TestCase):
    def test_keyspace_operations(self):
        engine = Engine.create_engine('cassandra://127.0.0.1/TestKeyspace')
        manager = KeyspaceManager()

        initial_has_keyspace = manager.check_keyspace_exists(engine, engine.get_keyspace())
        manager.create_keyspace(engine, engine.get_keyspace())
        after_created_has_keyspace = manager.check_keyspace_exists(engine, engine.get_keyspace())
        manager.drop_keyspace(engine, engine.get_keyspace())
        after_drop_has_keyspace = manager.check_keyspace_exists(engine, engine.get_keyspace())

        self.assertFalse(initial_has_keyspace)
        self.assertTrue(after_created_has_keyspace)
        self.assertFalse(after_drop_has_keyspace)
