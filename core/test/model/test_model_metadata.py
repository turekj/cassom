from unittest import TestCase
from core.field.fields import IdField, TextField
from core.model.model_metadata import ModelMetadataFactory


class TestModelMetadataFactory(TestCase):
    def test_create_model_metadata(self):
        model_metadata = ModelMetadataFactory()

        descriptor = model_metadata.create_table_metadata(SomeTestModel)

        self.assertEqual('some_test_model', descriptor.name)
        self.assertEqual(2, len(descriptor.columns))
        self.assertIn('id', descriptor.columns)
        self.assertEqual('uuid', descriptor.columns['id'])
        self.assertIn('some_text', descriptor.columns)
        self.assertEqual('text', descriptor.columns['some_text'])


class SomeTestModel(object):
    id = IdField()
    some_text = TextField()
