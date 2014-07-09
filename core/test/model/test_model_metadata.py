from unittest import TestCase
from core.field.field import Field
from core.model.model import Model
from core.model.model_metadata import ModelMetadataFactory


class TestModelMetadataFactory(TestCase):
    def test_create_model_metadata(self):
        test_model = TestModel()
        model_metadata = ModelMetadataFactory()

        descriptor = model_metadata.create_table_metadata(test_model)

        self.assertEqual('test_model', descriptor.name)
        self.assertEqual(2, len(descriptor.columns))
        self.assertIn('id', descriptor.columns)
        self.assertEqual('uuid', descriptor.columns['id'])
        self.assertIn('some_text', descriptor.columns)
        self.assertEqual('text', descriptor.columns['some_text'])


class IdField(Field):
    def __init__(self):
        pass

    def field_type(self):
        return 'uuid'


class TextField(Field):
    def __init__(self):
        pass

    def field_type(self):
        return 'text'


class TestModel(Model):
    id = IdField()
    some_text = TextField()
