class ColumnfamilyDescriptor(object):
    def __init__(self):
        self.keyspace = ''
        self.name = ''
        self.columns = []
        self.primary_key = []


class ColumnDescriptor(object):
    def __init__(self, name=None, data_type=None):
        self.name = ''

        if name is not None:
            self.name = name

        self.data_type = ''

        if data_type is not None:
            self.data_type = data_type

    def __str__(self):
        return "{0} {1}".format(self.name, self.data_type)
