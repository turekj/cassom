from unittest.case import TestCase
from core.keyspace.keyspace_manager import KeyspaceManager
from core.model.model_metadata import TableMetadata
from core.table.table_manager import TableManager
from core.engine.engine import Engine


class TestTableManager(TestCase):
    def setUp(self):
        self.engine = Engine.create_engine('cassandra://127.0.0.1/TestKeyspace')
        self.keyspace_manager = KeyspaceManager()
        self.keyspace_manager.create_keyspace(self.engine, self.engine.get_keyspace())

    def test_table_operations(self):
        metadata = TableMetadata()
        metadata.name = 'test_table'
        metadata.columns = {'id': 'uuid', 'name': 'text', 'surname': 'text'}
        metadata.primary_key = ['id']
        table_manager = TableManager()

        exists_initial = table_manager.check_table_exists(self.engine, metadata.name)
        table_manager.create_table(self.engine, metadata)
        exists_after_create = table_manager.check_table_exists(self.engine, metadata.name)
        table_manager.drop_table(self.engine, metadata.name)
        exists_after_drop = table_manager.check_table_exists(self.engine, metadata.name)

        self.assertFalse(exists_initial)
        self.assertTrue(exists_after_create)
        self.assertFalse(exists_after_drop)

    def tearDown(self):
        self.keyspace_manager.drop_keyspace(self.engine, self.engine.get_keyspace())
