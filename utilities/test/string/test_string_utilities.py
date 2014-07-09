from unittest import TestCase
from utilities.string.string_utilities import StringUtilities


class TestStringUtilities(TestCase):
    def test_convert_to_underscore(self):
        camelcase = 'SomeTestCamelCaseString'

        underscore = StringUtilities.convert_to_underscore(camelcase)

        self.assertEqual('some_test_camel_case_string', underscore)
