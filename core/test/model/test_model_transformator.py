from unittest import TestCase
from core.field.field import Field
from core.model.model_metadata import ModelMetadata
from core.model.model_transformator import ModelTransformator


class TestModelTransformator(TestCase):
    def test_transform_model(self):
        transformator = ModelTransformator()
        transformator.transform_model(TestModelTransformatorModel)

        metadata = TestModelTransformatorModel.metadata
        table_metadata = TestModelTransformatorModel.metadata['test_model_transformator_model']
        managers = TestModelTransformatorModel.managers
        test_model_manager = managers['test_model_transformator_model']
        has_dummy_field = hasattr(TestModelTransformatorModel, 'dummy')
        has_multi_field = hasattr(TestModelTransformatorModel, 'multi')
        has_multi_1_field = hasattr(TestModelTransformatorModel, 'multi_1')
        has_multi_2_field = hasattr(TestModelTransformatorModel, 'multi_2')
        has_multi_3_field = hasattr(TestModelTransformatorModel, 'multi_3')

        self.assertIn('test_model_transformator_model', metadata.table_metadata)
        self.assertEqual(1, len(metadata.table_metadata))
        self.assertEqual('test_model_transformator_model', table_metadata.name)
        self.assertEqual(4, len(table_metadata.columns))
        self.assertIn('multi_f1', table_metadata.columns)
        self.assertEqual('text', table_metadata.columns['multi_f1'])
        self.assertIn('multi_f2', table_metadata.columns)
        self.assertEqual('number', table_metadata.columns['multi_f2'])
        self.assertIn('multi_f3', table_metadata.columns)
        self.assertEqual('timeuuid', table_metadata.columns['multi_f3'])
        self.assertIn('dummy', table_metadata.columns)
        self.assertEqual('', table_metadata.columns['dummy'])
        self.assertEqual(2, len(table_metadata.primary_key))
        self.assertEqual('multi_f3', table_metadata.primary_key[0])
        self.assertEqual('dummy', table_metadata.primary_key[1])
        self.assertIsNotNone(test_model_manager)
        self.assertEqual(2, len(test_model_manager.fields))
        self.assertEqual('dummy', test_model_manager.fields[0][0])
        self.assertEqual('Field', type(test_model_manager.fields[0][1]).__name__)
        self.assertEqual('multi', test_model_manager.fields[1][0])
        self.assertEqual('TestModelTransformatorMultiField', type(test_model_manager.fields[1][1]).__name__)
        self.assertTrue(has_dummy_field)
        self.assertFalse(has_multi_field)
        self.assertTrue(has_multi_1_field)
        self.assertTrue(has_multi_2_field)
        self.assertTrue(has_multi_3_field)


class TestModelTransformatorMultiField(Field):
    def table_columns(self, field_name):
        return {field_name + '_f1': 'text', field_name + '_f2': 'number', field_name + '_f3': 'timeuuid'}

    def primary_keys(self, field_name):
        return {field_name + '_f3': 100}

    def model_transformation(self, cls, field_name):
        delattr(cls, field_name)

        fields = [field_name + '_' + str(x) for x in range(1, 4)]

        for field in fields:
            setattr(cls, field, None)

        return fields


class TestModelTransformatorModel(object):
    metadata = ModelMetadata()
    managers = {}

    dummy = Field(primary_key=True, primary_key_gravity=1)
    multi = TestModelTransformatorMultiField()
