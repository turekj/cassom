from core.model.model_metadata import ModelMetadataFactory


class ModelMeta(type):
    def __init__(cls, name, bases, attrs):
        super(ModelMeta, cls).__init__(name, bases, attrs)

        if not hasattr(cls, 'registry'):
            cls.registry = {}
        else:
            cls.registry[name] = cls


class Model(object):
    __metaclass__ = ModelMeta

    def __init__(self):
        self.metadata = ModelMetadataFactory().create_model_metadata(self)
