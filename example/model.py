from core.field.fields import TextField, PasswordField, TimestampField
from core.field.relations import DenormalizedField
from core.model.model import Model


class User(Model):
    username = TextField()
    password = PasswordField()


class Friend(Model):
    user = DenormalizedField(User, ['username'])
    friend = DenormalizedField(User, ['username'])
    since = TimestampField()


class Follower(Model):
    user = DenormalizedField(User, ['username'])
    follower = DenormalizedField(User, ['username'])
    since = TimestampField()


Model.metadata.populate()
