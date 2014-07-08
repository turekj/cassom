from unittest import TestCase
from utilities.module.module_utilities import ModuleUtilities


class TestModuleUtilities(TestCase):
    def test_discover_subclasses_within_module(self):
        classes = ModuleUtilities.discover_subclasses_within_module(__name__, str)

        self.assertEqual(2, len(classes))
        self.assertIn('SomeTestClass', classes)
        self.assertIn('AnotherTestClass', classes)


class SomeTestClass(str):
    pass


class AnotherTestClass(str):
    pass


class NotStrBasedClass(object):
    pass
