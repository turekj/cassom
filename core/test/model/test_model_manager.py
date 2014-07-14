from unittest import TestCase
from core.engine.engine import Engine
from core.field.fields import TextField, IdField
from core.model.model import Model


class TestModelManager(TestCase):
    def setUp(self):
        class TestModelManagerModel(Model):
            id = IdField()
            some_example_text = TextField()

        self.model = TestModelManagerModel
        self.engine = Engine.create_engine('cassandra://127.0.0.1/TestKeyspace')
        Model.bind(self.engine)

    def test_find(self):
        instance = self.model.objects().create()
        instance.id = '550e8400-e29b-41d4-a716-446655440000'
        instance.some_example_text = 'some text is here'
        instance.save()

        result = self.model.objects().find(id='550e8400-e29b-41d4-a716-446655440000')

        self.assertIsNotNone(result)
        self.assertIsInstance(result, self.model)
        self.assertEqual('550e8400-e29b-41d4-a716-446655440000', result.id)
        self.assertEqual('some text is here', result.some_example_text)

    def tearDown(self):
        del Model.registry['TestModelManagerModel']
        self.engine.execute_query('DROP KEYSPACE test_keyspace;')
