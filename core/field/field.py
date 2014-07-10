class Field(object):
    def __init__(self, primary_key=False, primary_key_gravity=-1):
        self.primary_key = primary_key
        self.primary_key_gravity = primary_key_gravity

    def table_columns(self, field_name):
        """
        Returns mapping between required table columns names and their types.
        """
        return {field_name: ''}

    def primary_keys(self, field_name):
        """
        Returns mapping between table column names which should be part of primary key and their gravities.
        """
        if self.primary_key:
            return {field_name: self.primary_key_gravity}

        return {}

    def model_transformation(self, cls, field_name):
        """
        Performs model class transformations between logical and physical model required for this field.
        """
        return [field_name]

    def values_to_persist(self, model, field_name):
        """
        Returns mapping between table column names and their values.
        """
        return getattr(model, field_name)
