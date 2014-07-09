from unittest import TestCase
from core.engine.engine import Engine
from core.field.fields import IdField, TextField, PasswordField
from core.model.model import Model


class TestModel(TestCase):
    def test_bind(self):
        table_test_query = "SELECT * FROM system.schema_columnfamilies WHERE keyspace_name='{0}' AND columnfamily_name='{1}';"
        column_test_query = "SELECT * FROM system.schema_columns WHERE keyspace_name='{0}' AND columnfamily_name='{1}' AND column_name='{2}';"
        engine = Engine.create_engine('cassandra://127.0.0.1/TestKeyspace')
        Model.bind(engine)

        test_model_exists = engine.execute_query(table_test_query.format('test_keyspace', 'example_model'))
        another_test_model_exists = engine.execute_query(
            table_test_query.format('test_keyspace', 'another_example_model'))
        test_model_id_exists = engine.execute_query(column_test_query.format('test_keyspace', 'example_model', 'id'))
        test_model_test_text_exists = engine.execute_query(
            column_test_query.format('test_keyspace', 'example_model', 'test_text'))
        another_test_model_id_exists = engine.execute_query(
            column_test_query.format('test_keyspace', 'another_example_model', 'id'))
        another_test_model_user_exists = engine.execute_query(
            column_test_query.format('test_keyspace', 'another_example_model', 'user'))
        another_test_model_password_exists = engine.execute_query(
            column_test_query.format('test_keyspace', 'another_example_model', 'password'))
        engine.execute_query('DROP KEYSPACE test_keyspace;')

        self.assertTrue(len(test_model_exists) > 0)
        self.assertTrue(len(another_test_model_exists) > 0)
        self.assertTrue(len(test_model_id_exists) > 0)
        self.assertTrue(len(test_model_test_text_exists) > 0)
        self.assertTrue(len(another_test_model_id_exists) > 0)
        self.assertTrue(len(another_test_model_user_exists) > 0)
        self.assertTrue(len(another_test_model_password_exists) > 0)


class ExampleModel(Model):
    id = IdField(primary_key=True)
    test_text = TextField()


class AnotherExampleModel(Model):
    id = IdField(primary_key=True)
    user = TextField()
    password = PasswordField()
