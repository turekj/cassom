from unittest.case import TestCase
from core.columnfamily.descriptor_factory import DescriptorFactory
from core.field.field import Field
from core.model.model import Model


class TestDescriptorFactory(TestCase):
    def test_create_descriptor(self):
        test_model = TestModel()
        descriptor_factory = DescriptorFactory()

        descriptor = descriptor_factory.create_descriptor(test_model)

        self.assertEqual('test_model', descriptor.name)
        self.assertEqual(2, len(descriptor.columns))
        self.assertEqual('id', descriptor.columns[0].name)
        self.assertEqual('uuid', descriptor.columns[0].data_type)
        self.assertEqual('some_text', descriptor.columns[1].name)
        self.assertEqual('text', descriptor.columns[1].data_type)


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
