import re


class StringUtilities(object):
    first_cap_re = re.compile('(.)([A-Z][a-z]+)')
    all_cap_re = re.compile('([a-z0-9])([A-Z])')

    def __init__(self):
        pass

    @staticmethod
    def convert_to_underscore(camelcase):
        first_sub = StringUtilities.first_cap_re.sub(r'\1_\2', camelcase)
        return StringUtilities.all_cap_re.sub(r'\1_\2', first_sub).lower()
