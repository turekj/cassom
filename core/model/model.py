from core.model.model_metadata import ModelMetadataFactory, ModelMetadata


class ModelMeta(type):
    def __init__(cls, name, bases, attrs):
        super(ModelMeta, cls).__init__(name, bases, attrs)

        if not hasattr(cls, 'registry'):
            cls.registry = {}
        else:
            cls.registry[name] = cls

        if not hasattr(cls, 'metadata'):
            cls.metadata = ModelMetadata()
        else:
            cls.metadata[name] = ModelMetadataFactory().create_table_metadata(cls)


class Model(object):
    __metaclass__ = ModelMeta

    def __init__(self):
        pass
