from core.field.fields import PasswordField


class ModelFieldsFactory(object):
    def __init__(self):
        pass

    def create_fields(self, model_class):
        fields = dir(model_class)

        for field in fields:
            value = getattr(model_class, field)

            if isinstance(value, PasswordField):
                print 'adding attribute to password field'
                pwd_field = '_' + field
                pwd_field_property = property(fget=lambda this: getattr(this, pwd_field), fset=lambda this, val: setattr(this, pwd_field, 'decrypted: ' + val))
                setattr(model_class, pwd_field, '')
                setattr(model_class, field, pwd_field_property)

