class ColumnfamilyDescriptor(object):
    def __init__(self):
        self.keyspace = ''
        self.name = ''
        self.columns = []
        self.primary_key = []


class ColumnDescriptor(object):
    def __init__(self, name=None, type=None):
        self.name = ''

        if name is not None:
            self.name = name

        if type is not None:
            self.type = type

    def __str__(self):
        return "{0} {1}".format(self.name, self.type)
