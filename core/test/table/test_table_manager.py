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

    def test_insert_into_table(self):
        metadata = TableMetadata()
        metadata.name = 'test_table'
        metadata.columns = {'id': 'uuid', 'name': 'text', 'surname': 'text'}
        metadata.primary_key = ['id']
        table_manager = TableManager()
        first_row = {'id': '550e8400-e29b-41d4-a716-446655440000', 'name': "'Jan'", 'surname': "'Kowalski'"}
        second_row = {'id': 'f47ac10b-58cc-4372-a567-0e02b2c3d479', 'name': "'Krzysztof'", 'surname': "'Nowak'"}

        table_manager.create_table(self.engine, metadata)
        table_manager.insert_into_table(self.engine, metadata.name, first_row)
        table_manager.insert_into_table(self.engine, metadata.name, second_row)
        first_row = self.engine.execute_query('SELECT * FROM test_keyspace.test_table WHERE id=550e8400-e29b-41d4-a716-446655440000;')
        second_row = self.engine.execute_query('SELECT * FROM test_keyspace.test_table WHERE id=f47ac10b-58cc-4372-a567-0e02b2c3d479;')
        table_manager.drop_table(self.engine, metadata.name)

        self.assertIsNotNone(first_row)
        self.assertEqual(1, len(first_row))
        self.assertEqual('Jan', first_row[0].name)
        self.assertEqual('Kowalski', first_row[0].surname)
        self.assertIsNotNone(second_row)
        self.assertEqual(1, len(second_row))
        self.assertEqual('Krzysztof', second_row[0].name)
        self.assertEqual('Nowak', second_row[0].surname)

    def tearDown(self):
        self.keyspace_manager.drop_keyspace(self.engine, self.engine.get_keyspace())
