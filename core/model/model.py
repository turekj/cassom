from core.keyspace.keyspace_manager import KeyspaceManager
from core.model.model_fields import ModelFieldsFactory
from core.model.model_transformator import ModelTransformator
from core.table.table_manager import TableManager
from core.model.model_metadata import ModelMetadataFactory, ModelMetadata


class ModelMeta(type):
    def __init__(cls, name, bases, attrs):
        super(ModelMeta, cls).__init__(name, bases, attrs)

        if not hasattr(cls, 'registry'):
            cls.registry = {}
        else:
            cls.registry[name] = cls

        ModelTransformator().transform_model(cls)


class Model(object):
    __metaclass__ = ModelMeta
    engine = None
    keyspace_manager = KeyspaceManager()
    table_manager = TableManager()

    def __init__(self):
        pass

    @staticmethod
    def bind(engine):
        if engine is None:
            raise AttributeError('engine is not initialized')

        Model.engine = engine
        Model.create_keyspace()
        Model.create_tables()

    @staticmethod
    def create_keyspace():
        if not Model.keyspace_manager.check_keyspace_exists(Model.engine, Model.engine.get_keyspace()):
            Model.keyspace_manager.create_keyspace(Model.engine, Model.engine.get_keyspace())

    @staticmethod
    def create_tables():
        for metadata_key in Model.metadata:
            if not Model.table_manager.check_table_exists(Model.engine, metadata_key):
                Model.table_manager.create_table(Model.engine, Model.metadata[metadata_key])
