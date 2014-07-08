from core.field.field import Field


class DenormalizedField(Field):
    def __init__(self, model, fields):
        self.model = model
        self.fields = fields

    def field_type(self):
        return 'denormalized'
