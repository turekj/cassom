from unittest import TestCase
from core.engine.engine import Engine


class TestEngine(TestCase):
    def test_create_config(self):
        engine_with_port = Engine()
        engine_with_port.create_config('cassandra://127.0.0.1:9170/TestKeyspace')
        engine_without_port = Engine()
        engine_without_port.create_config('cassandra://127.0.0.1/TestKeyspace')

        self.assertEqual('127.0.0.1', engine_with_port.configuration.contact_point)
        self.assertEqual(9170, engine_with_port.configuration.port)
        self.assertEqual('TestKeyspace', engine_with_port.configuration.keyspace_name)
        self.assertEqual('127.0.0.1', engine_without_port.configuration.contact_point)
        self.assertIsNone(engine_without_port.configuration.port)
        self.assertEqual('TestKeyspace', engine_without_port.configuration.keyspace_name)

    def test_execute_query(self):
        engine = Engine.create_engine('cassandra://127.0.0.1/TestKeyspace')

        engine.execute_query(
            "CREATE KEYSPACE test_keyspace WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 3};")
        engine.execute_query("CREATE TABLE test_keyspace.users (id uuid PRIMARY KEY, name text, surname text);")
        engine.execute_query("INSERT INTO test_keyspace.users (id, name, surname) VALUES (756716f7-2e54-4715-9f00-91dcbea6cf50, 'Jan', 'Brzoza');")
        result = engine.execute_query("SELECT name, surname FROM test_keyspace.users;")
        engine.execute_query("DROP TABLE test_keyspace.users;")
        engine.execute_query("DROP KEYSPACE test_keyspace;")

        self.assertEqual(1, len(result))
        self.assertEqual('Jan', result[0].name)
        self.assertEqual('Brzoza', result[0].surname)
