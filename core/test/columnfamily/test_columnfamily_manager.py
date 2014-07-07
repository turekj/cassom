from unittest.case import TestCase
from core.columnfamily.columnfamily_descriptor import ColumnfamilyDescriptor, ColumnDescriptor
from core.columnfamily.columnfamily_manager import ColumnfamilyManager
from core.config.cassandra_config import CassandraConfig
from core.keyspace.keyspace_manager import KeyspaceManager
from core.session.session_factory import SessionFactory


class TestColumnfamilyManager(TestCase):
    def setUp(self):
        self.config = CassandraConfig()
        self.config.contact_points = ['127.0.0.1']
        self.config.keyspace.name = 'test_keyspace'
        self.config.keyspace.replication_class = 'SimpleStrategy'
        self.config.keyspace.replication_factor = 3
        self.session = SessionFactory(self.config).create_session()
        self.keyspace_manager = KeyspaceManager()
        self.keyspace_manager.create_keyspace(self.session, self.config.keyspace)

    def test_columnfamily_operations(self):
        columnfamily_descriptor = ColumnfamilyDescriptor()
        columnfamily_descriptor.keyspace = self.config.keyspace.name
        columnfamily_descriptor.name = 'test_columnfamily'
        columnfamily_descriptor.columns = [ColumnDescriptor('id', 'uuid'),
                                           ColumnDescriptor('name', 'text'),
                                           ColumnDescriptor('surname', 'text')]
        columnfamily_descriptor.primary_key = ['id']
        columnfamily_manager = ColumnfamilyManager()

        exists_initial = columnfamily_manager.check_column_family_exists(self.session,
                                                                         columnfamily_descriptor.keyspace,
                                                                         columnfamily_descriptor.name)

        columnfamily_manager.create_columnfamily(self.session, columnfamily_descriptor)

        exists_after_create = columnfamily_manager.check_column_family_exists(self.session,
                                                                              columnfamily_descriptor.keyspace,
                                                                              columnfamily_descriptor.name)

        columnfamily_manager.drop_columnfamily(self.session,
                                               columnfamily_descriptor.keyspace,
                                               columnfamily_descriptor.name)

        exists_after_drop = columnfamily_manager.check_column_family_exists(self.session,
                                                                            columnfamily_descriptor.keyspace,
                                                                            columnfamily_descriptor.name)

        self.assertFalse(exists_initial)
        self.assertTrue(exists_after_create)
        self.assertFalse(exists_after_drop)

    def tearDown(self):
        self.keyspace_manager.drop_keyspace(self.session, self.config.keyspace.name)