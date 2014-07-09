from core.engine.engine import Engine
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


engine = Engine.create_engine('cassandra://127.0.0.1/TestKeyspace')
Model.bind(engine)
