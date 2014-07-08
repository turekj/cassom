import inspect
import sys


class ModuleUtilities(object):
    @staticmethod
    def discover_subclasses_within_module(module, master_class):
        member_classes = inspect.getmembers(sys.modules[module], inspect.isclass)
        subclasses = filter(lambda x: issubclass(x[1], master_class), member_classes)

        return map(lambda x: x[0], subclasses)
