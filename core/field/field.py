class Field(object):
    def __init__(self, primary_key=False):
        self.primary_key = primary_key

    def field_type(self):
        return ''

    def is_primary_key(self):
        if hasattr(self, 'primary_key'):
            return self.primary_key

        return False
