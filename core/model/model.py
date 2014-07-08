from utilities.string.string_utilities import StringUtilities


class ModelMeta(type):
    def __init__(cls, name, bases, attrs):
        super(ModelMeta, cls).__init__(name, bases, attrs)

        if not hasattr(cls, 'registry'):
            cls.registry = {}
        else:
            cls.registry[StringUtilities.convert_to_underscore(name)] = cls


class Model(object):
    __metaclass__ = ModelMeta

    def __init__(self):
        pass
