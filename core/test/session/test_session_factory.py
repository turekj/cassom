# -*- coding: utf-8 -*-

from unittest import TestCase
from core.config.cassandra_config import CassandraConfig
from core.session.session_factory import SessionFactory


class TestSessionFactory(TestCase):
    def test_create_session(self):
        config = CassandraConfig()
        config.contact_points = ['127.0.0.1']
        session_factory = SessionFactory(config)
        session = session_factory.create_session()

        session.execute(
            "CREATE KEYSPACE test_keyspace WITH replication = {'class':'SimpleStrategy', 'replication_factor':3};")
        session.execute("CREATE TABLE test_keyspace.users (id uuid PRIMARY KEY, name text, surname text);")
        session.execute("INSERT INTO test_keyspace.users (id, name, surname) VALUES (756716f7-2e54-4715-9f00-91dcbea6cf50, 'Jan', 'Brzoza');")
        result = session.execute("SELECT name, surname FROM test_keyspace.users;")
        session.execute("DROP KEYSPACE test_keyspace;")

        self.assertEqual(len(result), 1)
        self.assertEqual('Jan', result[0].name)
        self.assertEqual('Brzoza', result[0].surname)
